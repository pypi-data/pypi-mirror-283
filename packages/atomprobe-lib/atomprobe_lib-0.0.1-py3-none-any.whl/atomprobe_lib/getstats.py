import socket
import unpack_stats

IP = "192.168.4.100"
PORT = 8080
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
        msgToSend = input("Client: ")
        if (msgToSend == ""):
            msgToSend = "1 LASServer SendStats\n"
        elif msgToSend == "q":
            connected = False
            
        encodedString = msgToSend.encode()
            
        if msgToSend == "1 LASServer SendStats\n":
            client.send(encodedString)
            print(f"[SENT] {msgToSend}")

            #cut first 43 bytes
            cut = client.recv(43)
            print(cut.decode())
            
            binary_data = client.recv(1024)

            str = unpack_stats.start(binary_data)
            print(str)

    client.close()
    print("[DISCONNECTED] Client disconnected.")

if __name__ == "__main__":
    main()
