from open_address_hashtable import OpenAddressHashTable
from  hash_functions import hashpjw
import pandas as pd
#Method of how I acquired the TFL station data:
#Installed the panda module to parse the Excel sheet.
#Choose the row containing all the station names
#Added all stations names to a list. Avoiding any repetitions by checking if they were already in the list.

stations_xl = pd.read_excel("London Underground data.xlsx")

station_lst = []
for x in stations_xl["Harrow & Wealdstone"].values.tolist():
    if x not in station_lst:
        station_lst.append(x)

station_hashtable = OpenAddressHashTable(280, hashpjw)
for i in station_lst:
    station_hashtable.insert(i)

print(station_lst)

def search_station():
    name = input("Enter a station name: ")
    result = station_hashtable.search(name)
    if result is None:
        return "Not Found"
    return "Operational"

print(search_station())
