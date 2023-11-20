import numpy as np
from scipy.spatial import cKDTree
import time
start_time = time.time()
#

class_index = 9
def read_dane(filepath):
    X, Y = [], []
    first_line = []
    with open(filepath, 'r') as f:
        lines = f.readlines()
        first_line_tokens = lines[0].strip().split(' ')
        first_line = np.asarray(first_line_tokens, dtype=np.str)
        for line in lines[1:]:
            tokens = line.strip().split(' ')
            if 'nan' not in tokens:
                x_values = [float(t) for t_index, t in enumerate(tokens)]
                x_values[class_index] = float(tokens[class_index])
                X.append(x_values)
                Y.append(int(float(tokens[class_index])))
    return np.asarray(X, dtype=np.float64), np.asarray(Y, dtype=np.float64), first_line


def calculate_deltalocal(point_cloud, radius):
    x = point_cloud[:, :2]
    y = point_cloud[:, 2] # Wczytaj tylko współrzędne XYZ
    tree = cKDTree(x)
    deltalocal = []
    i = 0
    for point in x:
        index = tree.query_ball_point(point, radius)
        Y_in = y[index]
        Ysr = Y_in.mean()
        delta = Ysr - y[i]
        deltalocal.append(delta)
        i=i+1
        if i % 100000 == 0:
            print(str(i) + ' iteracja (deltaHeight)')
    deltalocal = np.array(deltalocal)
    return deltalocal

# Iteracja po punktach
def calculate_intensities(point_cloud, cube_size):
    points = point_cloud[:, :3]  # Wczytaj tylko współrzędne XYZ
    intensities = point_cloud[:, 6]  # Wczytaj wartości intensywności
    
    tree = cKDTree(points)  # Tworzenie drzewa kd dla szybkiego wyszukiwania najbliższych punktów

    imins = []
    imeans = []
    imaxes = []
    intensityRange = []
    
    i = 0

    for point in points:
        # Znajdź indeksy punktów wewnątrz sześcianu o zadanym rozmiarze
        indices = query_cube_points(tree, point, cube_size)

        # Pobierz intensywności punktów wewnątrz sześcianu
        cube_intensities = intensities[indices]

        # Oblicz cechy geometryczne
        imin = np.min(cube_intensities)
        imean = np.mean(cube_intensities)
        imax = np.max(cube_intensities)
        irange = np.ptp(cube_intensities)

        # Dodaj wartości cech do listy
        imins.append(imin)
        imeans.append(imean)
        imaxes.append(imax)
        intensityRange.append(irange)
        
        i=i+1
        if i % 100000 == 0:
            print(str(i) + ' iteracja (intensities)')
            
    # Zamień listy na tablicę numpy
    imins = np.array(imins)
    imeans = np.array(imeans)
    imaxes = np.array(imaxes)
    intensityRange = np.array(intensityRange)

    return imins, imeans, imaxes, intensityRange

def query_cube_points(tree, point, cube_size):
    x, y, z = point
    x_min, x_max = x - cube_size/2, x + cube_size/2
    y_min, y_max = y - cube_size/2, y + cube_size/2
    z_min, z_max = z - cube_size/2, z + cube_size/2

    indices = tree.query_ball_point(point, cube_size)
    indices = [idx for idx in indices if
               x_min <= point_cloud[idx, 0] <= x_max and
               y_min <= point_cloud[idx, 1] <= y_max and
               z_min <= point_cloud[idx, 2] <= z_max]
    return indices

def calculate_rgb(point_cloud):
    rgb = point_cloud[:,3:6]
    vdvi, vvi= [], []
    r_zero, g_zero, b_zero, w = 40, 60, 10, 1
    i = 0
    for cl in rgb:
        current_vdvi = (2 * cl[1] - cl[0] - cl[2])/(2 * cl[1] + cl[0] + cl[2])
        vdvi.append(current_vdvi)
        
        current_vvi = (abs((1-((cl[0]-r_zero)/(cl[0]+r_zero))) * (1-((cl[1]-g_zero)/(cl[1]+g_zero))) * (1-((cl[2]-b_zero)/(cl[2]+b_zero)))))**(1/w)
        vvi.append(current_vvi)
        
        i=i+1
        if i % 100000 == 0:
            print(str(i) + ' iteracja (RGB)')
            
    vdvi = np.array(vdvi)
    vvi = np.array(vvi)
    
    return vdvi, vvi
    

file_path = 'u_cub.txt'
filepath = 'D:\\MAGIST\\final\\u_rad.txt'
point_cloudraw = read_dane(filepath)
point_cloud = point_cloudraw[0]
#%%
# Obliczanie deltaLocal
d = calculate_deltalocal(point_cloud, 2.5)

#%%
a = (len(point_cloud),1)
point_cloud2 = np.c_[point_cloud, np.ones(a)]

for i in range(len(point_cloud)):
    point_cloud2[i][27] = d[i]


head = point_cloudraw[2]
head_l = head.tolist()
loc = ['deltaLocal']
head_l+= loc
#%%
# Obliczanie intensities

imins, imeans, imaxes, intensityRange = calculate_intensities(point_cloud, 2)

a = (len(point_cloud),4)
point_cloud2 = np.c_[point_cloud2, np.ones(a)]


for i in range(len(point_cloud)):
    point_cloud2[i][28] = imins[i]
    point_cloud2[i][29] = imeans[i]
    point_cloud2[i][30] = imaxes[i]
    point_cloud2[i][31] = intensityRange[i]

print('Intensity obliczono')

intens = ['iminis', 'imeans', 'imaxes', 'intensityRange']
head_l+= intens

# Obliczanie wskaznikow
vdvi, vvi = calculate_rgb(point_cloud)

a = (len(point_cloud),2)
point_cloud2 = np.c_[point_cloud2, np.ones(a)]

for i in range(len(point_cloud)):
    point_cloud2[i][32] = vdvi[i]
    point_cloud2[i][33] = vvi[i]

vvv = ['VDVI', 'VVI']
head_l += vvv


print('Combined')
combined_list = [dict(zip(head_l, row)) for row in point_cloud2]

print('Zaczynam eksportowac plik')
with open(file_path, 'w') as file:
    # Nagłówki kolumn
    headers = ' '.join(combined_list[0].keys())
    file.write(headers + '\n')
    i = 1
    # Wartości
    for item in combined_list:
        i = i+1
        line = ' '.join(str(value) for value in item.values())
        file.write(line + '\n')
        if i%1000000 == 0:
            print('Zapisano {} punktów'.format(str(i)))
print('Plik zapsiano')
#%%