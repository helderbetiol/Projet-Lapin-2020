#######################################################################################################################
#
#                                           Lapin Automate
#                                      Code liaison PC - Arduino
#
#######################################################################################################################
#imports
import pandas as pd
import time
import serial
import io
import requests # pip install requests

#Ouverture du fichier Excel
#file_name = "C:/Users/Lenovo/Desktop/Projet lapin/Donnees_demo/respi.csv"
#file_name2 = "C:/Users/Lenovo/Desktop/Projet lapin/donnees_demo/card.csv"

#df = pd.read_csv(file_name)
#df2 = pd.read_csv(file_name2)

url = "https://lapin-influx.osc-fr1.scalingo.io/"
paramsFR = "lapin/csv/adrenaline/20?limit=6000&field=FrequenceRespiratoire"
paramsFC = "lapin/csv/adrenaline/20?limit=6000&field=FrequenceCardiaque"

response = requests.get(url+paramsFR).content
df = pd.read_csv(io.StringIO(response.decode('utf-8')))

response = requests.get(url+paramsFC).content
df2 = pd.read_csv(io.StringIO(response.decode('utf-8')))

ser = serial.Serial('COM17', 9600)
time.sleep(1)

#print(df.at[3,'time'][17:23].replace('Z',''))


#Envoi des données vers Serial
t = time.time()
t3 = t
line_index = 1
old_line_time = float(df.at[line_index,'time'][17:23].replace('Z','')) + float(df.at[line_index,'time'][11:13])*3600 + float(df.at[line_index,'time'][14:16])*60
#current_line = line_index
row_count = min(len(df.index),len(df2.index))
while line_index < row_count and t-t3 < 40:



    line_time = float(df.at[line_index,'time'][17:23].replace('Z','')) + float(df.at[line_index,'time'][11:13])*3600 + float(df.at[line_index,'time'][14:16])*60    #11
    #print(line_time)

    if line_time - old_line_time < 0.5:
        line_index += 1




    t2 = time.time()

    if t2-t >= 0.5:

        old_line_time = line_time

        #print(df2.at[line_index,'FrequenceCardiaque'])
        msg = str(df2.at[line_index,'FrequenceCardiaque']) + 'c' + str(df.at[line_index,'FrequenceRespiratoire']) + 'r' #[freq_cardiaque, freq_respi]

        #print(df.at[line_index,'time'])
        ser.write(msg.encode())
        t = t2

msg = "10000000" + 'c' + "0.0001" + 'r'
ser.write(msg.encode())

ser.close()
print("ended")


