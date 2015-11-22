#!/usr/bin/env python

"""
    CryptoWall CryptoLocker clone bundle decompressor by Yonathan Klijnsma (@ydklijnsma)

    Works for file blobs downloaded by the unnamed cryptlocker clone (2013)
"""

import os, sys
from ctypes import *
import struct

def decompress(buf):
    buflen = len(buf) * 16
    dec_data = create_string_buffer(buflen)
    final_size = c_ulong(0)
    buf_size = c_ulong(len(buf))

    # NTSTATUS RtlDecompressBuffer(
    #   _In_  USHORT CompressionFormat,
    #   _Out_ PUCHAR UncompressedBuffer,
    #   _In_  ULONG  UncompressedBufferSize,
    #   _In_  PUCHAR CompressedBuffer,
    #   _In_  ULONG  CompressedBufferSize,
    #   _Out_ PULONG FinalUncompressedSize
    # );
    ret = (nt.RtlDecompressBuffer(2, dec_data, buflen, c_char_p(buf), byref(buf_size), byref(final_size)))
    
    print '[+] Data bundle sizes:'
    print '\t- Compressed size: ', buflen
    print '\t- Decompressed size: ', final_size.value

    return dec_data.raw[:final_size.value]

def main(compressed_bundle, decompressed_files_location):
    compressed_data = open(compressed_bundle, 'rb').read()
    compressed_data_size = len(compressed_data) - 4 # Remove 4 byte size
    decompressed_data = decompress(compressed_data[4::])

    file_index = 0
    total_files = 0
    while file_index < len(decompressed_data):
        blob_checksum = struct.unpack('<I', decompressed_data[file_index:file_index + 4])[0]
        file_index += 4

        blob_size = struct.unpack('<I', decompressed_data[file_index:file_index + 4])[0]
        file_index += 4

        blob_data = decompressed_data[file_index:file_index + (blob_size -1)]
        file_index += blob_size

        print '[+] Found new fileblob in container'
        print '\t- Checksum: ', hex(blob_checksum)
        print '\t- Size: ', blob_size

        f = open(decompressed_files_location + '/{}.bin'.format(total_files), 'wb')
        f.write(blob_data)
        f.close()

        total_files += 1

    print '[+] Found {} files in total'.format(total_files)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: %s <compressed blob filename> <decompressed files location>' % sys.argv[0]
        exit()
    else:
        print main(sys.argv[1], sys.argv[2])

