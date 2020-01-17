import os
import subprocess

def tile_processing(tile, temp_directory, output_directory, lastools_singularity):
    # Denoise
    if not os.path.exists(temp_directory + "/denoise"):
            os.makedirs(temp_directory + "/denoise")
    las_file = temp_directory + "/raw/" + tile
    print(las_file)
    subprocess.call(["singularity", "exec", lastools_singularity, "lasnoise", "-i", las_file, "-remove_noise", "-odir", temp_directory + "/denoise", "-odix", "_denoised", "-cpu64"])

    # Classify ground
    if not os.path.exists(temp_directory + "/ground"):
            os.makedirs(temp_directory + "/ground")
    las_file = temp_directory + "/denoise/" + tile[:-4] + "_denoised.las"
    subprocess.call(["singularity", "exec", lastools_singularity, "lasground", "-i", las_file, "-ultra_fine", "-step", "3", "-odir", temp_directory + "/ground", "-odix", "_ground", "-cpu64"])

    # Get height
    if not os.path.exists(temp_directory + "/height"):
            os.makedirs(temp_directory + "/height")
    las_file = temp_directory + "/ground/" + tile[:-4] + "_denoised_ground.las"
    subprocess.call(["singularity", "exec", lastools_singularity, "lasheight", "-i", las_file, "-drop_below", "0", "-drop_above", "100", "-odir", temp_directory + "/height", "-odix", "_height", "-cpu64"])

    # Classify remaining points
    if not os.path.exists(output_directory + "/buffered"):
            os.makedirs(output_directory + "/buffered")
    las_file = temp_directory + "/height/" + tile[:-4] + "_denoised_ground_height.las"
    subprocess.call(["singularity", "exec", lastools_singularity, "lasclassify", "-i", las_file, "-ground_offset", "0.2", "-odir", output_directory + "/buffered", "-odix", "_buffered", "-cpu64"])

    # Create seamless tiles
    if not os.path.exists(output_directory + "/seamless"):
            os.makedirs(output_directory + "/seamless")
    las_file = output_directory + "/buffered/" + tile[:-4] + "_denoised_ground_height_buffered.las"
    subprocess.call(["singularity", "exec", lastools_singularity, "lastile", "-i", las_file, "-remove_buffer", "-odir", output_directory + "/seamless", "-odix", "_seamless", "-cpu64"])

'''
    # Clip to plot
    las_file = output_directory + "/" + tile[:-4] + "_denoised_ground_height_buffered.las"
    plot_id=filename[0:4] # multiple scans don't matter for clipping to plot
    shapefile = shapefile_directory + "/Plot_Centers_Poly_Plot_ID_" + plot_id + ".shp"
    subprocess.call(["singularity", "exec", lastools_singularity, "lasclip", "-i", las_file, "-poly", shapefile, "-odir", output_directory, "-odix", plot_id, "-cpu64"])
'''
# Clip to plot should be its own function
