import os
import subprocess

def build_tiles(input_directory, temp_directory, lastools_singularity, tile_length=1000, buffer_length=100):
    if not os.path.exists(temp_directory + "/tiles/raw"):
        os.makedirs(temp_directory + "/tiles/raw")
    flightlines = input_directory + "/*.las"
    subprocess.call(["singularity", "exec", lastools_singularity, "lastile", "-i", flightlines, "-files_are_flightlines", "-rescale", "0.01", "0.01", "0.01", "-tile_size", str(tile_length), "-buffer", str(buffer_length), "-odir", temp_directory + "/tiles/raw"])
