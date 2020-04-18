import os, json, uuid, hashlib, glob


# set up env vars if we are in github actions
if os.environ.get('TRAVIS_API_TOKEN') is None:
	os.environ['COMMIT'] = os.environ.get('GITHUB_SHA')
	os.environ['BUILD_DIR'] = os.environ['GITHUB_WORKSPACE']

filename = 'download.json'
# get the number of chunks from our previously created file
chunkCount = glob.glob(os.environ['BUILD_DIR'] + '/txlmdb/chunks.*')[0].split('chunks.')[1]
parts = '/parts=' + str(chunkCount-1)
with open(filename, 'r') as f:
    data = json.load(f)
    # sort the array in ascending order by dbversion, then only modify the last element in the array
    data.sort(key=lambda x: x['dbversion'], reverse=False)
    data_urls = []
    # data_urls.append("https://quicksync.nebl.io/txlmdb/" + os.environ['COMMIT'] + "/data.mdb" + suffix)
    data_urls.append("https://assets.nebl.io/txlmdb/" + os.environ['COMMIT'] + parts + "/data.mdb")
    data[-1]['files'][1]['url'] = data_urls
    data[-1]['files'][1]['size'] =  os.path.getsize(os.environ['BUILD_DIR'] + '/txlmdb/data.mdb')
    sha256_hash = hashlib.sha256()
    with open(os.environ['BUILD_DIR'] + '/txlmdb/data.mdb',"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    data[-1]['files'][1]['sha256sum'] = sha256_hash.hexdigest()

    lock_urls = []
    # lock_urls.append("https://quicksync.nebl.io/txlmdb/" + os.environ['COMMIT'] + "/lock.mdb")
    lock_urls.append("https://assets.nebl.io/txlmdb/" + os.environ['COMMIT'] + "/lock.mdb")
    data[-1]['files'][0]['url'] = lock_urls
    data[-1]['files'][0]['size'] =  os.path.getsize(os.environ['BUILD_DIR'] + '/txlmdb/lock.mdb')
    sha256_hash = hashlib.sha256()
    with open(os.environ['BUILD_DIR'] + '/txlmdb/lock.mdb',"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    data[-1]['files'][0]['sha256sum'] = sha256_hash.hexdigest()

print("Writing the following to download.json")
print(json.dumps(data, indent=2))

# create randomly named temporary file to avoid
# interference with other thread/asynchronous request
tempfile = os.path.join(os.path.dirname(filename), str(uuid.uuid4()))
with open(tempfile, 'w') as f:
    json.dump(data, f, indent=2)

# rename temporary file replacing old file
os.rename(tempfile, filename)
