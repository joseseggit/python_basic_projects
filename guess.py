import random

limit = 20
n1 = random.randrange(limit)
while True:
    u_choice = int(input("What's your guess? "))
    if u_choice == n1:
        break
    elif u_choice < n1:
        print("Sorry. Try higher.")
    else:
        print("Sorry. Try lower.")
print("You did it!")