import os
import subprocess
import csv

directory = '/home/theo/Desktop/classified_tls/2018/prefire/ferguson'
plot_reference_table = '/home/theo/Desktop/plot_stats.csv'
for filename in os.listdir(directory):
    if filename.endswith(".las"):
        las_file = directory + '/' + filename
        subprocess.call(["lasinfo", "-i", las_file, "-o", "temp_info.txt", "-odir", directory])
        with open(directory + "/temp_info.txt") as f:
            plot_id=filename[0:4]
            for x in f:
                if "number of point records:" in x:
                    total_points = x
                if "ground" in x:
                    ground_points = x
                if "vegetation" in x:
                    vegetation_points = x
            with open(plot_reference_table, 'a') as ref:
                ref_headers = ['plot_id', 'total_points', 'ground_points', 'vegetation_points']
                ref_row = [plot_id, total_points, ground_points, vegetation_points]
                writer = csv.DictWriter(ref, fieldnames=ref_headers)
                writer.writerow({'plot_id' : plot_id, 'plot_id' : plot_id, 'total_points' : total_points, 'ground_points' : ground_points, 'vegetation_points' : vegetation_points})
            ref.close()
        f.close()
    else:
        continue
