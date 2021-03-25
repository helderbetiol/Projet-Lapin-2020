# InfluxDB

InfluxDB is a Time Series Database used to store and manipulate the TPs data of this project. 

Version in use for this project: 1.8.3.

Useful links for everyone:
- [InfluxDB v1.8 Documentation](https://docs.influxdata.com/influxdb/v1.8/)
- [Get started with InfluxDB OSS | InfluxDB v1.8 Documentation](https://docs.influxdata.com/influxdb/v1.8/introduction/get-started/)
- [InfluxDB key concepts | InfluxDB v1.8 Documentation](https://docs.influxdata.com/influxdb/v1.8/concepts/key_concepts/)
- [InfluxDB schema design and data layout | InfluxDB v1.8 Documentation](https://docs.influxdata.com/influxdb/v1.8/concepts/schema_and_data_layout/)

Useful links for génération de nouvelles courbes (previsions):
- [Time Series Forecasting Methods | InfluxData](https://www.influxdata.com/time-series-forecasting-methods/)
- [Applying Machine Learning Models to InfluxDB | InfluxData](https://www.influxdata.com/blog/applying-machine-learning-models-to-influxdb-with-loud-ml-docker-for-time-series-predictions/)
- [Loud ML | InfluxData](https://www.influxdata.com/partners/loud-ml/)
- [Installing and running Loud ML with Docker | Loud ML Reference](https://loudml.io/en/loudml/reference/current/docker.html)


## Schema 

Quick intro: a series is a collection of points that share a measurement, tag set, and field key. The measurement acts as a container for tags, fields, and the time column. Tags are indexed, fields are not.

Measurements : the injections.
- Adrenaline
- Acétylcholine
- Ballon
- Others to be added...

Complete example:

- Measurement: Adrenaline 
  - Tags: Group ID
  - Fields: 
	- PressionArterielle;
	- FrequenceCardiaque;
	- FrequenceRespiratoire.

Series: Measurement (Adrenaline, for example) + Group ID. Group ID can be seen as the ID of the rabbit. 

Retention policy: autogen (InfluxDB automatically creates that retention policy; it has an infinite duration and a replication factor set to one).

## Code

Csv2influx.py is used to read the data from .csv files and create the influx database according to the above schema. More information on how to use it can be found on the code. The following command can help:
```
python csv2influx.py --help
```

Csv2influxV2.py has the same purpose, but using a different schema. Only one field is present and the name of the field (Pression Arterielle, for example) is a tag. This creates one serie per injection per groupe per field. It was used only for testing.

## Restore

In the folder influx-export, you will find a compressed file with an export of the database created during the project. To restore it, unzip the file and use the command:
```
influxd restore -portable -db rabbit3 -newdb rabbit_restore [directory of unzip]
```

## Examples of queries
```
SELECT ("PressionArterielle") FROM "test"."autogen"."adrenaline" WHERE "time" > '1970-01-01T00:04:40.001000Z' and "time" < '1970-01-01T00:05:00.001000Z' and "group"=’22'

SELECT ("FrequenceRespiratoire") FROM "test"."autogen"."adrenaline" WHERE  "group"=‘1'

SELECT ("FrequenceCardiaque") FROM "test"."autogen"."adrenaline" WHERE  "group"=‘1'
```
