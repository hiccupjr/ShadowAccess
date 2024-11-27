
# Python Reverse Shell Backdoor
This is a simple Python script that establishes a R]reverse shell connection with a remote attacker. This only for education purpose. The Backdoor listens for incoming connections on a specified port and allows the attacker to execute system commands remotely.
 


## Features

- Reverse Shell connection
- Command execution
- File transfer
- Stealthy
- Auto restart


## Tech Details:
    1. Programming language: Python
    2. Operating system: Cross-platform (windows,Linux,macOs),
       but you have to modify persistence method.
    3. Port: Configurable (default is 4444)
    4. Protocol: TCP  
## Architecture
The backdoor consists of two main components:

    1. Server-side (Attacker's machine): A Python
       script that listens for incoming connections from 
       the compromised machine.
    
    2. Client-side (compromised machine): A Python
       script that estblishes a connection with the 
       attacker's machine and awaits for commands.