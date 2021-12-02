# This is a sample Python script.
import binascii
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
currentfile = 0

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open("Project2.dd", "rb") as file:
        while True:
            currSector = binascii.hexlify(file.read(512))
            if currSector == b'':
                break
            # if currSector.startswith(b"000001b"):
            #     print("MPG " + str(currSector))
            # if currSector.startswith(b"25504446"):
            #     print("PDF " + str(currSector))
            # if currSector.startswith(b"424d"):
            #     print("BMP " + str(currSector))
            if currSector.startswith(b"474946383761") or currSector.startswith(b"474946383961"):
                currFile = b""
                while not currSector.__contains__(b"003b"):
                    currFile += currSector
                    currSector = binascii.hexlify(file.read(512))
                byteList = [b'%c' % i for i in currSector]
                print(len(byteList))
                for element in range(0, len(byteList)):
                    if element % 2 == 0 and byteList[element] == b'0' and byteList[element + 1] == b'0' and byteList[element + 2] == b'3' and byteList[element + 3] == b'b':
                        currFile += byteList[element] + byteList[element + 1] + byteList[element + 2] + byteList[element + 3]
                        break
                    currFile += byteList[element]
                print(currFile)
                gif = open('gif' + str(currentfile) + '.gif', 'wb')

                gif.write(binascii.unhexlify(currFile))
                currentfile += 1;

            if currSector.startswith(b"ffd8"):
                currFile = b""
                while not currSector.__contains__(b"ffd9"):
                    currFile += currSector
                    currSector = binascii.hexlify(file.read(512))
                byteList = [b'%c' % i for i in currSector]
                print(len(byteList))
                for element in range(0, len(byteList)):
                    if element % 2 == 0 and byteList[element] == b'f' and byteList[element + 1] == b'f' and byteList[element + 2] == b'd' and  byteList[element + 3] == b'9':
                        currFile += byteList[element] + byteList[element + 1] + byteList[element + 2] + byteList[
                            element + 3]
                        break
                    currFile += byteList[element]
                jpg = open('jpg' + str(currentfile) + '.jpg', 'wb')
                jpg.write(binascii.unhexlify(currFile))
                currentfile += 1;
            # if currSector.startswith(b"504b030414000600"):
            #     print("DOCX " + str(currSector))
            # #if currSector.startswith(b"FFD8"):
            # #    print("AVI " + str(currSector))
            if currSector.startswith(b"89504E47"):
                # currFile = b""
                # currFile += currSector
                # while not currSector.__contains__(b"49454e44ae426082"):
                #     if currSector == b'':
                #         break
                #     currFile += currSector
                #     currSector = file.read(512)
                print("PNG " + str(currSector))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
