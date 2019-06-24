import cs50

# gets height from user and makes sure it is within bounds
while True:
    print("Enter height of the half pyramid (please pick a number between 1 and 8)")
    Height = cs50.get_int()
    if Height >= 1 and Height <= 8:
        break

# prints pyramid
for i in range(Height):
    print(" " * (Height - i - 1), end="")
    print("#" * (i + 1), end="")
    print()
