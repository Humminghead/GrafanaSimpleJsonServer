# Grafana Simple JSON Server
Grafana SimpleJson server it's a server side implementation for a generic Grafana backend datasource - [Simple JSON Datasource](https://grafana.com/grafana/plugins/grafana-simple-json-datasource/).

## Requrements:
- [Python 3.8.10](https://www.python.org/downloads/)

## How to use it
Copy files to a target and run `HTTPServerSimpleJsonGrafana.py`.

For example:

`HTTPServerSimpleJsonGrafana.py -d <inputfiles_dir> --ip=127.0.0.1 --port=3003 --extension=.txt`

## Command line parameters:

- -d - directory where JSON files are stored
- --ip - server address
- --port - server port
- --extension - file name suffix (by default: '.json')
- --max_records_count - max number of records in app cache (off by default: 0)
- --read_interval - data read interval in seconds (by default: 1s)

***default values are shown above***

- -d - empty
- --ip - 127.0.0.1
- --port - 3003
- --extension - json
- --max_records_count -  0
- --read_interval - 1s

## About data format

```json
{
  "@timestamp": 1631541610,
  "counter0": 234,
  "counter1": 7852
  "counter2": 29  
}
```
If the `@timestamp` field exists at the root of the user data, then the moment the file has been read from disk and converted to a JSON object, the time from the `@timestamp` will be captured as the timestamp of the data. Othervise system time will be used.
