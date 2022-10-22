
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoClimb.settings')
django.setup()

import json 
from GoClimbApp.models import * 

def generateCragDestination():
  filename = 'cragData/destinations.json'
  file = open(filename)
  data = json.load(file)
  for i in data['destinations']:
    destination =  cragDestination(**i)
    destination.save()

def generateCragFace():
  # import faces 
  filename = 'cragData/faces.json'
  file = open(filename)
  data = json.load(file)
  for i in data['faces']: 
    for j in i['destinationFaces']:
      face = cragFace(**j, FKCragDestination=cragDestination.objects.get(name=i['destinationName']))
      face.save()

def generateCragRoute():
  # import routes 
  filename = 'cragData/routes.json'
  file = open(filename)
  data = json.load(file)
  for i in data['routes']: 
    for j in i['faceRoutes']:
      route = cragRoute(**j, FKCragFace=cragFace.objects.get(name=i['faceName']))
      route.save()

generateCragDestination()
generateCragFace()
generateCragRoute()    