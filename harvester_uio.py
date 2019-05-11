# -*- coding: utf-8 -*-
#import couchdb
import sys
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import os 
import pymongo

##########DICCIONARIO API KEYS ######
## Crear un diccionario de las API KYES desde un archivo, dicho archivo estara en el gitignore

# Comprobar que el archivo con credenciales exista
api_keys = sys.argv[1]
if not os.path.isfile(api_keys):
    print ("Falta el archivo de Keys")
    sys.exit()

keys = {}
with open (api_keys) as fApis:
    cont = 0
    for line in fApis:
        keys[cont] = line.replace("\n","")
        cont = cont + 1

print (keys)


##########API CREDENTIALS ############   
#Colocar credenciales del API de dev de Twitter
ckey = keys[0]
csecret = keys[1]
atoken = keys[2]
asecret = keys[3]


######### MONGO DB #################
# CREAR LA BASE EN MONGO ###########
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["tweetsEcuadorQuito"]
mycol = mydb["tweets"]


class listener(StreamListener):
    print ("Dentro de listener")
 
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
             dictTweet["_id"] = str(dictTweet['id'])
             mycol.insert(dictTweet)
             print (dictTweet)
        except:
            print "Already exists"
            pass
        return True
 
    def on_error(self, status):
        print status
 
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
 
'''===============LOCATIONS=============='''
twitterStream.filter(locations=[-78.593445,-0.370099,-78.386078,-0.081711])  #Coordenadas QUITO 
print(twitterStream )

#Colocar este archivo en el escritorio de la máquina, ejecutarlo mediante el comando: 
#python harvester_uio.py localhost nombredebasededatos
