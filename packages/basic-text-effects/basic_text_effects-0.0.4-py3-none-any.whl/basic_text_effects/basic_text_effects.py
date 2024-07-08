import time
import random
import math

def _sigmoid(x):
    return 1 / (1 + math.exp(-x))

def _clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

def _linearCurve(x):
    return x

def print_continuous(text, speed=1):
    lines = text.split('\n')
    for line in lines:
        for i in range(len(line)+1):
            current_text = line[:i]
            print("\r" + current_text, end="")

            time.sleep(random.uniform(0.03 / speed, 0.2 / speed))
            
        print("")
        
def print_word_by_word(text, speed=1):
    lines = text.split('\n')
    for line in lines:
        words = line.split(" ")
        for i in range(len(words)+1):
            current_text = " ".join(words[:i])
            print("\r" + current_text, end="")

            time.sleep(random.uniform(0.10 / speed, 0.4 / speed))
        
        print("")

def print_wobbly(text, speed=1):
    charset = list('abcdefghijklmopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    lines = text.split('\n')
    for line in lines:
        for i in range(len(line)+1):
            previous = line[:i]
            last = "".join(list(map(lambda c: random.choice(charset) if c != ' ' else ' ', line[i:])))
            print("\r" + previous + last, end="")

            time.sleep(random.uniform(0.03 / speed, 0.2 / speed))
            
        print("")

def print_wobbly_continuous(text, speed=1):
    charset = list('abcdefghijklmopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    lines = text.split('\n')
    for line in lines:
        line_length = len(line)
        progress_show = 0
        i = 0
        while progress_show < line_length:
            ratio = i / line_length
            progress_show = int(_clamp(_linearCurve(ratio - 0.5), 0, 1) * line_length)
            progress_reveal = int(_clamp(_linearCurve(ratio), 0, 1) * line_length)
            
            revealed = line[:progress_reveal]
            previous = revealed[:progress_show]
            last = "".join(list(map(lambda c: random.choice(charset) if c != ' ' else ' ', revealed[progress_show:])))
            print("\r" + previous + last, end="")

            time.sleep(random.uniform(0.03 / speed, 0.2 / speed))
            i += 1
            
        print("")
        
def print_dotted(text, speed=1):
    lines = text.split('\n')
    for line in lines:
        line_length = len(line)
        progress_show = 0
        i = 0
        while progress_show < line_length:
            ratio = i / line_length
            progress_show = int(_clamp(_linearCurve(ratio - 0.5), 0, 1) * line_length)
            progress_reveal = int(_clamp(_linearCurve(ratio), 0, 1) * line_length)
            
            revealed = line[:progress_reveal]
            previous = revealed[:progress_show]
            
            revealed_mapped = []
            for ind in range(len(revealed[progress_show:])):
                char = revealed[progress_show:][ind]
                if char == ' ':
                    revealed_mapped.append(char)
                else:
                    print_double_dot = (ind + i) % 3 == 0
                    revealed_mapped.append(":" if print_double_dot else ".")
                
            last = "".join(revealed_mapped)
            print("\r" + previous + last, end="")

            time.sleep(random.uniform(0.03 / speed, 0.2 / speed))
            i += 1
            
        print("")