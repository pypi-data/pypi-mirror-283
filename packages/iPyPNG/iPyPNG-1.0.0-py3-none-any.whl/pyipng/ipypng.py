import zlib
from struct import pack, unpack
from binascii import crc32

def convert(img_bytes: bytes) -> bytes:
    '''
    This is for turning standard PNG to Apple CgBI PNG
    :param img_bytes: bytes: standard png
    :return: bytes: apple png
    '''
    signature_header = img_bytes[:8]
    rest_of_png = img_bytes[8:]
    new_PNG = signature_header
    current_byte = 8
    cgbi_added = False
    IDAT_data_raw = b''
    IDAT_type_raw = b''
    img_width = 0
    img_height = 0

    while current_byte < len(img_bytes):
        chunk_length_raw = img_bytes[current_byte:current_byte + 4]
        chunk_length = int.from_bytes(chunk_length_raw, 'big')
        current_byte += 4
        chunk_type_raw = img_bytes[current_byte:current_byte + 4]
        chunk_type = str(chunk_type_raw, encoding='ASCII')
        current_byte += 4
        chunk_data = img_bytes[current_byte:current_byte + chunk_length]
        chunk_CRC = img_bytes[current_byte + chunk_length:current_byte + chunk_length + 4]

        if chunk_type == 'IHDR':
            img_width, img_height, bitd, colort, compm, filterm, interlacem = unpack('>IIBBBBB', chunk_data)
            if compm != 0 or filterm != 0 or colort != 6 or bitd != 8 or interlacem != 0:
                raise ValueError('Unsupported PNG format')

            if not cgbi_added:
                cgbi_chunk = b'CgBI'
                cgbi_length = b'\x00\x00\x00\x00'
                cgbi_crc = crc32(cgbi_chunk).to_bytes(4, 'big')
                new_PNG += cgbi_length + cgbi_chunk + cgbi_crc
                cgbi_added = True

        elif chunk_type == 'IDAT':
            IDAT_type_raw = chunk_type_raw
            IDAT_data_raw += chunk_data
            current_byte += chunk_length + 4
            continue

        elif chunk_type == 'IEND':
            try:
                decompressed_data = zlib.decompress(IDAT_data_raw)
            except Exception as e:
                raise ArithmeticError('Error decompressing IDAT chunk!\n' + str(e))

            new_data = b''
            for y in range(img_height):
                position = y * (img_width * 4 + 1)
                new_data += decompressed_data[position:position + 1]
                for x in range(img_width):
                    pixel = position + 1 + x * 4
                    new_data += decompressed_data[pixel + 2:pixel + 3]  # Red
                    new_data += decompressed_data[pixel + 1:pixel + 2]  # Green
                    new_data += decompressed_data[pixel:pixel + 1]      # Blue
                    new_data += decompressed_data[pixel + 3:pixel + 4]  # Alpha

            compressed_data = zlib.compress(new_data)
            chunk_length_raw = len(compressed_data).to_bytes(4, 'big')
            new_CRC = crc32(IDAT_type_raw)
            new_CRC = crc32(compressed_data, new_CRC)
            new_CRC = (new_CRC + 0x100000000) % 0x100000000
            new_PNG += chunk_length_raw + IDAT_type_raw + compressed_data + new_CRC.to_bytes(4, 'big')

        new_CRC = crc32(chunk_type_raw)
        new_CRC = crc32(chunk_data, new_CRC)
        new_CRC = (new_CRC + 0x100000000) % 0x100000000
        new_PNG += chunk_length_raw + chunk_type_raw + chunk_data + new_CRC.to_bytes(4, 'big')
        current_byte += chunk_length + 4

    return new_PNG
