"""
conditions where it is simply impossible to do it
"aaab" reasoning:
there is no way to be able to space out the a's because they take up more than (maybe the number is half?) of the string



so a fail case I'm Identifying would be "amt of any char c is > half len(s)"




"""
from heapq import *
from heapq import _heapify_max
from queue import PriorityQueue


def organize(s: str) -> str:
    # not gonna use prio q anynmore we gonna python swag it
    h = []
    chrs = {}
    for c in s:
        if c in chrs:
            chrs[c] += 1
        else:
            chrs[c] = 1
        if chrs[c] > len(s) /2:
            return ""
    print(chrs)

    for (c, i) in chrs.items():
        heappush(h, (c,i))


    out = [None] * len(s) #LET ME COOK
    pos = 0

    while h: # will drain the heap from back to front
        (c,i) = heappop(h)
        dontpush = False
        if i <= 1:
            dontpush = True
        if not out[pos]:
            out[pos] = c
            i -= 1
            pos +=2
            pos %=len(s)
        else: # something there
            pos += 1 # we'll try on the next loop
            pos %=len(s)
            dontpush = False
        if not dontpush:
            heappush(h, (c,i))

    ret = str(out)       

    return ret

print(f"the one on my paper {organize('aaabbccdde')}")
print(f"ff {organize('ff')}")
print(f"aaab {organize('aaab')}")
print(f"aaab {organize('aaab')}")
evil = "aaaabbccccddeffffghhhijkkkklmmmmmmmmmnoppppqqqqqqqqrrsssssttteeeffffgggggggggggggggggggghhhhiijjjjkkkklllmmmnnnnnnooopppqqqqqqrrrssssttttttttuuuvvvvvvvwwwwxxxyyyyyyyzzzzzzzzzzzz"
print(f"the fucked one: {organize(evil)}")


