import json
from os import path
import boto3

def load(file):
    if path.exists(file):
        j_file = open(file,'r')
        raw = j_file.read()
        j_file.close()
        try:
          playload =  json.loads(raw)
        except ValueError as error:
           print("Problema para carregar arquivo {0}: {1}".format(file,error))
           playload = {}
    else:
       playload = {}
    return playload

def getTags():
    tags = {}
    ssm = boto3.client('ssm')
    try:
      params = ssm.get_parameters_by_path(Path='/tags')
      tags = params['Parameters']
    except ValueError as error:
      print("Problema ao carregar Tags do SSM {0}".format(error))
    return tags

def addTags(playload):
    tags = getTags()
    playTags = {}
    for tag in tags:
        playTags[tag['Name']] = tag['Value']

    playload['Tags'] = playTags

    return playload
def savefile(file,playload):
    try:
      j_file = open(file,'w')
      j_file.write(json.dumps(playload))
      print(json.dumps(playload))
      j_file.close()
      return True
    except ValueError as error:
      print("Problema para salvar arquivo {0}: {1}".format(file,error))
      return False


if __name__ == '__main__':
    files = [
        'infra/parameters-dev.json',
        'infra/parameters-hom.json',
        'infra/parameters-prod.json'
    ]

    for file in files:
        playload_temp = load(file)
        playload = addTags(playload_temp)
        print(playload)
        if not savefile(file,playload):
            exit(1)

    exit(0)