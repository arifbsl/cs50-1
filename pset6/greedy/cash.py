import cs50

# Gets Change from user, makes sure it's a positive number
while True:
    print("Change owed in dollars (ex: 9.75): ", end="")
    Change = cs50.get_float()
    if Change >= 0.00:
        break


# converts float to integer
Change = int(Change*100)

# counts quarters and updates Change
quarters = Change // 25
Change %= 25

# counts dimes and updates Change
dimes = Change // 10
Change %= 10

# counts nickels and updates Change
nickles = Change // 5
Change %= 5

# counts pennies and updates Change
pennies = Change // 1
Change %= 1

# prints smallest number of coins given back
print(quarters + dimes + nickles + pennies)