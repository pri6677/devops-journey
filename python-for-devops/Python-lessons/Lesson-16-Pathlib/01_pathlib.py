from pathlib import Path
#Printing name of the path
path = Path("server.log")

print(path)

# checking if the path is file or dir, gives true and false result
print(path.is_file())
print(path.is_dir())

#Printing the current working directory
from pathlib import Path

current = Path.cwd()

print(current)

#Printing the Home directory
from pathlib import Path

home = Path.home()

print(home)

