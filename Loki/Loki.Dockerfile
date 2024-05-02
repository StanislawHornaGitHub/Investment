FROM grafana/loki:2.9.0

USER root

RUN apk add curl

ENTRYPOINT ["/usr/bin/loki"]
CMD ["-config.file=/etc/loki/config.yaml"]