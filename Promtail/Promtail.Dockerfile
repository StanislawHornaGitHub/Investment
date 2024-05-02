FROM grafana/promtail:2.9.0

RUN apt-get update
RUN apt-get install -y curl

ENTRYPOINT ["/usr/bin/promtail"]
CMD ["-config.file=/etc/promtail/config.yaml"]