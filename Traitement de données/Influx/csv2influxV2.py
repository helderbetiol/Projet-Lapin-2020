# csv2influx.py
# Sends data from csv files to influxDB
# Requirement: pip install influxdb
# Tested with Python 3.7
# Usage example: 
# python csv2influx.py --file data-groupe1_Seq2_adrenaline\ 50uL_Essai4.csv --group 1 --measure adrenaline
#
# References:
# https://www.influxdata.com/blog/writing-data-to-influxdb-with-python/
# https://influxdb-python.readthedocs.io/en/latest/examples.html

import csv
import argparse
import os 
from influxdb import InfluxDBClient

# csv_to_influx
# input: a csv file name (with path, if needed)
# extracts data from the csv and sends it to influx
def csv_to_influx(file, args):
    print("Processing file "+file)
    # create json batches from csv
    json_batches = csv_to_influx_json(file, args.measure, args.group)
    if json_batches:
        print("We have data")
        # print(json_body)
        # exit()
    else:
        print("NO DATA!")
        exit()

    # send batches to influx
    send_influx(json_batches, host=args.host, port=args.port, user=args.user, password=args.password, dbname=args.dbname)

# send_influx
# input: JSON batches of points to write to influx
def send_influx(json_batches, host='localhost', port=8086, user='root', password='root', dbname='rabbit'):
    # Instantiate a connection to the InfluxDB
    # Additional parameteres
    # dbuser = 'smly'
    # dbuser_password = 'my_secret_password'
    client = InfluxDBClient(host, port, user, password, dbname)

    print("Create database: " + dbname)
    client.create_database(dbname)

    # Queries
    # query = 'select Float_value from cpu_load_short;'
    query = 'select * from adrenaline limit 5;'
    # query_where = 'select Int_value from cpu_load_short where host=$host;'
    # bind_params = {'host': 'server01'}

    # print("Create a retention policy")
    # client.create_retention_policy('awesome_policy', '3d', 3, default=True)

    # print("Switch user: " + dbuser)
    # client.switch_user(dbuser, dbuser_password)

    # print("Write points: {0}".format(json_body))
    for json_body in json_batches:
        client.write_points(json_body, time_precision='u')

    print("Querying data: " + query)
    result = client.query(query)
    print("Result: {0}".format(result))

    # print("Querying data: " + query_where)
    # result = client.query(query_where, bind_params=bind_params)
    # print("Result: {0}".format(result))

    # print("Switch user: " + user)
    # client.switch_user(user, password)

    # print("Drop database: " + dbname)
    # client.drop_database(dbname)

# read_csv_to_influx_json
# input: receives the csv file name (with path, if needed)
# output: an array of json files to send to influx
def csv_to_influx_json(file_name, measurement, groupID):
    line_count = 0
    time_offset = 0 # shift the timeseries so it begins in 0s
    json_batches = [] # InfluxDB performs best when data is written in batches
    json_body = [] # for each json batch

    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file) # read CSV file and save it as dict
        first_line = True
        for row in csv_reader:
            if first_line: 
                # first line should have column names
                print(f'Column names are {", ".join(row)}')
                line_count += 1
                first_line = False
            else:
                # each line is a new measurement (new point to write)
                value = FloatOrZero(row["PressionArterielle"])
                if checkPA(value):
                    measurement_data = {
                        "measurement": measurement,
                        "tags": {
                            "group": groupID,
                            "attribute": "PressionArterielle"
                        },
                        "time": int(FloatOrZero(row["Temps"])*1000000) - time_offset, # converted to us (microseconds)
                        "fields": { # Temps,PressionArterielle,Spirometrie,PAmoyenne,FrequenceCardiaque,FrequenceRespiratoire,Remarque
                            "PressionArterielle": value
                        }
                    }
                    json_body.append(measurement_data)

                value = FloatOrZero(row["FrequenceCardiaque"])
                if checkFC(value):
                    measurement_data = {
                        "measurement": measurement,
                        "tags": {
                            "group": groupID,
                            "attribute": "FrequenceCardiaque"
                        },
                        "time": int(FloatOrZero(row["Temps"])*1000000) - time_offset, # converted to us (microseconds)
                        "fields": { 
                            "FrequenceCardiaque": value
                        }
                    }
                    json_body.append(measurement_data)

                value = FloatOrZero(row["FrequenceRespiratoire"])
                if checkFR(value):
                    measurement_data = {
                        "measurement": measurement,
                        "tags": {
                            "group": groupID,
                            "attribute": "FrequenceRespiratoire"
                        },
                        "time": int(FloatOrZero(row["Temps"])*1000000) - time_offset, # converted to us (microseconds)
                        "fields": {
                            "FrequenceRespiratoire": value
                        }
                    }
                    json_body.append(measurement_data)

                if line_count == 1 and time_offset == 0: # first value
                    time_offset = measurement_dataPA["time"] # offset is the first measure's time 

                line_count += 1

                if line_count >= 10000: # ideal batch size for InfluxDB is 5,000-10,000 points
                    json_batches.append(json_body)
                    line_count = 0
                    json_body = []  

    if 0 < line_count < 10000: # one last batch left to add
        json_batches.append(json_body)   

    return json_batches

def FloatOrZero(value):
    try:
        return float(value)
    except:
        return 0.0

def checkPA(pa):
    if pa < 0:
        return False
    else:
        return True

def checkFR(fr):
    if fr > 70 or fr < 20:
        return False
    else:
        return True

def checkFC(fc):
    if fc > 350 or fc < 100:
        return False
    else:
        return True

# parse the args
def parse_args():
    parser = argparse.ArgumentParser(
        description='csv2python sends data from csv files to influxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    parser.add_argument('--user', type=str, required=False, default='root',
                        help='user of InfluxDB')
    parser.add_argument('--password', type=str, required=False, default='root',
                        help='password of InfluxDB')
    parser.add_argument('--dbname', type=str, required=False, default='rabbit',
                        help='Database name to use or create')
    parser.add_argument('--file', type=str, required=False,
                        help='CSV file to read the data from')
    parser.add_argument('--path', type=str, required=False,
                        help='Directory with CSV files to read the data from')
    parser.add_argument('--measure', type=str, required=True,
                        help='Measurement: adrenaline, acetylcholine, rest, ...')
    parser.add_argument('--group', type=int, required=True,
                        help='Group ID that identifies an unique rabbit')
    return parser.parse_args()

# MAIN
if __name__ == '__main__':
    args = parse_args()
    if not (args.file or args.path):
        parser.error('No CSV file provided, add --file or --path')

    if args.path:
        # process all files in given path
        with os.scandir(args.path) as directory:   
            file_list = [file.name for file in directory if os.path.isfile(file)]
            if not file_list:
                print("No files found in path")
                exit()

        for file in file_list:
            args.group = Int(file.split('_')[0].replace('data-groupe', ''))
            data-groupeX_SeqY.csv
            file = args.path + file
            print(file)
            csv_to_influx(file, args)
            # each file is expected to be an unique group
            # args.group += 1

    else:
        # process one given file
        csv_to_influx(args.file, args)
