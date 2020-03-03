import os

def divide_inputs(input_folder, ending=".las", num_cpus=32):
    inputs = []
    for filename in os.listdir(input_folder):
        if filename.endswith(ending):
            input_path = input_folder + "/" + filename
            inputs.append(input_path)
    chunk_size = round(len(inputs)/num_cpus)
    for i in range(num_cpus):
        chunk_file = temp_directory + "/input_" + str(i) + ".txt"
        chunks = []
        for j in range(chunk_size):
            chunks.append(inputs.pop())
        with open(chunk_file, 'w') as f:
            for line in chunks:
                f.write(line + "\n")
        f.close()

