import cv2
import numpy as np
import os
import subprocess
from decimal import Decimal

def findCircles(
    input_raster, output_raster, param1, param2, min_distance, min_rad, max_rad):
    image = cv2.imread(input_raster)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    output = image.copy()
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, min_distance,
              param1=param1,
              param2=param2,
              minRadius=min_rad,
              maxRadius=max_rad)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        info = getCoordinates(input_raster)
        addDetectedCircles(input_raster, output_raster, output, circles)
        realCircles(circles, output_raster, info[0], info[1], info[2])
        return circles
    else:
        return (-999)
        # replace this with an error code

def addDetectedCircles(input_raster, output_raster, output, circles):
    for(x, y, r) in circles:
        cv2.circle(output, (x, y), r, (0, 255, 0), 2)
        cv2.rectangle(output, (x, y), (x + 1, y + 1), (0, 128, 255), -1)
    cv2.imwrite(output_raster, output)

def getCoordinates(input_raster):
    p = subprocess.Popen(['gdalinfo', input_raster], stdout=subprocess.PIPE)
    info = str(p.communicate())
    parsed_info = info.split('\\n')
    for i in parsed_info:
        if 'Pixel Size' in i:
            pixel_res = i[14:31]
        if 'Upper Left' in i:
            lat = i[14:25]
            lon = i[28:38]
    return_info = [lat, lon, pixel_res]
    return return_info

def pixelToReal(lat, lon, pixel_res, pix_x, pix_y, rad):
    new_lat = float(lat) - (pix_y * float(pixel_res))
    '''
    test = float(lat)
    rounded_test = round(test, 3)
    print(lat)
    print(str(float(lat) + pix_x * float(pixel_res)))
    print(test)
    print(str(rounded_test))
    '''
    new_lon = float(lon) + (pix_x * float(pixel_res)) 
    new_rad = rad * float(pixel_res)
    new_line = [new_lon, new_lat, new_rad]
    return new_line

def realCircles(circles, output_raster, lat, lon, pixel_res):
    text_output = output_raster[:-4] + '.txt'
    with open(text_output, 'w') as f:
        f.write('lon, lat, r\n')
        for (x, y, r) in circles:
            new_line = pixelToReal(lon, lat, pixel_res, x, y, r)
            f.write(str(new_line[0]) + ',' + str(new_line[1]) + ',' + str(new_line[2]) + '\n')
            #f.write(str(x) + ',' + str(y) + ',' + str(r) + '\n')

input_directory = '/home/theo/Desktop/mensuration_rasters'
output_directory = '/home/theo/Desktop/hough_images'

# Find large circles
#circles = findCircles(input_raster, output_raster, param1=100, param2=20, min_distance=40, min_rad=40, max_rad=59)

for i in sorted(os.listdir(input_directory)):
    if i.endswith('.tif'):
        input_raster = input_directory + '/' + i
        output_raster = output_directory + '/small_' + i[0:3] + '.tif'
        # Find small circles
        findCircles(input_raster, output_raster, param1=100, param2=20, min_distance=5, min_rad=5, max_rad=19)

        output_raster = output_directory + '/medium_' + i[0:3] + '.tif'
        # Find medium circles
        findCircles(input_raster, output_raster, param1=100, param2=20, min_distance=20, min_rad=20, max_rad=39)

        output_raster = output_directory + '/large' + i[0:3] + '.tif'
        # Find large circles
        findCircles(input_raster, output_raster, param1=100, param2=20, min_distance=40, min_rad=40, max_rad=59)

        output_raster = output_directory + '/extra_large' + i[0:3] + '.tif'
        # Find extra large circles
        findCircles(input_raster, output_raster, param1=100, param2=20, min_distance=60, min_rad=60, max_rad=90)