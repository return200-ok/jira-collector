# Jira Influx Collector 
`Jira Influx Collector` is a python job to collect sprint infomation from Jira and push them to influxdb

## Quick start with `docker`
Run command below (edit env):
```
docker run -d \
-eJIRA_URL = 'http://jira_server:8080' \
-eJIRA_USER = 'jira_user' \
-eJIRA_PASSWORD = 'jira_password' \
-eINFLUX_TOKEN="KlXfBqa0uSGs0icfE-3g8FsQAoC9..." \
-eINFLUX_DB="http://192.168.3.101:8086" \
-eINFLUX_ORG="org" \
-eBUCKET_NAME="jira" \
return200/jira-influx-collector:0.1
```

# Use

## Run

### Build image
Run command below:
```
docker build -t return200/jira-influx-collector:0.1 .
```
### Change cronjob
Cronjob is set " 0 0 * * * " in current.
```
cat crontab
# START CRON JOB
0 0 * * * /usr/local/bin/python3 /jira_influx_collector/main.py > /proc/1/fd/1 2>/proc/1/fd/2
# END CRON JOB
```

### Run with `docker compose`

#### Define your environment

Using the sample environment as a base, 

```bash
$ cd docker-compose
$ cp config/sample.env config/production.env
$ vim config/production.env
```
#### Start with docker compose 
To run with your newly configured environment, execute the following.

```bash
docker-compose up -d
```
### Viewing data with Grafana
By default, a grafana instance preloaded with templated dashboards will be started. Use your browser to view [http://localhost:3000](http://localhost:3000). The default username is `admin` and default password is `admin`. The dasboards are then accessible under the 'Home' tab.

### Templated Grafana dashboards

The files under `dashboards/*.json` contain a grafana dashboards described below.
Or you can import dashboard from [18021] (https://grafana.com/grafana/dashboards/18021)

#### `Jira Sprint Summary Dashboard` 

The `Jira Sprint Summary Dashboard` dashboard presents sprint summary from Jira. See an image of the dasboard with data below.
![overview!](https://github.com/return200-ok/jira-crawler/blob/main/assets/Jira_Sprint_Summary_Dashboard.png?raw=true)








