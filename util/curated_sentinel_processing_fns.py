import json
import math
import sys
from PIL import Image
import numpy as np
import os

def my_distance(point_2, point_1):
    return (((point_2[0]-point_1[0])**2)+((point_2[1]-point_2[1])**2))**0.5

def distance_between_geojson(path):
    with open(path) as f:
        obj = json.load(f)
    points_list = obj['coordinates'][0]
    print(points_list)

def distance_lat_long(lat1, lon1, lat2, lon2):
    R = 6378.137 # Radius of earth in KM
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000; # meters


if __name__ == "__main__":
    if sys.argv[1] == 'once':
            
        coordinates_path = sys.argv[1]
        image_path = sys.argv[2]

        with open(coordinates_path, 'r') as f:
            points = json.load(f)['features'][0]['geometry']['coordinates'][0]
    
        distances = []

        for i in range(len(points)):
            if i + 1 < len(points):
                print(distance_lat_long(float(points[i][1]), float(points[i][0]), float(points[i+1][1]), float(points[i+1][0])))
                distances.append(distance_lat_long(float(points[i][1]), float(points[i][0]), float(points[i+1][1]), float(points[i+1][0])))
        print(f'length of points: {len(points)}')
        # distance_between_geojson('/Users/jacobriviere/Desktop/Personal_Projects/Onera Satellite Change Detection dataset - Images/aguasclaras/aguasclaras.geojson')

        # read in image and determine resolution in meters
        image_arr_sh = np.array(Image.open(image_path)).shape[:-1]
        if len(image_arr_sh) == 3:
            if image_arr_sh[0] <= 3:
                image_arr_sh = image_arr_sh[1:]
            elif image_arr_sh[-1] <= 3:
                image_arr_sh = image_arr_sh[:-1]

        width_m = min(distances)/min(image_arr_sh)
        length_m = max(distances)/max(image_arr_sh)
        print(f'this image is {length_m}m x {width_m}m')

    
    data_dir = sys.argv[1]
    geojson_dir = sys.argv[2]
    for inner in os.listdir(data_dir):
        if inner[-4:] != '.txt' and inner != '.DS_Store':
            print(inner)
            coordinates_path = geojson_dir+'/'+inner[:-4]+'.geojson'
            image_path = data_dir+'/'+inner

            with open(coordinates_path, 'r') as f:
                points = json.load(f)['coordinates'][0]

            distances = []

            for i in range(len(points)):
                if i + 1 < len(points):
                    print(distance_lat_long(float(points[i][1]), float(points[i][0]), float(points[i+1][1]), float(points[i+1][0])))
                    distances.append(distance_lat_long(float(points[i][1]), float(points[i][0]), float(points[i+1][1]), float(points[i+1][0])))
            print(f'length of points: {len(points)}')
            # distance_between_geojson('/Users/jacobriviere/Desktop/Personal_Projects/Onera Satellite Change Detection dataset - Images/aguasclaras/aguasclaras.geojson')

            # read in image and determine resolution in meters
            image_arr_sh = np.array(Image.open(image_path)).shape[:-1]
            print(f'image shape in pixels: {image_arr_sh}')
            if len(image_arr_sh) == 3:
                if image_arr_sh[0] <= 3:
                    image_arr_sh = image_arr_sh[1:]
                elif image_arr_sh[-1] <= 3:
                    image_arr_sh = image_arr_sh[:-1]
          
            width_m = min(distances)/min(image_arr_sh)
            length_m = max(distances)/max(image_arr_sh)
            print(f'this image is {length_m}m x {width_m}m')





