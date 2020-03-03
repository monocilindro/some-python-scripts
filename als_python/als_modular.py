import os
import subprocess
from multiprocessing import Pool, Process, Queue
from process_queues import flight_queue, tile_queue, dsm_queue
from build_tiles import build_tiles
from dsm_processing import make_input_list, make_region_blast_dsm
from quality_control import find_dropped_tiles, tile_rework

# todos
# make clip to plot function
# make dtm function
# make lasboundary use_bb for troubleshooting


las_directory = '/data/gpfs/assoc/gears/shared_data/rsdata/lidar_airborne/L1B/v001_flightline_corrections/walkerfire_20191007/las'
temp_directory = '/data/gpfs/assoc/gears/scratch/thartsook/walker_temp'
output_directory = '/data/gpfs/assoc/gears/scratch/thartsook/walker'
lastools_singularity = '/data/gpfs/assoc/gears/scratch/thartsook/gears-singularity_gears-lastools.sif'
num_workers = 32


# make temp_directory if it doesn't exist
if not os.path.exists(temp_directory + "/flightlines"):
    os.makedirs(temp_directory + "/flightlines")

# copy original flightlines to temp_directory for processing
for i in os.listdir(las_directory):
    subprocess.call(["cp", las_directory + "/" + i, temp_directory + "/flightlines"])
    print('copied ' + i)



# lasindex flightlines
print("indexing flightlines")
for filename in os.listdir(temp_directory + "/flightlines"):
    if filename.endswith(".las"):
        las_file = temp_directory + "/flightlines/" + filename
        subprocess.call(["singularity", "exec", lastools_singularity, "lasindex", "-i", filename, "-cpu64"])


flightlines = Queue()
for i in os.listdir(temp_directory + "/flightlines"):
    if i.endswith(".las"):
        flightlines.put(i)


workers = Pool(num_workers, flight_queue,(flightlines, temp_directory, lastools_singularity))
workers.close()
workers.join()


# build tiles
build_tiles(temp_directory + "/1_4", temp_directory, lastools_singularity)

# process tiles
tiles = Queue()
for i in os.listdir(temp_directory + "/tiles/raw"):
    if i.endswith(".las"):
        tiles.put(i)

workers = Pool(num_workers, tile_queue,(tiles, temp_directory + "/tiles", output_directory, lastools_singularity))
workers.close()
workers.join()

# look for tile rework
find_dropped_tiles(temp_directory + "/flightlines", output_directory + "/seamless", temp_directory)
tile_rework(temp_directory)



# make DSMS
if not os.path.exists(output_directory + "/DSM"):
    os.makedirs(output_directory + "/DSM")

make_input_list(output_directory + '/seamless', output_directory + "/DSM")
make_region_blast_dsm(output_directory + "/DSM", output_directory + "/DSM", lastools_singularity)
