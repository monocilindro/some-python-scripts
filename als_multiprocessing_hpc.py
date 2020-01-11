# todos
# add prefix based off flightline
# divide up input list
# add check for temp folder

import os
import subprocess
import csv
from multiprocessing import Process

#las_directory = '/data/gpfs/assoc/gears/shared_data/rsdata/lidar_airborne/L1B/vendor/ASO/Plumas/2018/corrected_flightlines/correction'


las_directory = '/data/gpfs/assoc/gears/scratch/thartsook/tahoe_flightlines'
shapefile_directory = '/data/gpfs/assoc/gears/scratch/thartsook/individual_plots'
temp_directory = '/data/gpfs/assoc/gears/scratch/thartsook/tahoe_temp'
output_directory = '/data/gpfs/assoc/gears/scratch/thartsook/tahoe_multiprocess'
lastools_singularity = '/data/gpfs/assoc/gears/scratch/thartsook/gears-singularity_gears-lastools.sif'

def flightlines_to_tiles(flightline):
    # Get projection info
    print("projection")
    if flightline.endswith(".las"):
        las_file = las_directory + "/" + flightline
        wgs = "0"
        utm = "0"
        if os.path.exists(temp_directory + "/temp_info.txt"):
            os.remove(temp_directory + "/temp_info.txt")
    subprocess.call(["singularity", "exec", lastools_singularity, "lasinfo", "-i", las_file, "-o", "temp_info.txt", "-odir", temp_directory])
    with open(temp_directory + "/temp_info.txt") as f:
        for line in f:
            if "GTCitationGeoKey" in line:
                if "WGS 84" in line:
                    wgs = "84"
                if "UTM zone 10N" in line:
                    utm = "10n"
                if "UTM zone 11N" in line:
                    utm = "11n"
            if wgs != 0:
                wgs_flag = "-wgs84"

        # Reproject from UTM to CA Albers
        subprocess.call(["singularity", "exec", lastools_singularity, "las2las", "-i", las_file, "-utm", utm, wgs_flag, "-target_epsg", "3310", "-odir", temp_directory, "-odix", "_reproject", "-cpu64"])
        f.close()

    print("conversion")
    las_file = temp_directory + "/" + flightline[:-4] + "_reproject.las"
    subprocess.call(["singularity", "exec", lastools_singularity, "las2las", "-i", las_file,  "-set_version", "1.4", "-odix", "_14", "-odir", temp_directory, "-cpu64"])


# -------------------

def tile_processing(tile):
# Denoise
    print("denoise")
    las_file = temp_directory + "/tiles/" + tile[:-4] + ".las"
    print(las_file)
    subprocess.call(["singularity", "exec", lastools_singularity, "lasnoise", "-i", las_file, "-remove_noise", "-odir", temp_directory, "-odix", "_denoised", "-cpu64"])

# Classify ground
    print("ground")
    las_file = temp_directory + "/" + tile[:-4] + "_denoised.las"
    subprocess.call(["singularity", "exec", lastools_singularity, "lasground", "-i", las_file, "-ultra_fine", "-step", "3", "-odir", temp_directory, "-odix", "_ground", "-cpu64"])

# Get height
    print("height")
    las_file = temp_directory + "/" + tile[:-4] + "_denoised_ground.las"
    subprocess.call(["singularity", "exec", lastools_singularity, "lasheight", "-i", las_file, "-drop_below", "0", "-drop_above", "100", "-odir", temp_directory, "-odix", "_height", "-cpu64"])

# Classify remaining points
    print("classify")
    las_file = temp_directory + "/" + tile[:-4] + "_denoised_ground_height.las"
    subprocess.call(["singularity", "exec", lastools_singularity, "lasclassify", "-i", las_file, "-ground_offset", "0.2", "-odir", output_directory, "-odix", "_buffered", "-cpu64"])

# Create seamless tiles
    print("seamless")
    las_file = output_directory + "/" + tile[:-4] + "_denoised_ground_height_buffered.las"
    subprocess.call(["singularity", "exec", lastools_singularity, "lastile", "-i", las_file, "-remove_buffer", "-odir", output_directory, "-odix", "_seamless", "-cpu64"])

# Clip to plot
    print("plot clip")
    las_file = output_directory + "/" + tile[:-4] + "_denoised_ground_height_buffered.las"
    plot_id=filename[0:4] # multiple scans don't matter for clipping to plot
    shapefile = shapefile_directory + "/Plot_Centers_Poly_Plot_ID_" + plot_id + ".shp"
    subprocess.call(["singularity", "exec", lastools_singularity, "lasclip", "-i", las_file, "-poly", shapefile, "-odir", output_directory, "-odix", plot_id, "-cpu64"])
    
# -------------------

def divide_inputs(input_folder, ending = ".las", num_cpus=32):
    inputs = []
    for filename in os.listdir(input_folder):
        if filename.endswith(ending):
            input_path = input_folder + "/" + filename
            inputs.append(input_path)
    chunk_size = round(len(inputs)/num_cpus)
    for i in range(num_cpus):
        chunk_file = temp_directory + "/input_" + str(i) + ".txt"
        chunks = []
        for j in range(chunk_size):
            chunks.append(inputs.pop())
        with open(chunk_file, 'w') as f:
            for line in chunks:
                f.write(line + "\n")
        f.close()



# -------------------

# -------------------

# lasindex flightlines
os.chdir(las_directory)
print("indexing flightlines")
for filename in os.listdir(las_directory):
    if filename.endswith(".las"):
        las_file = las_directory + "/" + filename
        subprocess.call(["singularity", "exec", lastools_singularity, "lasindex", "-i", filename, "-cpu64", "-dont_reindex"])

# multiprocess flightlines
processes = []
for flightline in os.listdir(las_directory):
    if flightline.endswith(".las"):
        processes.append(Process(target=flightlines_to_tiles, args=(flightline, )))
    else:
        continue

for p in processes:
    p.start()
for p in processes: 
    p.join() 



# build tiles
print("tiles")
for filename in os.listdir(temp_directory):
    if filename.endswith("14.las"):
        las_file = temp_directory + "/" + filename
        subprocess.call(["singularity", "exec", lastools_singularity, "lastile", "-i", las_file, "-files_are_flightlines", "-rescale", "0.01", "0.01", "0.01", "-tile_size", "1000", "-buffer", "100", "-odir", temp_directory + "/tiles", "-odix", "_plumas_tile"])


# multiprocess tiles
processes = []
for tile in os.listdir(temp_directory + "/tiles"): 
    if tile.endswith(".las"):
        processes.append(Process(target=tile_processing, args=(tile, )))
    else:
        continue

for p in processes: 
    p.start()
for p in processes: 
    p.join() 


