import math


# First practice function
def reverseList(list1):
    revList = []
    length = len(list1)
    for i in list1:
        revList.append(list1[length - 1])
        length -= 1

    return revList


# Second practice function
def maxElement(list1):
    maxE = 0
    for i in list1:
        if maxE < i:
            maxE = i

    return maxE


# Third practice function
def oddList(list1):
    oddL = []
    for i in list1:
        if (list1[i - 1] % 2) != 0:
            oddL.append(list1[i - 1])

    return oddL


# Fourth practice function
def euclideanList(list1, list2):
    dist = math.sqrt(math.pow(list2[0] - list1[0], 2) + math.pow(list2[1] - list1[1], 2))
    return dist


# Fifth  practice function
def listFile(name):
    lines = name.readlines()
    output = []
    for i in lines:
        output.append(i)
    return output


# Sixth practice function
def writeFile(name, list1):
    for x in list1:
        name.write(str(x) + "\n")


# These are the variables that are plugged into the functions
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
euList1 = [-5, 7]
euList2 = [3, -8]
read = open("listRead.txt", "r")  # I made a .txt file it reads from that has animal names, called listRead.txt
write = open("listWrite", "w+")

# This is where i call each of the functions in the same order they are given
newList = reverseList(a)
maxValue = maxElement(a)
odd = oddList(a)
euDist = euclideanList(euList1, euList2)
fileOutput = listFile(read)
writeFile(write, a)

# This is the output of each of the called functions in the same output that they are given
print("\nThe reverse list is: " + str(newList))
print("\nThe max number in the list is " + str(maxValue))
print("\nThe odd numbers in the list are: " + str(odd))
print("\nThe euclidean distance between " + str(euList1) + " and " + str(euList2) + " is " + str(euDist))
print("\nThe output of the text file is: " + str(fileOutput))


# part 2, classes.
class BankAccount:

    def __init__(self, ID, initialDeposit):
        self.member = ID
        self.balance = initialDeposit

    def deposit(self, depositAmount):
        self.balance += depositAmount
        return self.balance

    def withdraw(self, withdrawAmount):
        self.balance -= withdrawAmount
        return self.balance


# Outputs the starting balance, balance after deposit and withdraw for both accounts.
account1 = BankAccount(1159, 20000)
print("\nAccount 1 starting balance:       " + str(account1.balance))
print("Account 1 balance after deposit:  " + str(account1.deposit(6542)))
print("Account 1 balance after withdraw: " + str(account1.withdraw(3840)))

account2 = BankAccount(9859, 1600)
print("\nAccount 2 starting balance:       " + str(account2.balance))
print("Account 2 balance after deposit:  " + str(account2.deposit(369)))
print("Account 2 balance after withdraw: " + str(account2.withdraw(1594)))

