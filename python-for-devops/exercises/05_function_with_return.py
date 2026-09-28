# Create a function that takes a server name as a parameter and returns the server name

def check_cpu(cpu):
    if cpu > 80:
        return "High"
    else:
        return "Normal"


result = check_cpu(85)

print(result)



# difference between return and print
'''
def check_cpu(cpu):
    if cpu > 80:
        return "High"
    else:
        return "Normal"


result = check_cpu(85)

print(result)
'''

# KEY DIFFERENCE: return vs print
#
# print()  -> DISPLAY ONLY
#   - Shows output on the screen for human eyes.
#   - Does NOT hand data back to the program.
#   - Evaluates to None if saved to a variable.
#
# return   -> PASS DATA BACK
#   - Sends a value back to where the function was called.
#   - Saves the result into a variable (like `result = check_cpu(85)`).
#   - Exits the function immediately when executed.



