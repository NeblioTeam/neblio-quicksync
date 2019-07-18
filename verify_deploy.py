import os, json, hashlib, requests, subprocess

def restart_job():
   print('SIMULATING JOB RESTART')
   subprocess.call("travis_terminate 1", shell=True)


sha256_hash = hashlib.sha256()
# calculate lock.mdb checksum
print('Calculating sha256sum for uploaded lock.mdb')
with open(os.environ['TRAVIS_BUILD_DIR'] + '/txlmdb/lock.mdb',"rb") as f:
    # Read and update hash string value in blocks of 4K
    for byte_block in iter(lambda: f.read(4096),b""):
        sha256_hash.update(byte_block)
lock_sha256 = sha256_hash.hexdigest()

# calculate data.mdb checksum
print('Calculating sha256sum for uploaded data.mdb')
with open(os.environ['TRAVIS_BUILD_DIR'] + '/txlmdb/data.mdb',"rb") as f:
    # Read and update hash string value in blocks of 4K
    for byte_block in iter(lambda: f.read(4096),b""):
        sha256_hash.update(byte_block)
data_sha256 = sha256_hash.hexdigest()

tmp_dir = 'tmp_download'
prefix = ''
if not os.path.exists(tmp_dir):
	# check first download
	prefix = "https://quicksync.ams3.digitaloceanspaces.com/txlmdb/"
	os.mkdir(tmp_dir) # dir does not exist, create it
else:
	# check second download
	prefix = "https://quicksync-backup.sfo2.digitaloceanspaces.com/txlmdb/"

os.chdir(tmp_dir)
downloaded_sha256 = ''
url1 = prefix + os.environ['TRAVIS_COMMIT'] + "/data.mdb"
url2 = prefix + os.environ['TRAVIS_COMMIT'] + "/lock.mdb"
# check if the above URLs exist
for url in [url1, url2]:
    check = requests.head(url)
    if check.status_code > 399:
    	# RESTART JOB
    	restart_job()
    # URL exists, download file
    print('Downloading URL to verify checksum: ' + url)
    file_name = url.rsplit('/', 1)[1]
    r = requests.get(url, allow_redirects=True)
    if r.status_code > 399:
    	# RESTART JOB
    	restart_job()
    open(file_name, 'wb').write(r.content)
    # verify checksum
    with open(os.environ['TRAVIS_BUILD_DIR'] + '/' + tmp_dir + '/' + file_name, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    downloaded_sha256 = sha256_hash.hexdigest()
    # verify checksums
    if file_name == "data.mdb":
    	if data_sha256 != downloaded_sha256:
    		# RESTART JOB
    		restart_job()
    	else:
    		# checksum valid
    		print(filename + " sha256sum is valid")
    		os.remove(filename)
    if file_name == "lock.mdb":
    	if lock_sha256 != downloaded_sha256:
    		# RESTART JOB
    		restart_job()
    	else:
    		# checksum valid
    		print(filename + " sha256sum is valid")
    		os.remove(filename)



