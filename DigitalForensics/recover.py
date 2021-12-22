import binascii
import hashlib

currentfile = 0
BUF_SIZE = 512
offset = 0


# Press the green button in the gutter to run the script.
def carveSector(currSector, footer, isDocx):
    currFinalSector = b""
    byteList = [b'%c' % i for i in currSector]
    for element in range(0, len(byteList)):
        curTestFooter = b''
        for i in range(element, element + len(footer)):
            curTestFooter += byteList[i]
        if int(curTestFooter, 16) == int(footer, 16):
            if isDocx:
                for x in range(element + len(footer),  element + len(footer) + 36):
                    curTestFooter += byteList[x]
            currFinalSector += curTestFooter
            break
        currFinalSector += byteList[element]
    return currFinalSector


if __name__ == '__main__':
    with open("Project2.dd", "rb") as file:
        while True:
            currSector = binascii.hexlify(file.read(512))
            if currSector == b'':
                break

            # MPG
            if currSector.startswith(b"000001b3"):
                startOffset = offset
                currFile = b""
                # Loops until footer found
                while not (currSector.__contains__(b"000001b7")):
                    currFile += currSector
                    currSector = binascii.hexlify(file.read(512))
                    offset += 512
                # Carves out last sector
                currFile += carveSector(currSector, b"000001b7", False)
                # Writes File
                mpg = open('mpg' + str(currentfile) + '.mpg', 'wb')
                mpg.write(binascii.unhexlify(currFile))
                mpg.close()
                sha1 = hashlib.sha1()
                # Writes SHA-256 hash
                with open('mpg' + str(currentfile) + '.mpg', 'rb') as f:
                    while True:
                        data = f.read(BUF_SIZE)
                        if not data:
                            break
                        sha1.update(data)
                # Prints the current file data
                print("mpg" + str(currentfile) + ".mpg, Start Offset: " + hex(startOffset) + " End Offset:  " + hex(
                    startOffset + len(binascii.unhexlify(currFile)) - 1) + "\nSHA-256: " + sha1.hexdigest())
                currentfile += 1

            # PDF -- GOOD
            if currSector.startswith(b"25504446"):
                startOffset = offset
                currFile = b""
                # Loops until footer found
                while not ((currSector.__contains__(b"0a2525454f460d0a") or currSector.__contains__(
                        b"0a2525454f460a")) and currSector.endswith(b"00")):
                    currFile += currSector
                    currSector = binascii.hexlify(file.read(512))
                    offset += 512
                # Carves out last sector
                if currSector.__contains__(b"0a2525454f460d0a"):
                    currFile += carveSector(currSector, b"0a2525454f460d0a", False)
                else:
                    currFile += carveSector(currSector, b"0a2525454f460a", False)
                # Writes File
                pdf = open('pdf' + str(currentfile) + '.pdf', 'wb')
                pdf.write(binascii.unhexlify(currFile))
                pdf.close()
                # Writes SHA-256 hash
                sha1 = hashlib.sha1()
                with open('pdf' + str(currentfile) + '.pdf', 'rb') as f:
                    while True:
                        data = f.read(BUF_SIZE)
                        if not data:
                            break
                        sha1.update(data)
                # Prints the current file data
                print("pdf" + str(currentfile) + ".pdf, Start Offset: " + hex(startOffset) + " End Offset:  " + hex(
                    startOffset + len(binascii.unhexlify(currFile)) - 1) + "\nSHA-256: " + sha1.hexdigest())
                currentfile += 1

            # BMP
            if currSector.startswith(b'424d'):
                startOffset = offset
                currFile = b""
                # Gets file length
                fileLength = currSector[10:12] + currSector[8:10] + currSector[6:8] + currSector[4:6]
                fileLength = fileLength.decode('utf-8')
                fileLength = int(fileLength, 16)
                if fileLength < 1000000:
                    # Creates File
                    currFile += currSector
                    currFile += binascii.hexlify(file.read(fileLength - 512))
                    file.read(512 - fileLength % 512)
                    offset += fileLength + (512 - fileLength % 512) - 512
                    # Writes File
                    bmp = open('bmp' + str(currentfile) + '.bmp', 'wb')
                    bmp.write(binascii.unhexlify(currFile))
                    bmp.close()
                    sha1 = hashlib.sha1()
                    # Writes SHA-256 hash
                    with open('bmp' + str(currentfile) + '.bmp', 'rb') as f:
                        while True:
                            data = f.read(BUF_SIZE)
                            if not data:
                                break
                            sha1.update(data)
                    # Prints the current file data
                    print("bmp" + str(currentfile) + ".bmp, Start Offset: " + hex(
                        startOffset) + " End Offset:  " + hex(
                        startOffset + len(binascii.unhexlify(currFile)) - 1) + "\nSHA-256: " + sha1.hexdigest())
                currentfile += 1

            # GIF
            if currSector.startswith(b"474946383761") or currSector.startswith(b"474946383961"):
                startOffset = offset
                currFile = b""
                # Loops until footer found
                while not (currSector.__contains__(b"00003b") and currSector.index(b"00003b") % 2 == 0):
                    currFile += currSector
                    currSector = binascii.hexlify(file.read(512))
                    offset += 512
                # Carves out last sector
                currFile += carveSector(currSector, b"00003b", False)
                # Writes File
                gif = open('gif' + str(currentfile) + '.gif', 'wb')
                gif.write(binascii.unhexlify(currFile))
                gif.close()
                # Writes SHA-256 hash
                sha1 = hashlib.sha1()
                with open('gif' + str(currentfile) + '.gif', 'rb') as f:
                    while True:
                        data = f.read(BUF_SIZE)
                        if not data:
                            break
                        sha1.update(data)
                # Prints the current file data
                print("gif" + str(currentfile) + ".gif, Start Offset: " + hex(startOffset) + " End Offset:  " + hex(
                    startOffset + len(binascii.unhexlify(currFile)) - 1) + "\nSHA-256: " + sha1.hexdigest())
                currentfile += 1

            # JPG -- GOOD
            if currSector.startswith(b"ffd8ff"):
                startOffset = offset
                currFile = b""
                # Loops until footer found
                while not (currSector.__contains__(b"ffd9") and currSector.index(b"ffd9") % 2 == 0):
                    currFile += currSector
                    currSector = binascii.hexlify(file.read(512))
                    offset += 512
                # Carves out last sector
                currFile += carveSector(currSector, b'ffd9', False)
                # Writes File
                jpg = open('jpg' + str(currentfile) + '.jpg', 'wb')
                jpg.write(binascii.unhexlify(currFile))
                jpg.close()
                # Writes SHA-256 hash
                sha1 = hashlib.sha1()
                with open('jpg' + str(currentfile) + '.jpg', 'rb') as f:
                    while True:
                        data = f.read(BUF_SIZE)
                        if not data:
                            break
                        sha1.update(data)
                # Prints the current file data
                print("jpg" + str(currentfile) + ".jpg, Start Offset: " + hex(startOffset) + " End Offset:  " + hex(
                    startOffset + len(binascii.unhexlify(currFile)) - 1) + "\nSHA-256: " + sha1.hexdigest())
                currentfile += 1

            # DOCX
            if currSector.startswith(b"504b030414000600"):
                startOffset = offset
                currFile = b""
                # Loops until footer found
                while not (currSector.__contains__(b"504b0506")):
                    currFile += currSector
                    currSector = binascii.hexlify(file.read(512))
                    offset += 512
                # Carves out last sector
                currFile += carveSector(currSector, b"504b0506", True)
                # Writes File
                docx = open('docx' + str(currentfile) + '.docx', 'wb')
                docx.write(binascii.unhexlify(currFile))
                docx.close()
                # Writes SHA-256 hash
                sha1 = hashlib.sha1()
                with open('docx' + str(currentfile) + '.docx', 'rb') as f:
                    while True:
                        data = f.read(BUF_SIZE)
                        if not data:
                            break
                        sha1.update(data)
                # Prints the current file data
                print("docx" + str(currentfile) + ".docx, Start Offset: " + hex(startOffset) + " End Offset:  " + hex(
                    startOffset + len(binascii.unhexlify(currFile)) - 1) + "\nSHA-256: " + sha1.hexdigest())
                currentfile += 1

            # AVI
            if currSector.startswith(b'52494646'):
                startOffset = offset
                currFile = b""
                # Gathers file length
                fileLength = currSector[14:16] + currSector[12:14] + currSector[10:12] + currSector[8:10]
                fileLength = fileLength.decode('utf-8')
                fileLength = int(fileLength, 16) + 8
                # Carves last sector
                currFile += currSector
                currFile += binascii.hexlify(file.read(fileLength - 512))
                file.read(512 - fileLength % 512)
                offset += fileLength + (512 - fileLength % 512) - 512
                # Writes to file
                avi = open('avi' + str(currentfile) + '.avi', 'wb')
                avi.write(binascii.unhexlify(currFile))
                avi.close()
                # Writes hash
                sha1 = hashlib.sha1()
                with open('avi' + str(currentfile) + '.avi', 'rb') as f:
                    while True:
                        data = f.read(BUF_SIZE)
                        if not data:
                            break
                        sha1.update(data)
                # Prints the current file data
                print("avi" + str(currentfile) + ".avi, Start Offset: " + hex(startOffset) + " End Offset:  " + hex(
                    startOffset + len(binascii.unhexlify(currFile)) - 1) + "\nSHA-256: " + sha1.hexdigest())
                currentfile += 1

            # PNG -- GOOD
            if currSector.startswith(b"89504e47"):
                startOffset = offset
                currFile = b""
                # Loops until footer found
                while not (currSector.__contains__(b"49454e44ae426082") and currSector.index(
                        b"49454e44ae426082") % 2 == 0):
                    currFile += currSector
                    currSector = binascii.hexlify(file.read(512))
                    offset += 512
                # Carves out last sector
                currFile += carveSector(currSector, b"49454e44ae426082", False)
                # Writes File
                png = open('png' + str(currentfile) + '.png', 'wb')
                png.write(binascii.unhexlify(currFile))
                png.close()
                # Writes SHA-256 hash
                sha1 = hashlib.sha1()
                with open('png' + str(currentfile) + '.png', 'rb') as f:
                    while True:
                        data = f.read(BUF_SIZE)
                        if not data:
                            break
                        sha1.update(data)
                # Prints the current file data
                print("png" + str(currentfile) + ".png, Start Offset: " + hex(startOffset) + " End Offset:  " + hex(
                    startOffset + len(binascii.unhexlify(currFile)) - 1) + "\nSHA-256: " + sha1.hexdigest())
                currentfile += 1
            offset += 512

