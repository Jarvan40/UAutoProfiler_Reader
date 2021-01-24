import os
import socket
import struct
import io
from hexdump import hexdump
def main():    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 55000-55511
    sock.settimeout(5)
    sock.connect(('127.0.0.1', 55205))
    with open('a.bin', 'rb') as f:
        data = f.read()
    # buf = [0x67A54E8F, 0x5fa194, 0x5fa158, 0x5fa158]

    # magic = [0x8f, 0x4e, 0xa5, 0x67]
    # msgid1 = [22 75 64 d6  e0 e0 74 ad 98 28 c6 0f e4 86 31 c5]
    # msgsz1 = [04 00 00 00]
    # pyadload = [fd 1f 00 00]
    # data = struct.pack('<4i',*buf)
    # print([f'{e:x}' for e in data])
    # print(data)
    
    sock.send(data)
    
    # recv = sock.recv(1024)
    # print(recv) 
    buf = bytes()   
    while True:
        try:        
            recv = sock.recv(10240)            
            if recv:         
                # print(len(recv))       
                # print(hexdump(recv))            
                # buf.extend(recv)
                print(len(buf))
                buf += recv
                if len(buf) > 1024 * 70:
                    # print(hexdump(buf))
                    # print(buf)
                    # with open('o.bin', 'wb') as f:
                    #     f.write(buf)
                    break
        except IOError as msg:
            # print(msg)
            continue
        except KeyboardInterrupt:
            break
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()    
    
    f = open('o.bin', 'wb')
    i = io.BytesIO(buf)
    while True:
        try:
            magic, v1, v2, v3, v4, size = struct.unpack('<6I', i.read(6*4))
            # data  = struct.unpack(f'<{size}b', i.read(size))
            f.write(i.read(size))
            print(f'{magic:x} {v1:x} {v2:x} {v3:x} {v4:x} {size}')                    
        except Exception as e:
            f.close()
            break    

def parser():    
    dat = open('o.bin', 'rb').read()
    i = io.BytesIO(dat)
    signature, = struct.unpack('<I', i.read(4))
    isLittleEndian, = struct.unpack('<?', i.read(1))
    isAlignedMemoryAccess, = struct.unpack('<?', i.read(1))
    platform, = struct.unpack('<H', i.read(2))
    version, = struct.unpack('<I', i.read(4))
    timeNumerator, = struct.unpack('<Q', i.read(8))
    timeDenominator, = struct.unpack('<Q', i.read(8))
    mainThreadId, = struct.unpack('<Q', i.read(8))            
    print(f'{signature:x}', isLittleEndian, isAlignedMemoryAccess, platform, f'{version:x}', f'{timeNumerator:x}', f'{timeDenominator:x}', mainThreadId)
    f = open('blocked.bin', 'wb')
    while True:
        try:            

            block_signature, = struct.unpack('<I', i.read(4))
            blockId, = struct.unpack('<I', i.read(4))
            threadId, = struct.unpack('<Q', i.read(8))         
            length, = struct.unpack('<I', i.read(4))            
            dat = i.read(length)                        
            f.write(dat)
            nextBlockId, = struct.unpack('<I', i.read(4))
            signature, = struct.unpack('<I', i.read(4))
            print(f'{block_signature:x}', blockId, f'{threadId:x}', f'{length:x}', f'{nextBlockId:x}', f'{signature:x}')

        except Exception as e:          
            print(e)  
            break    


def parser_block():
    dat = open('blocked.bin', 'rb').read()
    i = io.BytesIO(dat)    
    while True:
        messageType, = struct.unpack('<H', i.read(2))
        if messageType == 0X21: #kThreadInfo
            threadId, = struct.unpack('<Q', i.read(8))
            startTime, = struct.unpack('<Q', i.read(8))
            flags, = struct.unpack('<I', i.read(4))            
            group_sz, = struct.unpack('<I', i.read(4))          
            if group_sz > 0:
                group = i.read(group_sz)
            else:
                group = ''
            name_sz, =struct.unpack('<I', i.read(4))            

            if name_sz > 0:
                name = i.read(name_sz)
            else:
                name = ''
            print(f'{messageType}', f'{threadId:x}', f'{startTime:x}', f'{flags:x}', f'{group_sz:x}', f'{name_sz:x}')                        
        elif messageType == 0X01: #kSamplerInfo            
            samplerId, = struct.unpack('<I', i.read(4))            
            flags, = struct.unpack('<H', i.read(2))
            group, = struct.unpack('<H', i.read(2))
            name_sz, = struct.unpack('<I', i.read(4))
            if name_sz > 0:
                name = i.read(name_sz)
            else:
                name = ''
            metadataDescriptionsCount, = struct.unpack('<B', i.read(1))
            metadataDescriptions = []
            if metadataDescriptionsCount > 0:
                for _ in range(metadataDescriptionsCount):
                    paramType, = struct.unpack('<H', i.read(2))
                    paramName_sz, = struct.unpack('<I', i.read(4))
                    paramName = ''
                    if paramName_sz > 0:
                        paramName = i.read(paramName_sz)                    
                    print(paramType, paramName)                    

            print(f'{messageType}', f'{samplerId:x}', f'{flags:x}', f'{group:x}', f'{name_sz:x}', f'{metadataDescriptionsCount:x}')                                
        elif messageType == 0X00: #kProfilerState
            flags, = struct.unpack('<I', i.read(4))
            time, = struct.unpack('<Q', i.read(8))
            frameIndex, = struct.unpack('<I', i.read(4))
            print(flags, time, frameIndex)            
        else:
            print(f'{messageType} not parser')
            print(hexdump(i.read(-1)))

            # print(hexdump(i.read(-1)))
            
            break
        # name_sz, = struct.unpack('<I', i.read(4))
        # name = i.read(name_sz)

def parser_block2():
    dat = open('blocked.bin', 'rb').read()
    i = io.BytesIO(dat)
    buf = bytes()

    b = i.read(1)
    messageType, = struct.unpack('<B', b)
    buf += b
    while True:                        
        b = i.read(1)
        messageType, = struct.unpack('<B', b)
        if messageType == 0X21:
            print(" ".join("%02x" % e for e in buf))
            # print(hexdump(buf))
            buf = bytes()
            buf += b
        else:
            buf += b



if __name__ == '__main__':
    parser_block()
    