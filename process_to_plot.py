#goal: reproject each uav plot, do the classification, clip to plot. use reference table to get reproject values

import os
import subprocess
import csv

#directory = '/data/gpfs/assoc/gears/scratch/thartsook/uav_merge/2018'
#plot_reference_table = '/data/gpfs/assoc/gears/scratch/thartsook/plot_info_reference.csv'
las_directory = '/home/theo/Desktop/text'
plot_reference_table = '/home/theo/Desktop/uav_info.csv'
plot_boundary_directory = '/home/theo/Desktop/Plot_Centers_Poly/individual'
temp_directory = '/home/theo/Desktop/temp_uav'
shapefile_directory = '/home/theo/Desktop/Plot_Centers_Poly/individual'
output_directory = '/home/theo/Desktop/'

# this could be replaced with a lasinfo call
'''
ref = csv.DictReader(open(plot_reference_table))
for filename in os.listdir(las_directory):            
    if filename.endswith(".las"):
        las_file = las_directory + "/" + filename
        plot_id=filename[:-11] # multiple scans don't matter for reproject values
        wgs = "0"
        utm = "0"
        for row in ref:
            ref_id = row["plot_id"]
            if plot_id == ref_id:
                wgs = row["wgs"]
                utm = row["utm"]
        if wgs != 0:
            wgs_flag = "-wgs84"
        #print(plot_id + " " + wgs + " " + utm) # test to see if parsing works
        os.path.isdir(temp_directory)
'''
for filename in os.listdir(las_directory):
    if filename.endswith(".las"):
        las_file = las_directory + "/" + filename
        wgs = "0"
        utm = "0"
        if os.path.exists(temp_directory + "/temp_info.txt"):
            os.remove(temp_directory + "/temp_info.txt")
        subprocess.call(["lasinfo", "-i", las_file, "-o", "temp_info.txt", "-odir", temp_directory])
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
        subprocess.call(["las2las", "-i", las_file, "-utm", utm, wgs_flag, "-target_epsg", "3310", "-odir", temp_directory, "-odix", "_reproject", "-cpu64"])
        f.close()
'''
# Denoise
for filename in os.listdir(temp_directory):
    if filename.endswith("reproject.las"):
        las_file = temp_directory + "/" + filename
        subprocess.call(["lasnoise", "-i", las_file, "-remove_noise", "-odir", temp_directory, "-odix", "_denoised", "-cpu64"])
# Classify ground
for filename in os.listdir(temp_directory):
    if filename.endswith("denoised.las"):
        las_file = temp_directory + "/" + filename
        subprocess.call(["lasground", "-i", las_file, "-ultra_fine", "-step", "3", "-odir", temp_directory, "-odix", "_ground", "-cpu64"])

# Get height
for filename in os.listdir(temp_directory):
    if filename.endswith("ground.las"):
        las_file = temp_directory + "/" + filename
        subprocess.call(["lasheight", "-i", las_file, "-drop_below", "0", "-drop_above", "100", "-odir", temp_directory, "-odix", "_height", "-cpu64"])

# Classify remaining points
for filename in os.listdir(temp_directory):
    if filename.endswith("height.las"):
        las_file = temp_directory + "/" + filename
        subprocess.call(["lasclassify", "-i", las_file, "-ground_offset", "0.2", "-odir", temp_directory, "-odix", "_classified", "-cpu64"])

# Clip to plot
for filename in os.listdir(temp_directory):
    if filename.endswith("classified.las"):
        plot_id=filename[0:4] # multiple scans don't matter for clipping to plot
        las_file = temp_directory + "/" + filename
        shapefile = shapefile_directory + "/Plot_Centers_Poly_Plot_ID_" + plot_id + ".shp"
        print("this is a sample shapefile name " + shapefile)
        subprocess.call(["lasclip", "-i", las_file, "-poly", shapefile, "-odir", output_directory, "-odix", "_clipped", "-cpu64"])
'''
