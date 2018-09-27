FROM neblioteam/nebliod
MAINTAINER Neblio <info@nebl.io>

ADD ./bin /usr/local/bin
RUN chmod 755 /usr/local/bin/neblio_quicksync_copy

VOLUME /root/.neblio

CMD ["neblio_quicksync_copy"]