import json 
from django.db import models
from .models import * 


def generateModels():
  # import routes 
  filename = 'cragData/routes.json'
  file = open(filename)
  data = json.load(file)
  data = data['routes']
  route_models = []
  for i in range(len(data)): 
    cragRoute.create(data[i])
    # id = data[i]['id']
    # name = data[i]['name']
    # grade = data[i]['grade']
    # description = data[i]['description']
    # bolts = data[i]['bolts']
    # rating = data[i]['rating']
    # length = data[i]['length']
    # ascents = data[i]['ascents']
    # first_ascent = data[i]['first_ascent']
    # CragData.create({'id':id, 'name':name, 'grade':grade, 'description':description, 'bolts':bolts, 'rating':rating, 'length':length, 'ascents':ascents,'first_ascednt':first_ascent})


  # import faces 
  filename = 'cragData/faces.json'
  file = open(filename)
  data = json.load(file)
  data = data['faces']
  route_models = []
  for i in range(len(data)): 
    cragFaces.create(data[i])
    # id = data[i]['id']
    # name = data[i]['name']
    # locationX = data[i]['locationX']
    # locationY = data[i]['locationY']
    # description = data[i]['description']
    # access = data[i]['access']
    # approach = data[i]['approach']
    
    # cragFace.create({'id':id, 'name':name, 'locationX':locationX, 'locationY':locationY, 'description':description, 'access':access, 'approach':approach})

    
  # import destinations: 
  filename = 'cragData/destinations.json'
  file = open(filename)
  data = json.load(file)
  data = data['destinations']
  route_models = []
  for i in range(len(data)): 
    cragDestination.create(data[i])
    # id = data[i]['id']
    # name = data[i]['name']
    # description = data[i]['description']
    # access = data[i]['access']
    # approach = data[i]['approach']
    # history = data[i]['history']
    # cragDestination.create({'id':id, 'name':name, 'locationX':locationX, 'locationY':locationY, 'description':description, 'access':access, 'approach':approach})
