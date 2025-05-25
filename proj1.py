def toNeg(len: int, num: int) -> str:
    arr = [0] * len
    num = num -1
    i = 0
    while i < len:
        arr[i] = (num+1) % 2
        i += 1
        num = num // 2
        
    return str(arr[::-1])


def encrypt( key: int):
        file = open("encrypted.txt", "r")
        data = file.read()
        file.close()
        file = open("encrypted.txt", "w")
        for char in data:
            file.write(chr(ord(char) ^ key))
        file.close()