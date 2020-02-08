import os
import subprocess
import math

input_directory = '/home/theo/Desktop/ferguson/height_normalized/postfire_tls_height_norm'
output_directory = '/home/theo/Desktop/rasterized'
temp_directory = '/home/theo/Desktop/ferguson/temp_feb_7'
vertical_slice = 1

def find_max_height(filename, input_directory, temp_directory):
    las_file = input_directory + "/" + filename
    text_name = filename[:-4] + "_info.txt"
    max_height = 0
    subprocess.call(["lasinfo", "-i", las_file, "-o", text_name, "-odir", temp_directory])
    with open(temp_directory + "/" + text_name) as f:
        for line in f:
            if "max x y z:" in line:
                max_height = math.ceil(float(line[-9:]))
    f.close()
    return max_height

def build_slices(filename, max_height = 70, vertical_slice = 1):
    for i in range(0, max_height):
        lower = i
        upper = lower + vertical_slice
        rasterize_slice(filename, input_directory, upper, lower)

def rasterize_slice(filename, input_directory, upper, lower):
    lasfile = input_directory + '/' + filename
    plot_id = filename[0:4]
    output_name = plot_id + "_" + str(lower) + "_" + str(upper) + "_elev.png"
    subprocess.call(["lasgrid", "-i", lasfile, "-step", "0.10", "-drop_class", "8", "-keep_z", str(lower), str(upper), "-nbits", "2", "-opng", "-o", output_name, "-odir", output_directory])

for filename in os.listdir(input_directory):
    if filename.endswith(".las"):
        highest_point = find_max_height(filename, input_directory, temp_directory)
        build_slices(filename, highest_point, vertical_slice)
