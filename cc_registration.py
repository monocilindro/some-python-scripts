import os
import shutil
import subprocess

def register_tls_to_als(tls, als):
    subprocess.call(['cloudcompare.CloudCompare', '-SILENT', '-C_EXPORT_FMT', 'LAS', '-O', tls, '-O', als, '-ICP', '-MIN_ERROR_DIFF', '1e-8', '-RANDOM_SAMPLING_LIMIT', '100000'])

def apply_reg_matrix(lasfile, matrix):
    subprocess.call(['cloudcompare.CloudCompare', '-O', lasfile, '-APPLY_TRANS', matrix])

tls_directory = '/home/theo/Desktop/clipped_walker_tls'
als_directory = '/home/theo/Desktop/walker_als_plots'
output_las_directory = '/home/theo/Desktop/registered_walker/las'
output_txt_directory = '/home/theo/Desktop/registered_walker/txt'

if not os.path.exists(output_las_directory):
    os.makedirs(output_las_directory)
if not os.path.exists(output_txt_directory):
    os.makedirs(output_txt_directory)


# Create registration matrix using clipped files
for i in os.listdir(tls_directory):
    if i.endswith('.las'): # 'pre' in i 
        plot_id=i[3:6]
        tls = tls_directory + '/' + i
        for j in os.listdir(als_directory):
            if plot_id in j and j.endswith('.las'):
                als = als_directory + '/' + j
                register_tls_to_als(tls, als)
    
        for k in os.listdir(tls_directory):
            if '_REGISTERED' in k and k.endswith('.las'):
                old_file = tls_directory + '/' + k
                new_file = output_las_directory + '/' + i[:-4] + '_v004.las'
                shutil.move(old_file, new_file)
            if '_REGISTRATION' in k and k.endswith('.txt'):
                old_file = tls_directory + '/' + k
                new_file = output_txt_directory + '/' + i[:-4] + '_sop.txt'
                shutil.move(old_file, new_file)


for i in os.listdir(output_txt_directory):
    if i.endswith('.txt'):
        plot = i[:-7] + '.las'
        print(plot)
        #matrix = output_txt_directory + '/' + i
        #apply_reg_matrix(plot, i)
        
