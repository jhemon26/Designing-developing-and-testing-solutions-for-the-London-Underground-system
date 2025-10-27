from open_address_hashtable import OpenAddressHashTable
from  hash_functions import hashpjw
#Method of how i did this
#I copied the names of all the stations in each train line.
#Pasted them into a text file
#wrote code that goes through each line in the text file , convert them to string and add them to the list if they aren't already in it.

f = open("stations")

# print(f.read())
station_lst = []
for x in f:
    station = str(x).replace("\n","")
    if station not in station_lst:
        station_lst.append(station)

station_hashtable = OpenAddressHashTable(270, hashpjw)
for i in station_lst:
    station_hashtable.insert(i)

print(station_hashtable)

def search_station():
    name = input("Enter a station name: ")
    result = station_hashtable.search(name)
    if result is None:
        return "Not Found"
    return "Operational"

print(search_station())
# print(station_hashtable.search("Dollis Hill"))
# print(station_hashtable.table[80])