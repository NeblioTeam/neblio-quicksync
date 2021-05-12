import os, json, uuid, hashlib, glob


# set up env vars if we are in github actions
if os.environ.get('TRAVIS_API_TOKEN') is None:
	os.environ['COMMIT'] = os.environ.get('GITHUB_SHA')
	os.environ['BUILD_DIR'] = os.environ['GITHUB_WORKSPACE']


filename = 'download.json'

with open(filename, 'r') as f:
    data = json.load(f)
    # sort the array in ascending order by dbversion, then find the index for our target version
    data.sort(key=lambda x: x['dbversion'], reverse=False)
    index = None
    for x in data:
    	if x['dbversion'] == int(os.environ['DB_VER']):
    		print("Found DB Version")
    		index = data.index(x)
    		print(index)
    		break
    	else:
    		print("DB Version Miss")

    data_urls = []
    data_urls.append("https://assets.nebl.io/quicksync/txlmdb-" + os.environ['DB_VER'] + "/" + os.environ['COMMIT'] + "/data.mdb")
    data[index]['files'][1]['url'] = data_urls
    data[index]['files'][1]['size'] =  os.path.getsize(os.environ['BUILD_DIR'] + '/txlmdb/data.mdb')
    sha256_hash = hashlib.sha256()
    with open(os.environ['BUILD_DIR'] + '/txlmdb/data.mdb',"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    data[index]['files'][1]['sha256sum'] = sha256_hash.hexdigest()

    lock_urls = []
    lock_urls.append("https://assets.nebl.io/quicksync/txlmdb-" + os.environ['DB_VER'] + "/" + os.environ['COMMIT'] + "/lock.mdb")
    data[index]['files'][0]['url'] = lock_urls
    data[index]['files'][0]['size'] =  os.path.getsize(os.environ['BUILD_DIR'] + '/txlmdb/lock.mdb')
    sha256_hash = hashlib.sha256()
    with open(os.environ['BUILD_DIR'] + '/txlmdb/lock.mdb',"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    data[index]['files'][0]['sha256sum'] = sha256_hash.hexdigest()

print("Writing the following to download.json")
print(json.dumps(data, indent=2))

# create randomly named temporary file to avoid
# interference with other thread/asynchronous request
tempfile = os.path.join(os.path.dirname(filename), str(uuid.uuid4()))
with open(tempfile, 'w') as f:
    json.dump(data, f, indent=2)

# rename temporary file replacing old file
os.rename(tempfile, filename)
