# tcp-chat-server
tcp-chat-server
Co-lab Nick Damberg, J Christie

# Version
- Version 1.0.0

# Use
- 

# Features
## Version 1.0.0
- [X]Create a TCP Server using the Python standard socket module
- [X]The server should be running on an individual thread using the threading module in Python
- [X]Create a Client class that models an individual connection, and exists as a module in your application
- [X]Each client instance should contain at least an id, nickname, and socket conn and addr
- [X]Each client instance should be started on an individual thread using the threading module in Python
- [X]Clients should be able to send messages to all other clients by sending it to the server without a special command
- [ ]Clients should be able to run special commands by sending messages that start with a command name, for example:
  - [ ]The client should send @quit to disconnect (this should not stop the server… only the client that invoked @quit)
  - [X]The client should send @list to list all connectued users
  - [X]The client should send @nickname <new-name> to change their nickname
  - [ ]The client should send @dm <to-username> <message> to send a message directly to another user by nickname
- [ ]Connected clients should be maintained as an in memory collection on the server instance called the client_pool
- [X]When a socket emits the close event, the socket should be removed from the client_pool
- [?]When a socket emits the data event, the data should be logged on the server and the commands below should be implemented
 - there was nothing below this in the instructions.

## Change Log

### 2018-08-20
- Created wire frame
- Created new branch class-06-tcp-chat
- @list prints all connected users.
- User is removed from client_pool when quitting.
- @nickname "new-name" allows user to change their screen name.
- updated readme
- Attempted to get @dm working, close but no cigar.



# Software
- Linux
```
  sudo apt-get install python3-pip
  sudo pip install --upgrade pip
  pip install --user pipenv
  sudo -H pip install -U pipenv
  pipenv --three
  pipenv shell
  pipenv install pytest
  pytest -v
  pipenv install uuid

  #to remove env
  pipenv --rm

  #to check pipenv
  pipenv check
```