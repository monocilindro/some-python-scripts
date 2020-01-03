# todos
# add prefix based off flightline
# divide up input list

import os
import subprocess
import csv

las_directory = '/data/gpfs/assoc/gears/shared_data/rsdata/lidar_airborne/L1B/vendor/ASO/Plumas/2018/corrected_flightlines/correction'
shapefile_directory = '/data/gpfs/assoc/gears/scratch/thartsook/individual_plots
temp_directory = '/data/gpfs/assoc/gears/scratch/thartsook/plumas_temp'
output_directory = '/data/gpfs/assoc/gears/scratch/thartsook/plumas'
lastools_singularity = '/data/gpfs/assoc/gears/scratch/thartsook/gears-singularity_gears-lastools.sif'

# ask Martin where are best places to put the index calls
'''
for filename in os.listdir(las_directory):
    if filename.endswith(".las"):
        las_file = las_directory + "/" + filename
        subprocess.call(["singularity", "exec", lastools_singularity, "lasindex", "-i", filename, "-cpu64"])'''

# Get projection info

for filename in os.listdir(las_directory):
    if filename.endswith(".las"):
        las_file = las_directory + "/" + filename
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

# 1.4 conversion
for filename in os.listdir(temp_directory):
    if filename.endswith("reproject.las"):
        las_file = temp_directory + "/" + filename
        subprocess.call(["singularity", "exec", lastools_singularity, "las2las", "-i", las_file,  "-set_version", "1.4", "-odix", "_14", "-odir", temp_directory, "-cpu64"])

# Build tiles
for filename in os.listdir(temp_directory):
    if filename.endswith("14.las"):
        las_file = temp_directory + "/" + filename
        subprocess.call(["singularity", "exec", lastools_singularity, "lastile", "-i", las_file, "-files_are_flightlines", "-rescale", "0.01", "0.01", "0.01", "-tile_size", "1000", "-buffer", "100", "-odir", temp_directory, "-odix", "_plumas_tile", "-cpu64"])

# Denoise
for filename in os.listdir(temp_directory):
    if filename.endswith("plumas_tile.las"):
        las_file = temp_directory + "/" + filename
        subprocess.call(["singularity", "exec", lastools_singularity, "lasnoise", "-i", las_file, "-remove_noise", "-odir", temp_directory, "-odix", "_denoised", "-cpu64"])

# Classify ground
for filename in os.listdir(temp_directory):
    if filename.endswith("denoised.las"):
        las_file = temp_directory + "/" + filename
        subprocess.call(["singularity", "exec", lastools_singularity, "lasground", "-i", las_file, "-ultra_fine", "-step", "3", "-odir", temp_directory, "-odix", "_ground", "-cpu64"])

# Get height
for filename in os.listdir(temp_directory):
    if filename.endswith("singularity", "exec", lastools_singularity, "ground.las"):
        las_file = temp_directory + "/" + filename
        subprocess.call(["lasheight", "-i", las_file, "-drop_below", "0", "-drop_above", "100", "-odir", temp_directory, "-odix", "_height", "-cpu64"])

# Classify remaining points
for filename in os.listdir(temp_directory):
    if filename.endswith("singularity", "exec", lastools_singularity, "height.las"):
        las_file = temp_directory + "/" + filename
        subprocess.call(["singularity", "exec", lastools_singularity, "lasclassify", "-i", las_file, "-ground_offset", "0.2", "-odir", output_directory, "-odix", "_buffered", "-cpu64"])

# Clip to plot
for filename in os.listdir(temp_directory):
    if filename.endswith("classified.las"):
        plot_id=filename[0:4] # multiple scans don't matter for clipping to plot
        las_file = temp_directory + "/" + filename
        shapefile = shapefile_directory + "/Plot_Centers_Poly_Plot_ID_" + plot_id + ".shp"
        print("this is a sample shapefile name " + shapefile)
        subprocess.call(["lasclip", "-i", las_file, "-poly", shapefile, "-odir", output_directory, "-odix", "_clipped", "-cpu64"])


