import time #ask the lecturer if i am allowed to use the time and random for 1.b
import random
from open_address_hashtable import OpenAddressHashTable
from hash_functions import hashpjw
start = time.time()

def insert_elements_hashtable(size, hash_func1, hash_func2 = None):
    # if hash_func2 is not None:
    #     hashtable = OpenAddressHashTable(size, hash_func1, hash_func2)
    hashtable = OpenAddressHashTable(size, hash_func1)
    for x in [num for num in range(size)]:
        hashtable.insert(x)
    return hashtable

#only one hash function
dataset_1k = insert_elements_hashtable(1000, hashpjw)
dataset_5k = insert_elements_hashtable(5000, hashpjw)
dataset_10k = insert_elements_hashtable(10000, hashpjw)
dataset_25k = insert_elements_hashtable(25000, hashpjw)
dataset_50k = insert_elements_hashtable(50000, hashpjw)

def measure_status_checker(hashtable, target):
    begin = time.time()
    hashtable.search(target)
    finish = time.time()
    return f"Finding {target} took {finish-begin}"

print(measure_status_checker(dataset_1k , random.randint(0,999)))
print(measure_status_checker(dataset_1k , random.randint(0,999)))
print(measure_status_checker(dataset_1k , random.randint(0,999)))
print(measure_status_checker(dataset_1k , random.randint(0,999)))

print(measure_status_checker(dataset_5k, random.randint(0,5000)))
print(measure_status_checker(dataset_5k, random.randint(0,5000)))
print(measure_status_checker(dataset_5k, random.randint(0,5000)))
print(measure_status_checker(dataset_5k, random.randint(0,5000)))

print(measure_status_checker(dataset_10k, random.randint(0,10000)))
print(measure_status_checker(dataset_10k, random.randint(0,10000)))
print(measure_status_checker(dataset_10k, random.randint(0,10000)))
print(measure_status_checker(dataset_10k, random.randint(0,10000)))

print(measure_status_checker(dataset_25k, random.randint(0,25000)))
print(measure_status_checker(dataset_25k, random.randint(0,25000)))
print(measure_status_checker(dataset_25k, random.randint(0,25000)))
print(measure_status_checker(dataset_25k, random.randint(0,25000)))

print(measure_status_checker(dataset_50k, random.randint(0,50000)))
print(measure_status_checker(dataset_50k, random.randint(0,50000)))
print(measure_status_checker(dataset_50k, random.randint(0,50000)))
print(measure_status_checker(dataset_50k, random.randint(0,50000)))
end = time.time()
print("Total time running: ", end-start)

