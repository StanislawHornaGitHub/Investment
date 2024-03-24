## Startup
### Build docker image
    docker build -t grafana_investment .

### Run container
    docker run --name Grafana_Investment -p 3333:3000 -d grafana_investment
