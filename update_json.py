import os, json, uuid, hashlib

filename = 'download.json'
with open(filename, 'r') as f:
    data = json.load(f)
    data.sort(key=lambda x: x['dbversion'], reverse=True)
    data_urls = []
    data_urls.append("https://quicksync.ams3.digitaloceanspaces.com/txlmdb/" + os.environ['TRAVIS_COMMIT'] + "/data.mdb")
    data_urls.append("https://quicksync-backup.sfo2.digitaloceanspaces.com/txlmdb/" + os.environ['TRAVIS_COMMIT'] + "/data.mdb")
    data[0]['files'][0]['url'] = data_urls
    data[0]['files'][0]['size'] =  os.path.getsize(os.environ['TRAVIS_BUILD_DIR'] + '/txlmdb/data.mdb')
    sha256_hash = hashlib.sha256()
    with open(os.environ['TRAVIS_BUILD_DIR'] + '/txlmdb/data.mdb',"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    data[0]['files'][0]['sha256sum'] = sha256_hash.hexdigest()

    lock_urls = []
    lock_urls.append("https://quicksync.ams3.digitaloceanspaces.com/txlmdb/" + os.environ['TRAVIS_COMMIT'] + "/lock.mdb")
    lock_urls.append("https://quicksync-backup.sfo2.digitaloceanspaces.com/txlmdb/" + os.environ['TRAVIS_COMMIT'] + "/lock.mdb")
    data[0]['files'][1]['url'] = lock_urls
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