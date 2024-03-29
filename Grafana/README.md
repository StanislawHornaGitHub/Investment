## Startup
### Build docker image
    docker build -t grafana_investment .

### Run container
    docker run --name Grafana_Investment -p 3333:3000 -d grafana_investment

## Grafana configuration
1. Add new data source for PostgreSQL
   - Name: `Investment-DB`
   - Database name: `Investments`
   - username: ``
   - password: ``
   - TLS/SSL Mode: `disable` 
2. Import dashboards form `/Grafana/Dashboards` directory