import random
import array
import hashlib
import threading

class CountMinSketch:
    def __init__(self, tableSize, hashFuncCount):
        self.__tableSize = tableSize
        self.__hashFuncCount = hashFuncCount
        self.__tables = []
        self.__lock = threading.Lock()
        for _ in range(0, self.__hashFuncCount):
            table = array.array('l', (0 for _ in range(0, self.__tableSize)))
            self.__tables.append(table)

    def __getHash(self, value):
        md5Value = hashlib.md5(str(hash(value)))
        for i in range(0, self.__hashFuncCount):
            md5Value.update(str(i))
            yield int(md5Value.hexdigest(), 16) % self.__tableSize
        
    def add(self, key):
        with self.__lock:
            for table, i in zip(self.__tables, self.__getHash(key)):
                table[i] += 1
            
    def get(self, key):
        with self.__lock:    
            return min(table[i] for table, i in zip(self.__tables, self.__getHash(key)))