# Neblio QuickSync

This docker container copies a fully-synced copy of the Neblio blockchain to the appropriate directory on your Windows, Mac, Linux or Raspberry Pi system. This container brings Neblio QuickSync to any system running neblio-Qt or nebliod.

This container does not run nebliod nor nebliod-Qt in docker, it simply provides nebliod or neblio-Qt already running on your system with a fully-synced copy of the Neblio Blockchain.

## Prerequisites
- [Install Docker](https://store.docker.com/search?offering=community&type=edition)

## Instructions
- Always back up your wallet.
- Close neblio-Qt or nebliod if it is running
- Run one of the following commands, depending on your Operating System. The only difference between these commands is the folder that the blockchain gets copied to.
- Restart neblio-Qt or nebliod and your blockchain will be synced

Windows:

```docker run -i --rm --name neblio-quicksync -v $APPDATA/neblio:/root/.neblio neblioteam/neblio-quicksync```

Mac:

```sudo docker run -i --rm --name neblio-quicksync -v $HOME/Library/Application\ Support/neblio:/root/.neblio neblioteam/neblio-quicksync```

Linux:

```sudo docker run -i --rm --name neblio-quicksync -v $HOME/.neblio:/root/.neblio neblioteam/neblio-quicksync```

RaspberryPi:

```sudo docker run -i --rm --name neblio-quicksync -v $HOME/.neblio:/root/.neblio neblioteam/neblio-quicksync-rpi```