import os, json, hashlib, requests, subprocess, time, sys, glob

def restart_job():
    print('FAILURE. RESTARTING JOB.')

    if os.environ.get('TRAVIS_API_TOKEN') is not None:
        url = 'https://api.travis-ci.org/repo/NeblioTeam%2Fneblio-quicksync/requests'
        token = "token " + os.environ["TRAVIS_API_TOKEN"]
        h = {'Content-Type': 'application/json', 'Travis-API-Version': '3', 'Accept': 'application/json', 'Authorization': token}
        d = {}
        r = requests.post(url, data=d, headers=h)
    else:
        url = 'https://api.github.com/repos/NeblioTeam/neblio-quicksync/dispatches'
        token = "token " + os.environ["GITHUB_TOKEN"]
        h = {'Accept': 'application/vnd.github.everest-preview+json', 'Authorization': token}
        d = {"event_type": "restart_neblio_quicksync"}
        # r = requests.post(url, data=json.dumps(d), headers=h)


    print('Deploy Verification Failed. Killing This Job.')
    sys.exit(1)




print('Starting Deploy Verification. Sleeping 60s to let deploys finish.')
# If we are not using Travis we need to set up some env vars
if os.environ.get('TRAVIS_API_TOKEN') is None:
    os.environ['BUILD_DIR'] = os.environ.get('GITHUB_WORKSPACE')
    os.environ['COMMIT'] = os.environ.get('GITHUB_SHA')

time.sleep(60)
# calculate lock.mdb checksum
print('Calculating sha256sum for uploaded lock.mdb')
sha256_hash = hashlib.sha256()
with open(os.environ['BUILD_DIR'] + '/txlmdb/lock.mdb',"rb") as f:
    # Read and update hash string value in blocks of 4K
    for byte_block in iter(lambda: f.read(4096),b""):
        sha256_hash.update(byte_block)
lock_sha256 = sha256_hash.hexdigest()
print(lock_sha256)
os.remove(os.environ['BUILD_DIR'] + '/txlmdb/lock.mdb')

# calculate data.mdb checksum
print('Calculating sha256sum for uploaded data.mdb')
sha256_hash = hashlib.sha256()
with open(os.environ['BUILD_DIR'] + '/txlmdb/data.mdb',"rb") as f:
    # Read and update hash string value in blocks of 4K
    for byte_block in iter(lambda: f.read(4096),b""):
        sha256_hash.update(byte_block)
data_sha256 = sha256_hash.hexdigest()
print(data_sha256)
os.remove(os.environ['BUILD_DIR'] + '/txlmdb/data.mdb')

tmp_dir = 'tmp_download'
prefix = ''

if not os.path.exists(tmp_dir):
    # check first download
    prefix = "https://assets.nebl.io/quicksync/txlmdb/"
    os.mkdir(tmp_dir) # dir does not exist, create it
else:
    # check second download
    prefix = "https://assets.nebl.io/quicksync/txlmdb/"

os.chdir(tmp_dir)
downloaded_sha256 = ''
url1 = prefix + os.environ['COMMIT'] + "/data.mdb"
url2 = prefix + os.environ['COMMIT'] + "/lock.mdb"
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
    sha256_hash = hashlib.sha256()
    with open(os.environ['BUILD_DIR'] + '/' + tmp_dir + '/' + file_name, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    downloaded_sha256 = sha256_hash.hexdigest()
    # verify checksums
    if file_name == "data.mdb":
        if data_sha256 != downloaded_sha256:
            print('SHA256 did not match for data.mdb')
            print('Original SHA256: ' + data_sha256)
            print('Download SHA256: ' + downloaded_sha256)
            # RESTART JOB
            restart_job()
        else:
            # checksum valid
            print(file_name + " sha256sum is valid")
            print('Original SHA256: ' + data_sha256)
            print('Download SHA256: ' + downloaded_sha256)
            # move verified file to expected dir
            os.rename(os.environ['BUILD_DIR'] + '/' + tmp_dir + '/' + file_name, os.environ['BUILD_DIR'] + '/txlmdb/' + file_name)
    if file_name == "lock.mdb":
        if lock_sha256 != downloaded_sha256:
            print('SHA256 did not match for lock.mdb')
            print('Original SHA256: ' + lock_sha256)
            print('Download SHA256: ' + downloaded_sha256)
            # RESTART JOB
            restart_job()
        else:
            # checksum valid
            print(file_name + " sha256sum is valid")
            print('Original SHA256: ' + lock_sha256)
            print('Download SHA256: ' + downloaded_sha256)
            # move verified file to expected dir
            os.rename(os.environ['BUILD_DIR'] + '/' + tmp_dir + '/' + file_name, os.environ['BUILD_DIR'] + '/txlmdb/' + file_name)



