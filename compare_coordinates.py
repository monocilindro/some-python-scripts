import os
import subprocess

tile_directory = '/home/theo/Desktop/walker_seamless'
plot_directory = '/home/theo/Desktop/clipped_walker_tls'
output_directory = '/home/theo/Desktop/walker_als_plots'
temp_directory = '/home/theo/Desktop'


# create a .txt file with plot coordinates (or anything to clip to)
def create_plot_coordinates_list(plot_directory, temp_directory):
    plot_coordinates = []
    for plot in os.listdir(plot_directory):
        if plot.endswith(".las"):
            las_file = plot_directory + "/" + plot
            text_name = temp_directory + "/temp_info.txt"
            if os.path.exists(text_name):
                os.remove(text_name)
            subprocess.call(["lasinfo", "-i", las_file, "-o", text_name, "-nco"])
            with open(text_name, "r") as f:
                bbox = []
                bbox.append(las_file)
                for line in f:
                    if "min x y z:" in line:
                        min_coord = line.split()
                        bbox.append(min_coord[4])
                        bbox.append(min_coord[5])
                    elif "max x y z:" in line:
                        max_coord = line.split()
                        bbox.append(max_coord[4])
                        bbox.append(max_coord[5])
                plot_coordinates.append(bbox)
            f.close()
    with open(temp_directory + '/plot_coordinates.txt', 'w') as f:
        for i in plot_coordinates:
            f.write(str(i) + '\n')
    f.close()


# create a .txt file with tile coordinates (or anything you want to clip)
def create_tile_coordinates_list(tile_directory, temp_directory):
    tile_coordinates = []
    for tile in os.listdir(tile_directory):
        if tile.endswith(".las"):
            las_file = tile_directory + "/" + tile
            text_name = temp_directory + "/temp_info.txt"
            if os.path.exists(text_name):
                os.remove(text_name)
            subprocess.call(["lasinfo", "-i", las_file, "-o", text_name, "-nco"])
            with open(text_name, "r") as f:
                bbox = []
                bbox.append(las_file)
                for line in f:
                    if "min x y z:" in line:
                        min_coord = line.split()
                        bbox.append(min_coord[4])
                        bbox.append(min_coord[5])
                    elif "max x y z:" in line:
                        max_coord = line.split()
                        bbox.append(max_coord[4])
                        bbox.append(max_coord[5])
                tile_coordinates.append(bbox)
            f.close()
    with open(temp_directory + '/tile_coordinates.txt', 'w') as f:
        for i in tile_coordinates:
            f.write(str(i) + "\n")
    f.close()


# checks each corner of the input plot (p##) and checks if it is contained within the tile (t##)
# Returns a list of the lower left, upper left, lower right, and upper right corners and if they matched
def check_coordinates(pxn, pxx, pyn, pyx, txn, txx, tyn, tyx):
    matches = [0, 0, 0, 0]
    if txn < pxn < txx and tyn < pyn < tyx:
        matches[0] = 1
    if txn < pxn < txx and tyn < pyx <= tyx:
        matches[1] = 1
    if txn < pxx <= txx and tyn < pyn < tyx:
        matches[2] = 1
    if txn < pxx <= txx and tyn < pyx <= tyx:
        matches[3] = 1
    return(matches)


# This is the main processing step

tile_list = temp_directory + '/tile_coordinates.txt'
tile_coordinates = []

try:
    with open(tile_list, 'r') as f:
        for line in f:
            tile_coordinates.append(line)
except FileNotFoundError:
        create_tile_coordinates_list(tile_directory, temp_directory)

plot_list = temp_directory + '/plot_coordinates.txt'
plot_coordinates = []

try:
    with open(plot_list, 'r') as f:
        for line in f:
            plot_coordinates.append(line)
except FileNotFoundError:
        create_plot_coordinates_list(plot_directory, temp_directory)

for i in plot_coordinates:
    # Set up min and max plot coordinates

    line = i.split()
    pxn = float(line[1].strip("',[]"))
    pxx = float(line[3].strip("',[]"))
    pyn = float(line[2].strip("',[]"))
    pyx = float(line[4].strip("',[]"))

    plot = line[0].strip("',[]")
    plot_id = plot[40:46]
    tiles = []

    for j in tile_coordinates:
        line = j.split()
        txn = float(line[1].strip("',[]"))
        txx = float(line[3].strip("',[]"))
        tyn = float(line[2].strip("',[]"))
        tyx = float(line[4].strip("',[]"))
        check = check_coordinates(pxn, pxx, pyn, pyx, txn, txx, tyn, tyx)   
        if 1 in check:
            tiles.append(line[0])
    shapefile = temp_directory + '/tmp.shp'
    clipped_las = output_directory + '/' + str(plot_id) + '_clipped_30.las'
    if len(tiles) == 1:
        subprocess.call(['lasboundary', '-i', tiles[0].strip("',[]"), '-use_bb', '-o', shapefile, '-epsg', '3310'])
    if len(tiles) == 2:
        subprocess.call(['lasboundary', '-i', tiles[0].strip("',[]"), tiles[1].strip("',[]"), '-merged', '-use_bb', '-o', shapefile, '-epsg', '3310'])
    # sidenote: I think we could have an edge case where only three tiles overlap
    if len(tiles) == 3:
        subprocess.call(['lasboundary', '-i', tiles[0].strip("',[]"), tiles[1].strip("',[]"), tiles[2].strip("',[]"), '-merged', '-use_bb', '-o', shapefile, '-epsg', '3310'])
    if len(tiles) == 4:
        subprocess.call(['lasboundary', '-i', tiles[0].strip("',[]"), tiles[1].strip("',[]"), tiles[2].strip("',[]"), tiles[3].strip("',[]"), '-merged', '-use_bb', '-o', shapefile, '-epsg', '3310'])
    print(plot)
    subprocess.call(['lasclip', '-i', plot, '-poly', shapefile, '-o', clipped_las])
