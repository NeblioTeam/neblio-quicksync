import os, json, uuid, hashlib

filename = 'download.json'
with open(filename, 'r') as f:
    data = json.load(f)
    data[0]['files'][0]['url'] = "https://quicksync.ams3.digitaloceanspaces.com/txlmdb/data.mdb"
    data[0]['files'][0]['size'] =  os.path.getsize(os.environ['TRAVIS_BUILD_DIR'] + '/txlmdb/data.mdb')
    sha256_hash = hashlib.sha256()
    with open(os.environ['TRAVIS_BUILD_DIR'] + '/txlmdb/data.mdb',"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    data[0]['files'][0]['sha256sum'] = sha256_hash.hexdigest()

    data[0]['files'][1]['url'] = "https://quicksync.ams3.digitaloceanspaces.com/txlmdb/lock.mdb"
    data[0]['files'][1]['size'] =  os.path.getsize(os.environ['TRAVIS_BUILD_DIR'] + '/txlmdb/lock.mdb')
    sha256_hash = hashlib.sha256()
    with open(os.environ['TRAVIS_BUILD_DIR'] + '/txlmdb/lock.mdb',"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    data[0]['files'][1]['sha256sum'] = sha256_hash.hexdigest()

print("Writing the following to download.json")
print(json.dumps(data, indent=2))

# create randomly named temporary file to avoid
# interference with other thread/asynchronous request
tempfile = os.path.join(os.path.dirname(filename), str(uuid.uuid4()))
with open(tempfile, 'w') as f:
    json.dump(data, f, indent=2)

# rename temporary file replacing old file
os.rename(tempfile, filename)