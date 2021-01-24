import mmap
import  os
import sys
import shutil
import subprocess
import glob
import concurrent.futures
import io

def get_wiki_page_existence(frame, timeout=10):
    signature, size, threadCount, offset, i = frame    
    with open(sys.argv[1], 'rb') as f:
        f.seek(offset)
        dat = f.read(12 + size)
        with open(f'./{i}.frame', 'wb') as o:
            o.write(dat)
            o.write(0xDEADFEED.to_bytes(4, byteorder='little'))
    # print(frame)
    return frame

def write_file(dat, i):
    with open(f'./{i}.frame', 'wb') as o:
        o.write(dat)
        o.write(0xDEADFEED.to_bytes(4, byteorder='little'))

def parser_frame(dat, i):
    f = io.BytesIO(dat)
    signature   = int.from_bytes(f.read(4),  byteorder='little')
    size        = int.from_bytes(f.read(4),  byteorder='little')        
    threadCount = int.from_bytes(f.read(4),  byteorder='little')
    frameIndex  = int.from_bytes(f.read(4),  byteorder='little')
    realFrame  = int.from_bytes(f.read(4),  byteorder='little')
    StartTimeUS  = int.from_bytes(f.read(4),  byteorder='little')
    _u = int.from_bytes(f.read(4),  byteorder='little')
    Cpums = int.from_bytes(f.read(4),  byteorder='little')
    Gpums  = int.from_bytes(f.read(4),  byteorder='little')
    m_GatheredData = int.from_bytes(f.read(4),  byteorder='little')
    b_UsedTotal  = int.from_bytes(f.read(4),  byteorder='little') / 1024
    b_UsedUnity  = int.from_bytes(f.read(4),  byteorder='little') / 1024
    t  = int.from_bytes(f.read(4),  byteorder='little') / 1024
    t  = int.from_bytes(f.read(4),  byteorder='little') / 1024
    t  = int.from_bytes(f.read(4),  byteorder='little') / 1024
    return (i, f'{signature:x}', frameIndex, Cpums, Gpums, b_UsedTotal, b_UsedUnity)

def main():
    files_in_dir = glob.iglob('*.frame')
    for _file in files_in_dir:    
        os.remove(_file)    
    
    frames = []
    with open(sys.argv[1], 'rb') as f:
        i = 0
        offset = 0    
        while True:            
            offset = f.tell()
            signature = int.from_bytes(f.read(4),  byteorder='little')
            size = int.from_bytes(f.read(4),  byteorder='little')        
            threadCount = int.from_bytes(f.read(4),  byteorder='little')
            # print(f'{signature:x}', size, threadCount, offset)
            if signature == 0x20191122 or signature == 0x20181101:                                
                frames.append((signature, size, threadCount, offset, i))
                f.seek(size, 1)
                i += 1
                # f.seek(-12, 1)
                # frame = f.read(12 + size)
                # i += 1
                # with open(f'{i}.frame', 'wb') as o:
                #     o.write(frame)    
                #     o.write(0xDEADFEED.to_bytes(4, byteorder='little'))
            else:
                break    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        with open(sys.argv[1], 'r+b') as f2:
            # memory-map the file, size 0 means whole file
            mm = mmap.mmap(f2.fileno(), 0)
            f_bojecst = []
            for signature, size, threadCount, offset, i in frames:            
                print(i)
                dat = mm.read(12+size)
                fobj = executor.submit(parser_frame, dat= dat, i=i)                
                f_bojecst.append(fobj)
            results = []
            for e in concurrent.futures.as_completed(f_bojecst):
                # v = f_bojecst[e]
                results.append(e.result())
            
            results.sort(key=lambda tup: tup[0]) 
            print(results)



                # with open(f'F:/tmp/{i}.frame', 'wb') as o:
                #     o.write(dat)
                #     o.write(0xDEADFEED.to_bytes(4, byteorder='little'))
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = []
    #     for frame in frames:
    #         futures.append(executor.submit(get_wiki_page_existence, frame=frame, timeout=0.00001))
    #     for future in concurrent.futures.as_completed(futures):            
    #         print(future.result())            
                
    
if __name__ == '__main__':
    main()
    