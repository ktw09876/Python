import random

lot_num = []

def lotto():
    num = random.randint(1,45)    
    return num

count = 0

while True:
    getRandNo = lotto()
    if getRandNo not in lot_num:
        lot_num.append(getRandNo)
    count = count + 1
    if count > 5:
        break

print(lot_num)

