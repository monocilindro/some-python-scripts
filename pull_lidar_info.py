import os
import subprocess
import csv

directory = '/home/theo/Desktop/1_Combined'
plot_reference_table = '/home/theo/Desktop/plot_info_reference.csv'
for filename in os.listdir(directory):
    if filename.endswith(".las"):
        las_file = directory + '/' + filename
        subprocess.call(["lasinfo", "-i", las_file, "-o", "temp_info.txt", "-odir", directory])
        with open(directory + "/temp_info.txt") as f:
            plot_id=filename[0:4]
            for x in f:
                if "GTCitationGeoKey" in x:
                    if "WGS 84" in x:
                        wgs = "84"
                    if "UTM zone 10N" in x:
                        utm = "10n"
                    if "UTM zone 11N" in x:
                        utm = "11n"
                with open(plot_reference_table, 'a') as ref:
                    ref_headers = ['plot_id', 'wgs', 'utm']
                    ref_row = [plot_id, wgs, utm]
                    writer = csv.DictWriter(ref, fieldnames=ref_headers)
                    writer.writeheader()
                    writer.writerow({'plot_id' : plot_id, 'wgs' : wgs, 'utm' : utm})
                ref.close()
        f.close()
    else:
        continue
