FROM resin/armv7hf-debian:stretch
MAINTAINER Neblio <info@nebl.io>

RUN [ "cross-build-start" ]

COPY --from=neblioteam/nebliod-testnet-rpi:latest /root/.neblio.bootstrapped /root/.neblio.bootstrapped

ADD ./bin /usr/local/bin
RUN chmod 755 /usr/local/bin/neblio_quicksync_copy

VOLUME /root/.neblio

CMD ["neblio_quicksync_copy"]

RUN [ "cross-build-end" ]