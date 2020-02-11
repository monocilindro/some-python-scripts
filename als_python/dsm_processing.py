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

def make_input_list(tile_directory, output_directory, chunk_size=500):
    input_list = []
    for i in os.listdir(tile_directory):
        if i.endswith(".las"):
            las_file = str(tile_directory + "/" + i)
            input_list.append(las_file)
    input_list.sort()
    if len(input_list) > chunk_size:
        counter = 0
        for i in range(0, len(input_list), chunk_size):
            counter = counter + 1
            upper_limit = i + chunk_size
            temp_list = input_list[i:upper_limit]
            with open(output_directory + "/tile_inputs_" + str(counter), 'w') as f:
                for item in temp_list:
                    f.write(item + "\n")
            f.close()
            
    else:
        with open(output_directory + "/tile_inputs", 'w') as f:
            for item in input_list:
                f.write(item + "\n")
        f.close()
    
def make_region_blast_dsm(input_list_location, output_directory, lastools_singularity, step=str(1), epsg=str(3310)):
    input_lists = []
    for i in os.listdir(input_list_location):
        if i.startswith("tile_inputs_"):
            lof = input_list_location + "/" + i
            input_lists.append(lof)
    input_lists.sort()
    counter = 0
    for i in input_lists:
        counter = counter + 1
        output_name = "plumas_dsm_" + str(counter) + '.tif'
        subprocess.call(["singularity", "exec", lastools_singularity, "blast2dem", "-lof", i, "-otif", "-epsg", epsg , "-keep_class", "2", "-step", str(step), "-merged", "-o", output_name, "-odir", output_directory])
