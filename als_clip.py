import os
import subprocess
import shapefile
import pathlib

tile_directory = '/home/theo/Desktop/walker_seamless'
plot_directory = '/home/theo/Desktop/clipped_walker_tls'
shapefile_directory = '/home/theo/Desktop/clipped_walker_tls'
#plot_directory = '/home/theo/Desktop/Plot_Centers_Poly/individual'
output_directory = '/home/theo/Desktop/walker_als_plots'
temp_directory = '/home/theo/Desktop'


# Todos from 3/7
# Extend tile matching for 3rd and 4th scenarios
# Move the clip command to the end so I don't make double clips

# Sure, I can match these tiles using the shapefile, but at this point, why not just read bounding boxes directly?
# A: Keep the shapefile functionality for clipping TLS to plot boundary
'''
sf = shapefile.Reader("/home/theo/Desktop/Plot_Centers_Poly/individual/Plot_Centers_Poly_Plot_ID_P001")
print(sf.bbox)
#bbox returns xmin, ymin, xmax, ymax

contained_sf = ['-4700900', '-4700100', '3100100', '3099800']
'''
'''
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
            print(bbox)
        f.close()
with open("/home/theo/Desktop/plot_coordinates.txt", "w") as f:
    for i in plot_coordinates:
        f.write(str(i) + "\n")
f.close()
'''

'''
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
with open("/home/theo/Desktop/tile_coordinates.txt", "w") as f:
    for i in tile_coordinates:
        f.write(str(i) + "\n")
f.close()
'''

tile_coordinates = []
with open("/home/theo/Desktop/tile_coordinates.txt", "r") as f:
    for line in f:
        tile_coordinates.append(line)

plot_coordinates = []
with open("/home/theo/Desktop/plot_coordinates.txt", "r") as f:
    for line in f:
        plot_coordinates.append(line)
match = []
for i in plot_coordinates:
    # Set up min and max plot coordinates

    line = i.split()
    pxn = float(line[1].strip("',[]"))
    pxx = float(line[3].strip("',[]"))
    pyn = float(line[2].strip("',[]"))
    pyx = float(line[4].strip("',[]"))

    plot = line[0]
    plot_id = plot[40:46]
    shapefile = ''

    for shape in os.listdir(shapefile_directory):
        if plot_id in shape and shape.endswith('.shp'):
            shapefile = shapefile_directory + '/' + shape
    print(type(shapefile))

    tile_matches = []

    for j in tile_coordinates:
        line = j.split()
        txn = float(line[1].strip("',[]"))
        txx = float(line[3].strip("',[]"))
        tyn = float(line[2].strip("',[]"))
        tyx = float(line[4].strip("',[]"))

        if pxn > txn and pyn > tyn and pxx < txx and pyx < tyx:
            tile_matches.append(line[0])
        elif pxn > txn and pxn < txx and pxx > txx:
            if pyn > tyn and pyx < tyx:
                tile = line[0]
                #print(tile[37:50])
                next_tile = int(tile[37:43]) + 1000
                first_tile = tile[2:-2]
                second_tile = tile[2:37] + str(next_tile) + tile[43:-2]
                print(first_tile)
                print(second_tile)
                #tile_coord = 
                subprocess.call(['lasclip', '-i', first_tile, second_tile, '-merged', '-poly', shapefile, '-odir', output_directory])
        elif pyn > tyn and pyn < tyx and pyx > tyx:
            if pxn > txn and pxx < txx:
                tile_matches.append(line[0])
        elif pxn > txn and pxn < txx and pxx > txx:
            if pyn > tyn and pyn < tyx and pyx > tyx:
                tile_matches.append(line[0])

# think of ways to simplify
# containment check is good
# if plot's min x value is great than tile min and less than tile max, it starts in plot x,y and ends in x,y+1
# if plot's min y value is great than tile min and less than tile max, it starts in plot x,y and ends in x+1,y
# if those statements are both true, it needs to be clipped with x,y;x+1,y;x,y+1;x+1,y+1



'''
for tile in os.listdir(als_directory):
    input_tile = als_directory + "/" + tile
    for plot in os.listdir(plot_directory):
        if plot.endswith(".shp"):
            shape = plot_directory + "/" + plot
            plot_id = plot[0:4]
            output_name = plot_id + "_clipped.las"
            subprocess.call(["lasclip", "-i", input_tile, "-poly", shape, "-o", output_name, "-odir", output_directory])
'''
