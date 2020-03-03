import os

def create_input_txt(input_directory, ending=".las"):
    
    with open(input_directory + "/blast2dem_input.txt", 'w') as f:
        for filename in os.listdir(input_directory):
            if filename.endswith(".las"):
                las_file = input_directory + "/" + filename
                f.write(las_file + "\n")
        f.close()
