import couchdb
import json

server = couchdb.Server("http://g36:1q2w3e@127.0.0.1:5984")
db = server["tweets"]

with open("designDocForTweets.json") as file_object:
	db["_design/analysis"] = json.load(file_object)


db = server["aurin"]
with open("designDocForAurin.json") as file_object:
	db["_design/analysis"] = json.load(file_object)
