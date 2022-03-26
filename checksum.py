def checksum(count, data):
    #RFC 1071
    addr = 0 
    # Copute Internet Checksum for "count" bytes, begining at location "addr"
    Sum = 0

    while (count > 1):
        # inner loop
        Sum += data[addr] << 8 + data[addr+1]  # index do byte 
        addr += 2
        count -= 2

    # add left-over byte, if any
    if (count > 0):
        Sum += data[addr]

    # fold 32-bit Sum to 16 bits
    while (Sum>>16):
        Sum = (Sum & 0xffff) + (Sum >> 16)

    checksum = ~Sum
    return checksum
