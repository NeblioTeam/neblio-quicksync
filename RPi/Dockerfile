FROM neblioteam/nebliod-rpi
MAINTAINER Neblio <info@nebl.io>

RUN [ "cross-build-start" ]

ADD ./bin /usr/local/bin
RUN chmod 755 /usr/local/bin/neblio_quicksync_copy

VOLUME /root/.neblio

CMD ["neblio_quicksync_copy"]

RUN [ "cross-build-end" ]