import os
import subprocess

# add copy from source to temp_flightlines

def flightlines_to_tiles(flightline, temp_directory, lastools_singularity):
    # Get projection info
    las_file = flightline
    wgs = "0"
    utm = "0"
    text_name = las_file[:-4] + "_info.txt"
    if os.path.exists(temp_directory + "/" + text_name):
        os.remove(temp_directory + "/" + text_name)
    subprocess.call(["singularity", "exec", lastools_singularity, "lasinfo", "-i", las_file, "-o", text_name, "-odir", temp_directory + "/flightlines"])
    with open(temp_directory + "/flightlines/" + text_name) as f:
        for line in f:
            if "GTCitationGeoKey" in line:
                if "WGS 84" in line:
                    wgs = "84"
                if "UTM zone 10N" in line:
                    utm = "10n"
                if "UTM zone 11N" in line:
                    utm = "11n"
            if wgs != 0:
                wgs_flag = "-wgs84"

        # Reproject from UTM to CA Albers
        if not os.path.exists(temp_directory + "/reproject"):
            os.makedirs(temp_directory + "/reproject")
        subprocess.call(["singularity", "exec", lastools_singularity, "las2las", "-i", las_file, "-utm", utm, wgs_flag, "-target_epsg", "3310", "-odir", temp_directory + "/reproject", "-odix", "_reproject", "-cpu64"])
        f.close()


    # Convert from LAS 1.2 to LAS 1.4
    if not os.path.exists(temp_directory + "/1_4"):
            os.makedirs(temp_directory + "/1_4")
    las_file = temp_directory + "/reproject/" + flightline[:-4] + "_reproject.las"
    subprocess.call(["singularity", "exec", lastools_singularity, "las2las", "-i", las_file,  "-set_version", "1.4", "-odix", "_14", "-odir", temp_directory + "/1_4", "-cpu64"])
