import os
import subprocess

def build_tiles(input_directory, lastools_singularity, tile_length=1000, buffer_length=100):
    if not os.path.exists(input_directory + "/tiles/raw"):
        os.makedirs(input_directory + "/tiles/raw")
    flightlines = input_directory + "\*.las"
    subprocess.call(["singularity", "exec", lastools_singularity, "lastile", "-i", flightlines, "-files_are_flightlines", "-rescale", "0.01", "0.01", "0.01", "-tile_size", str(tile_length), "-buffer", str(buffer_length), "-odir", input_directory + "/tiles/raw"])

# this is not the correct way to solve the problem. Can't be parallelized with worker queue.
def build_tiles_bad(input_directory, append_tag, lastools_singularity, tile_length=1000, buffer_length=100):

    for filename in os.listdir(input_directory + "/1_4"):
        if filename.endswith("14.las"):
            las_file = input_directory + "/1_4/" + filename
            subprocess.call(["singularity", "exec", lastools_singularity, "lastile", "-i", las_file, "-files_are_flightlines", "-rescale", "0.01", "0.01", "0.01", "-tile_size", str(tile_length), "-buffer", str(buffer_length), "-odir", input_directory + "/tiles/raw", "-odix", append_tag])
