import cs50

# asks user for height for pyramid and also makes sure that height is within bounds
while True:
    print("Enter height of the pyramid (please pick a number between 1 and 8, inclusive)")
    Height = cs50.get_int()
    if Height >= 1 and Height <= 8:
        break

# makes the pyramid
for i in range(Height):
    print(" " * (Height - i - 1), end="")
    print("#" * (i + 1), end="")
    print("  ", end="")
    print("#" * (i + 1), end="")
    print()
