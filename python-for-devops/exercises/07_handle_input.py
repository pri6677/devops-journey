# ask user for number but if user enters a string, say please enter a valid number

try:
    number = int(input("Enter a number: "))
    print(number)
except ValueError:
    print("Please enter a valid number")