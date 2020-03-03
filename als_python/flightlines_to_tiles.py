import os
import subprocess

# add copy from source to temp_flightlines (this has been handled in the main function currently
# consider combining reproject and 1.4 step

def flightlines_to_tiles(flightline, temp_directory, lastools_singularity):
    # Get projection info
    las_file = temp_directory +  "/flightlines/" + flightline
    wgs = "0"
    utm = "0"
    text_name = las_file[:-4] + "_info.txt"
    if os.path.exists(text_name):
        os.remove(text_name)
    subprocess.call(["singularity", "exec", lastools_singularity, "lasinfo", "-i", las_file, "-o", text_name])
    with open(text_name) as f:
        for line in f:
            if "key 3072" in line:
                if "WGS 84" in line and "UTM 10N" in line:
                    wgs = "-wgs84"
                    utm = "10n"
                if "WGS 84" in line and "UTM 11N" in line:
                    wgs = "-wgs84"
                    utm = "11n"

        # Reproject from UTM to CA Albers
        if not os.path.exists(temp_directory + "/reproject"):
            os.makedirs(temp_directory + "/reproject")
        subprocess.call(["singularity", "exec", lastools_singularity, "las2las", "-i", las_file, "-utm", utm, wgs, "-target_epsg", "3310", "-odir", temp_directory + "/reproject", "-odix", "_reproject", "-cpu64"])
        f.close()


    # Convert from LAS 1.2 to LAS 1.4
    if not os.path.exists(temp_directory + "/1_4"):
            os.makedirs(temp_directory + "/1_4")
    las_file = temp_directory + "/reproject/" + flightline[:-4] + "_reproject.las"
    subprocess.call(["singularity", "exec", lastools_singularity, "las2las", "-i", las_file,  "-set_version", "1.4", "-odix", "_14", "-odir", temp_directory + "/1_4", "-cpu64"])
