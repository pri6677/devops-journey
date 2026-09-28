# Print all the server whose status is running

servers ={
    "web-01": "running",
    "web-02": "stopped",
    "db-01": "running",
}

for server in servers:
    if servers[server] == "running":
     '''
     In Python, curly braces {} are used to define dictionaries or sets. 
     To access or look up a value by its key in a dictionary, you must use square brackets [].
    ''' 


print(servers)