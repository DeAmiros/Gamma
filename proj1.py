def toNeg(length: int, num: int) -> str:
    bin_num = bin(num - 1)[2:]
    if length < len(bin(num)) - 2:
        raise Exception("Length is less than the binary representation of the number.")
        
    return ("".join('1' if i == '0' else '0' for i in bin_num.zfill(length)))

print(toNeg(int(input("Enter the length of the num: ")), int(input("Enter the number to be converted: "))))

# Bonus Task: Encrypt a file using XOR encryption

def encrypt( key: int):
        file = open("encrypted.txt", "r")
        data = file.read()
        file.close()
        file = open("encrypted.txt", "w")
        for char in data:
            file.write(chr(ord(char) ^ key))
        file.close()