# Neblio QuickSync

This repo constains docker files and scripts that run one or more times a day to generate a fully-synced copy of the Neblio blockchain. 

Newly installed versions of nebliod and neblio-Qt will check for links at this repo to the latest version of the QuickSync files.

You may also perform a manual QuickSync if automatic QuickSync is not working for you for some reason.

To perform a manual Quicksync, get the links from here for data.mdb and lock.mdb: https://github.com/NeblioTeam/neblio-quicksync/blob/master/download.json (the links change every day)

```
- Close nebliod/neblio-Qt
- Download one of the lock.mdb files and one of the data.mdb files from the download.json linked 
  above (choose links for the highest dbversion such as 75014, 75015, etc)
- Verify the sha256sum of the downloads (important!)
- Move both .mdb files to the txlmdb folder in the neblio data directory, overwriting 
  any that are already there.
- Open nebliod/neblio-Qt
```

If your wallet keeps trying to automaticly quicksync and you do not want it to, you can add noquicksync=1 to your neblio.conf
