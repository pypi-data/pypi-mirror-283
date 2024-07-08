import socket
import unpack_data2

IP = "192.168.4.100"
PORT = 8080
ADDR = (IP, PORT)
SIZE = 1024
MAX_BUF_SIZE = 1048576

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
            msgToSend = "1 LASServer SendData\n"
        elif msgToSend == "q":
            connected = False

        encodedString = msgToSend.encode()

        if msgToSend == "1 LASServer SendData\n":
            client.send(encodedString)
            print(f"[SENT] {msgToSend}")

            #get all data
            data = client.recv(MAX_BUF_SIZE)
            #data = bytearray(unpack_data.test_data)
            #print(data)

            '''
            print("Raw bytes:", end="")
            for byte in data:
                print(f"\\x{byte:02x}", end="")
            print()
            '''

            binary_payload = b''
            is_binary_payload = False
            #cut text part
            bytes_to_newline = 0
            for byte in data:
                bytes_to_newline += 1
                if byte == 10:
                    break
                if is_binary_payload:
                    binary_payload += byte.to_bytes()
                if byte == 61:
                    is_binary_payload = True
            print()

            #server response
            cut = data[:bytes_to_newline]
            
            '''
            for byte in cut:
                print(f"\\x{byte:02x}", end="")
                print(byte)
            print()
            '''

            print(f"Server Response: {cut.decode()}")            

            data = data[bytes_to_newline:]

            if data == b'':
                print("No data")
                continue

            if len(data) != int(binary_payload.decode()):
                print("Error: Binary payload does not match received data. Continuing run...")
                
            '''
            print("Raw byte data:", end="")
            for byte in data:
                print(f"\\x{byte:02x}", end="")
            print()
            '''
            
            '''
            #remove everything not F-12
            byte = 3
            while byte < len(data):
                if data[byte] < 15 or data[byte] > 18:
                    print(f"Removing data: {data[byte-3:byte+1]}")
                    data = bytearray(data)
                    del data[byte-3:byte+1]
                    byte -= 4
                byte += 4
            
            print("Raw byte Post-cuts:", end="")
            for byte in data:
                print(f"\\x{byte:02x}", end="")
            print()
            '''

            unpack_data2.handle_ions(data)
            
    
    client.close()
    print("[DISCONNECTED] Client disconnected.")

if __name__ == "__main__":
    main()
