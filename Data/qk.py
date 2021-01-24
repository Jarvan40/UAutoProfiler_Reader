import mmap
import  os
import sys
import shutil
import subprocess
import glob
import concurrent.futures

def main():    
    with open(sys.argv[1], 'rb') as f:
        signature   = int.from_bytes(f.read(4),  byteorder='little')
        size        = int.from_bytes(f.read(4),  byteorder='little')        
        threadCount = int.from_bytes(f.read(4),  byteorder='little')
        frameIndex  = int.from_bytes(f.read(4),  byteorder='little')
        realFrame  = int.from_bytes(f.read(4),  byteorder='little')
        StartTimeUS  = int.from_bytes(f.read(4),  byteorder='little')
        Cpums  = int.from_bytes(f.read(4),  byteorder='little')
        Gpums  = int.from_bytes(f.read(4),  byteorder='little')
        b_UsedTotal  = int.from_bytes(f.read(4),  byteorder='little') / 1024
        b_UsedUnity  = int.from_bytes(f.read(4),  byteorder='little') / 1024
        t  = int.from_bytes(f.read(4),  byteorder='little') / 1024
        t  = int.from_bytes(f.read(4),  byteorder='little') / 1024
        t  = int.from_bytes(f.read(4),  byteorder='little') / 1024
        print(b_UsedTotal, b_UsedUnity)
        # print(f'{b_UsedTotal:x}')

           
                
    
if __name__ == '__main__':
    main()
    