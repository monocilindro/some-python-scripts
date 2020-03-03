import os
from tile_processing import tile_processing

# find the stragglers
# compare tiles in buffer with tiles in raw
# missing tiles should get the processing rerun
# report missing tiles in a .txt file

def find_dropped_tiles(raw_tiles, seamless_tiles, error_directory):
    dropped_tiles = []
    for i in os.listdir(raw_tiles):
        raw_name = i.split('_')
        raw_tile = raw_name[0] + "_" + raw_name[1] + ".las"
        dropped_flag = 0
        for j in os.listdir(seamless_tiles):
            seamless_name = j.split('_')
            seamless_tile = seamless_name[0] + '_' + seamless_name[1] + ".las"
            if raw_tile == seamless_tile:
                dropped_flag = 1

        if dropped_flag == 0:            
            dropped_tiles.append(raw_tile)
    with open(error_directory + "/dropped_tiles.txt", 'w') as f:
        for item in dropped_tiles:
            f.write(raw_tiles + "/" + item + "\n")
        f.close()

def tile_rework(error_directory):
    with open(error_directory + "/dropped_tiles.txt", 'r') as f:
        tiles = f.readlines()
        for i in tiles:
            tile_processing(i, input_directory, output_directory, lastools_singularity)
