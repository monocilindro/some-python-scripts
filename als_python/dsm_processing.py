import os
import subprocess
gm = '/usr/bin/gdal_merge.py'

def make_tile_dsm(tile, output_directory, lastools_singularity, epsg=str(3310)):
    subprocess.call(["singularity", "exec", lastools_singularity, "las2dem", "-i", tile, "-otif", "-epsg", epsg, "-keep_class", "2", "-step", "1", "-odir", output_directory])    

def make_region_dsm(tile_directory, output_directory, prefix, gdal_singularity):
    merge_call = ["singularity", "exec", gdal_singularity, "python3", gm, "-o", output_directory + "/" + prefix + "_DSM.tif"]
    for i in os.listdir(tile_directory):
        if i.endswith(".tif"):
            merge_call.append(tile_directory + "/" + i)
    subprocess.call(merge_call)
