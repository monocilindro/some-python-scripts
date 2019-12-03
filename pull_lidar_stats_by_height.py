import os
import subprocess
import csv

# add positional arguments
# modify text parsing to account for empty height slices

directory = '/home/theo/Desktop/ferguson/height_normalized/prefire_als_height_norm'
plot_reference_table = '/home/theo/Desktop/height_plot_stats.csv'
for filename in os.listdir(directory):
    if filename.endswith(".las"):
        i = 0
        while i < 100:
            j = i + 2
            las_file = directory + '/' + filename
            subprocess.call(["lasinfo", "-i", las_file, "-o", "temp_info.txt", "-odir", directory, "-compute_density", "-keep_z", str(i), str(j)])
            with open(directory + "/temp_info.txt") as f:
                plot_id=filename[0:4]
                if 'E1' in filename:
                    plot_id=plot_id + 'E1'
                if 'E2' in filename:
                    plot_id=plot_id + 'E2'
                for x in f:
                    if "number of point records:" in x:
                        total_points = x
                    if "ground" in x:
                        ground_points = x
                    if "vegetation" in x:
                        vegetation_points = x
                    if 'point density:' in x:
                        density = x
                with open(plot_reference_table, 'a') as ref:
                    ref_headers = ['plot_id', 'total_points', 'ground_points', 'vegetation_points', 'density', 'lower_bound', 'upper_bound']
                    ref_row = [plot_id, total_points, ground_points, vegetation_points, i, j]
                    writer = csv.DictWriter(ref, fieldnames=ref_headers)
                    writer.writerow({'plot_id' : plot_id, 'plot_id' : plot_id, 'total_points' : total_points, 'ground_points' : ground_points, 'vegetation_points' : vegetation_points, 'density' : density, 'lower_bound' : i, 'upper_bound' : j})
                i = j
                ref.close()
            f.close()
    else:
        continue
