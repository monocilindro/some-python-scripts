from multiprocessing import Pool, Process, Queue
from flightlines_to_tiles import flightlines_to_tiles
from tile_processing import tile_processing

def flight_queue(q, input_directory, lastools_singularity, overwrite = False):
    while not q.empty():
        try:
            las_file = q.get()
            flightlines_to_tiles(las_file, input_directory, lastools_singularity)
        except ValueError as val_error:
            print(val_error)
        except Exception as error:
            print(error)


# -------------------

def tile_queue(q, input_directory, output_directory, lastools_singularity, overwrite = False):
    while not q.empty():
        try:
            las_file = q.get()
            tile_processing(las_file, input_directory, output_directory, lastools_singularity)
        except ValueError as val_error:
            print(val_error)
        except Exception as error:
            print(error)
