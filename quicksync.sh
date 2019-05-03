#!/bin/bash

# abort on error
set -e
set -x

# clone and build our repo
git clone -b QuickSyncAll https://github.com/NeblioTeam/neblio
cd neblio
python ci_scripts/test_linux-daemon.py

echo "Finished Building. Syncing blockchain data"
mkdir -p $HOME/.neblio

cat <<EOF > $HOME/.neblio/neblio.conf
rpcuser=${RPCUSER:-nebliorpc}
rpcpassword=${RPCPASSWORD:-rpctemp}
EOF

# start nebliod, which will kick off QuickSync
./wallet/nebliod -daemon=1

# sync the remainder of the chain
i=0
while true
do
    (( i = i + 1 ))
    REMOTE_COUNT=`wget -O - http://explorer.nebl.io/api/getblockcount 2>/dev/null`
    LOCAL_COUNT=`./wallet/nebliod getblockcount 2>&1 || true`
    echo "Syncing $LOCAL_COUNT \ $REMOTE_COUNT"
    if [ "$LOCAL_COUNT" -eq "$REMOTE_COUNT" ]; then
        break
    fi
    if [ "$i" -gt 60 ]; then
        # break after 30 minutes no matter what
        break
    fi
    sleep 30
done
sleep 10
./wallet/nebliod stop
sleep 10
rm $HOME/.neblio/neblio.conf
rm $HOME/.neblio/wallet.dat
# move our db files out for deployment
mv $HOME/.neblio/txlmdb $HOME/$TRAVIS_BUILD_DIR/