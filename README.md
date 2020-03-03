## requirement
python after 3.7

## Installation
intall gui dependency [pygubu](https://github.com/alejandroautalan/pygubu) by command
```
pip3 install -r requirements.txt
```

# Usage
To run server with gui, command
```
python3 run_server_gui.py
```

To run client Example(sending timestamp message)
```
python3 run_client.py
```

![GIF 2020-03-03 오후 3-35-21](https://user-images.githubusercontent.com/21076531/75749210-a4219b00-5d64-11ea-9734-2e5ce26c9fba.gif)


## Implement Client Side
You need to implement a UDP broadcast socket that finds a remote-logger server on your local network.
Once you find the server, connect the TCP socket to the server IP. Then send a Json byte string with the following format.
```
{"message": "log message something", "type": 0, "timestamp": 1583207428}
```
type: 0 = Debug, 1 = Warning, 2 = Error.

### Example

See ClientExample.py for the Python client implementation.

See UnityClientExample.cs for the Unity client implementation.



