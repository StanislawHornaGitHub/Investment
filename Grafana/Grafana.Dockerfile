### DESCRIPTION
# Docker file to create image for Grafana container.

### INPUTS
# GF_DEFAULT_INSTANCE_NAME - grafana instance name
# GF_INSTALL_PLUGINS - list of coma separated plugins to be installed

### CHANGE LOG
# Author:   Stanisław Horna
# GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
# Created:  24-Mar-2024
# Version:  1.1

# Date            Who                     What
# 2024-04-22      Stanisław Horna         Instance name added

FROM grafana/grafana-enterprise


ENV GF_DEFAULT_INSTANCE_NAME="Grafana"
ENV GF_INSTALL_PLUGINS="grafana-clock-panel, grafana-simple-json-datasource, speakyourcode-button-panel, volkovlabs-form-panel"
ENV GF_LOG_LEVEL="warn"

EXPOSE 3000

ENTRYPOINT [ "/run.sh" ]