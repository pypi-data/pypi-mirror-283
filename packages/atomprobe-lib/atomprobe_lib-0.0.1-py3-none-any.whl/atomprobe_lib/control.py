import socket

IP = "192.168.4.100"
PORT = 1000
ADDR = (IP, PORT)
SIZE = 1024

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    connreadStatsMsg = client.recv(SIZE).decode()
    print(f"[SERVER] {connreadStatsMsg}")

    connected = True
    while connected:
        #Commands: 1 LASControl HV SET SPECIMEN VOLTS xxxx
        #1 LASControl ACQ AUTO VOLT ENA FALSE/TRUE
        userInput = input("Client: ")
        if userInput == "volts":
            userInput = input("Enter volts: ")
            msg = f"1 LASControl HV SET SPECIMEN VOLTS {userInput}\n"
        elif userInput == "auto volt":
            userInput = input("True/False: ")
            msg = f"1 LASControl ACQ AUTO VOLT ENA {userInput}\n"
        else:
            msg = userInput

        encodedString = msg.encode()
        

        if msg == "!q":
            connected = False
        elif msg.startswith("1 LASControl"):
            client.send(encodedString)
            print(f"[SENT] {msg}")
            
            data = client.recv(SIZE)
            print(data.decode())

    client.close()
    print("[DISCONNECTED] Client disconnected.")

if __name__ == "__main__":
    main()
