
import sys

def readFile(loc:str) -> str:
    try:
        with open(loc, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {loc}")
        return None

punc = [',', '.', '!', '?', ';', ':', '-', '_', '(', ')', '[', ']', '{', '}', '`', '~', "\t", "\n","' ", '"', " '"]

txt = readFile(input("Enter the file location: ")).lower()

for char in punc:
    txt = txt.replace(char, ' ')

words = [i for i in txt.split(' ')]

word_counter = {}

for word in words:
    word_counter[word] = word_counter.get(word,0) + 1
    
word_counter = {k: v for k, v in word_counter.items() if k not in punc and k != ''} 


most_common = sorted(word_counter.items(), key=lambda x: x[1], reverse=True)

print("Most common words:")
for word, count in most_common[:int(sys.argv[1])]:
    print(f"{word.capitalize()}: {count}")