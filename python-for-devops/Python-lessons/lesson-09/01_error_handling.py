try:
    number = int(input("Enter a number: "))
    print(f"You entered: {number}")

except ValueError:
    print("ERROR: Please enter a valid number")