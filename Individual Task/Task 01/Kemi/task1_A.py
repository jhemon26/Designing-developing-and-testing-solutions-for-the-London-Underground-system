from open_address_hashtable import OpenAddressHashTable

def division_hash_function(key):
    """Returns an integer that will be the hash index."""
    return key % 7

small_hashtable = OpenAddressHashTable(5, division_hash_function)
print(small_hashtable)

lst = [2, 30, 53, 26, 87]
for x in lst:
    small_hashtable.insert(x) #adds each number to the hash table
    print(small_hashtable)
print(small_hashtable.search(87)) #returns the index where the element is stored
# print(small_hashtable.search(53))