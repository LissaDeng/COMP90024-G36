import sys
import time
import couchdb
import threading
import mpi4py.MPI as MPI
from harvesterInfo import HarvesterInfo
from searchAPI import SearchAPI
from streamAPI import StreamAPI

comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()

try:
	# The user is expected to tell which processor should be run
	if rank == 0:
	    harvester_id = int(sys.argv[1])
	else:
		harvester_id = 5-int(sys.argv[1])
		time.sleep(1)

	    
	#max for search
	try:
	    maxTweetsForSearch = int(sys.argv[2])
	except Exception:
	    maxTweetsForSearch = 10000000 # Some arbitrary large number

	#max for stream
	try:
	    maxTweetsForStream = int(sys.argv[3])
	except Exception:
	    maxTweetsForStream = 10000000 # Some arbitrary large number

	#If user inputs a valid since_id, pass it to searchAPIHarvester
	#try:
	#    sinceId = int(sys.argv[4])
	#except Exception:
	sinceId = None

	couchdb_server = couchdb.Server('http://g36:1q2w3e@127.0.0.1:5984/')
	if "tweets" in couchdb_server:
		couchdb_database = couchdb_server['tweets']  #couchdb-db-name
	else:
		couchdb_database = couchdb_server.create('tweets')

	info = HarvesterInfo()
	print(info.api[harvester_id],info.search_loc_str[harvester_id],info.stream_loc[harvester_id])
	thread_searchAPI = SearchAPI(info.api[harvester_id], info.search_loc_str[harvester_id], harvester_id, couchdb_database, sinceId, maxTweetsForSearch)
	thread_streamAPI = StreamAPI(info.api[harvester_id], info.stream_loc[harvester_id], harvester_id, couchdb_database, maxTweetsForStream)

	thread_searchAPI.start()
	thread_streamAPI.start()

#except IndexError:
#	print('Harvester ID should be given')
except Exception as e:
	print(str(e))
