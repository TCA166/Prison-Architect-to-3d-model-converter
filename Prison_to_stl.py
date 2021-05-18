from voxelfuse.voxel_model import VoxelModel
from voxelfuse.mesh import Mesh
from voxelfuse.plot import Plot
from voxelfuse.primitives import *
from tqdm import tqdm
import voxelfuse
import re

#before we actually create the voxel we have to parse the savefile

def check_if_indoor_mat(mat):
    if 'Floor' in mat or 'Tiles' in mat or mat in ['Seluco','Carpet']:
        return True
    else:
        return False

filename = input('Input the name of the prison architect save file you want to convert to a voxel model (without .prison):')

file = open(filename + '.prison', "r")

filedata = file.read()

tiledata = re.findall(r'BEGIN Cells .+?\nEND', filedata, re.S)[0].replace('BEGIN Cells','').replace('\nEND','')

objectdata = re.findall(r'\nBEGIN Objects .+?\nEND', filedata, re.S)[0].replace('BEGIN Objects','').replace('\nEND','').split('\n')

datarows = tiledata.split('\n')

tiles = []

for item in datarows:
    if item != datarows[0]:
        item = item.replace('BEGIN','').replace('END','')
        coords = re.findall(r'".+?\"', item, re.S)[0].replace('"','').split(' ')
        try:
            material = re.findall(r'Mat.+?\ Con', item, re.S)[0].replace('Mat','').replace('Con','').replace(' ','')
        except:
            material = 'dirt'
        row = {'x':coords[0],'y':coords[1],'Mat':material,'Ind':'Ind' in item}
        tiles.append(row)

cubes = []

print('Savefile parsed...')
print('Tiles: ' + str(len(tiles)))

low = ['Road','RoadMarkings','RoadMarkingsLeft','RoadMarkingsRight']
high = ['BrickWall','ConcreteWall','Fence','PerimeterWall']

for i in tqdm (range(len(tiles)),desc="Creating 3d models…",ascii=False, ncols=75):
    tile = tiles[i]
    material = tile['Mat']
    if material in high or 'Wall' in material:
        cubes.append(cuboid((6,18,6),(int(tile['x'])*6,2,int(tile['y'])*6),1,10))
    elif material in low:
        cubes.append(cuboid((6,1,6),(int(tile['x'])*6,2,int(tile['y'])*6),1,10))
    else:
        cubes.append(cuboid((6,3,6),(int(tile['x'])*6,2,int(tile['y'])*6),1,10))
    if tile['Ind'] and check_if_indoor_mat(material):
        cubes.append(cuboid((6,2,6),(int(tile['x'])*6,18,int(tile['y'])*6),1,10))
    

#for object_ in objectdata:



finalmodel = cubes[0]

for i in tqdm (range(len(cubes)),desc="Merging 3d models… ",ascii=False, ncols=75):
    cube = cubes[i]
    if cube != cubes[0]:
        finalmodel = finalmodel.union(cube)         

mesh1 = Mesh.fromVoxelModel(finalmodel)
mesh1.export(filename + '.stl')
