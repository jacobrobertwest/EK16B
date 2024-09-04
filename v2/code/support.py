from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map,delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map
            
def import_folder(path):
    surface_list = []
    for _,__,img_files in walk(path):
        for image in sorted(img_files):
            if image == '.DS_Store':
                pass
            else:
                full_path = path + '/' + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)
    return surface_list

def return_2pts_distance(point1,point2):
    x1,y1 = point1
    x2,y2 = point2
    return ((x2-x1)**2 + (y2-y1)**2)**0.5
