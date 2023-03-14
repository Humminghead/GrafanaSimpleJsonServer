# Grafana Simple JSON Server
Grafana SimpleJson server it's a server side implementation for a generic Grafana backend datasource - [Simple JSON Datasource](https://grafana.com/grafana/plugins/grafana-simple-json-datasource/).

## How to use it
Copy files to the server and run with parameters:

`HTTPServerSimpleJsonGrafana.py -d <inputfiles_dir> --ip=127.0.0.1 --port=3003 --extension=.out`

- -d - directory where JSON files are stored
- --ip - server address
- --port - server port
- --extension - files extension

***default values are shown above***

## About data format

```json
{
  "@timestamp": 1631541610,
  "counter0": 234,
  "counter1": 7852
  "counter2": 29  
}
```
TODO
