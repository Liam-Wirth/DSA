#!/usr/bin/env python3

#constraints: nums.length == 2 * n
# 1 <= n <= 500
# 1 <= nums[i] <=500

restri = 20

from random import random


def genTest() -> list[int]:
    n = random() # n is a float 0 -> 1
    n *= restri
    n = int(n) + 1
    nums: list[int] = [0] * (2*n)
    for i in range(len(nums)):
        nums[i] = int(random() * restri)
    return nums


from divide import Solution


sol = Solution()
nums = genTest()
print(sol.divideArray(nums))

numtrue = 0
sep = '-' * 10

trues = [] * 10
numfalse = 0
while numtrue < 10:
    print(sep)
    nums = genTest()
    # print(nums)
    truth = sol.divideArray(nums)
    print(f"{truth} | {numfalse + numtrue} ")
    if truth:
        numtrue+=1
        trues.append(nums)
    else:
        numfalse += 1

print(trues)

print(f"numfalse: {numfalse}")



