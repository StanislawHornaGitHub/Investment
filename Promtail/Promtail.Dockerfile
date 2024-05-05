### DESCRIPTION
# Docker file to create image for Grafana Promtail.

### INPUTS

### CHANGE LOG
# Author:   Stanisław Horna
# GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
# Created:  02-May-2024
# Version:  1.1

# Date            Who                     What
# 2024-05-05      Stanisław Horna         Add timezone setup.
#

FROM grafana/promtail:2.9.0

RUN apt-get update
RUN apt-get install -y curl

# Set timezone
ENV TZ="Europe/Warsaw"

ENTRYPOINT ["/usr/bin/promtail"]
CMD ["-config.file=/etc/promtail/config.yaml"]