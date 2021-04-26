#!/usr/bin/python3
import sys
import string
import time
import itertools

def outputResult(start):
    print("Cracked Password: ", crackedPwd)
    endTime = time.time()
    elapsedTime = endTime - startTime
    hours = 0
    minutes = 0
    if(elapsedTime > 3600) :
        hours = elapsedTime // 3600
        elapsedTime = elapsedTime - 3600 * hours
    if(elapsedTime > 60) :
        minutes = elapsedTime // 60
    seconds = elapsedTime - 60 * minutes 

    print("Elapsed time: %d hours, %d minutes, %.2f seconds"  %(hours, minutes, seconds))
    return [hours, minutes, seconds]

def checkPermutations(password, permutations):
    result = 0
    for p in permutations: 
        if ''.join(p) == password:
            result = ''.join(p)
            break
    return result

args = sys.argv 
length = len(args[1])
inputPwd = args[1]
userpwd = bytes(args[1] + '\n', 'utf-8')
pwdType = args[2] # 1 = lowercase, 2 = lowercase + digit, 3 = alphanumeric, 4 = 

#Read password list file and initialize cracked password 
crackedPwd = 0
pwds = open("./rockyou.txt", "rb")

startTime = time.time()
# Iterate through password list searching for given password
print("Searching list for password . . . ")
for p in pwds:
    if(p == userpwd) :
        crackedPwd = p.decode('utf-8')
        break
pwds.close()

# If password found, calculate and display the amount of time it took
if(crackedPwd) :
    time = outputResult(startTime)
    f = open("./results.txt", "a")
    f.write("Character set: %s \t Pwd Length: %d \t Pwd: %s \t Time: %d: %d: %.2f \n" 
            %(pwdType, length, inputPwd, time[0], time[1], time[2]))
    f.close()
    sys.exit()
else:
    print("Password not on list. Initializing brute force . . . ")

# If the password doesn't exist on the list, try brute force

#lowercase
if(pwdType == '1') :
    permutations = itertools.product(string.ascii_lowercase, repeat=length)
    crackedPwd = checkPermutations(inputPwd, permutations)
# lowercase and digit
if(pwdType == '2'):
    permutations = itertools.product(string.ascii_lowercase + string.digits, repeat=length)
    crackedPwd = checkPermutations(inputPwd, permutations)
# alphanumeric
if(pwdType == '3'):
    permutations = itertools.product(string.ascii_letters + string.digits, repeat=length)
    crackedPwd = checkPermutations(inputPwd, permutations)
# printable
if(pwdType == '4'):
    permutations = itertools.product(string.printable, repeat=length)
    crackedPwd = checkPermutations(inputPwd, permutations)

if(crackedPwd):
    time = outputResult(startTime)
    f = open("./results.txt", "a")
    f.write("Character set: %s \t Pwd Length: %d \t Pwd: %s \t Time: %d: %d: %.2f \n" 
            %(pwdType, length, crackedPwd, time[0], time[1], time[2]))
    f.close()
else:
    print("Password not found.")
    sys.exit()