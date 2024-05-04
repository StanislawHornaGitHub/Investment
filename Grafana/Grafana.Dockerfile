### DESCRIPTION
# Docker file to create image for Grafana container.

### INPUTS
# GF_DEFAULT_INSTANCE_NAME - grafana instance name
# GF_INSTALL_PLUGINS - list of coma separated plugins to be installed

### CHANGE LOG
# Author:   Stanisław Horna
# GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
# Created:  24-Mar-2024
# Version:  1.2

# Date            Who                     What
# 2024-04-22      Stanisław Horna         Instance name added
#
# 2024-05-04      Stanisław Horna         Add log definition variables and timezone.

FROM grafana/grafana-enterprise

ENV GF_DATE_FORMATS_DEFAULT_TIMEZONE="Europe/Warsaw"

ENV GF_DEFAULT_INSTANCE_NAME="Grafana"
ENV GF_INSTALL_PLUGINS="grafana-clock-panel, grafana-simple-json-datasource, speakyourcode-button-panel, volkovlabs-form-panel"

ENV GF_LOG_LEVEL="info"
ENV GF_LOG_MODE="file console"
ENV GF_LOG_FILE_FORMAT="json"

USER root
RUN apk add curl

EXPOSE 3000

ENTRYPOINT [ "/run.sh" ]