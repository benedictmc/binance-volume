from pymongo import MongoClient
import socket

local_ip_address = socket.gethostbyname(socket.gethostname())

# Not sure if necessary
if local_ip_address != '192.168.0.227':
    ip_address = '192.168.0.227'
else:
    ip_address = 'localhost'

db = MongoClient(ip_address, 27017)
