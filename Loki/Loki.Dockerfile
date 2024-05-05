### DESCRIPTION
# Docker file to create image for Grafana Loki.

### INPUTS

### CHANGE LOG
# Author:   Stanisław Horna
# GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
# Created:  02-May-2024
# Version:  1.1

# Date            Who                     What
# 2024-05-05      Stanisław Horna         Add timezone setup.
#

FROM grafana/loki:2.9.0

USER root

RUN apk add curl

# Set timezone
ENV TZ="Europe/Warsaw"
RUN apk add --no-cache tzdata

ENTRYPOINT ["/usr/bin/loki"]
CMD ["-config.file=/etc/loki/config.yaml"]