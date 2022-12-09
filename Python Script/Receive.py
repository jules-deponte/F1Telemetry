import socket
import pandas as pd


UDP_IP = "127.0.0.1"
UDP_PORT = 20777

sock = socket.socket(
    socket.AF_INET, # Internet
    socket.SOCK_DGRAM
) # UDP


sock.bind(('', UDP_PORT))
df = pd.DataFrame(columns=['data'])

l = []
i = 0

while True:
    data, addr = sock.recvfrom(4096) # buffer size is 1024 bytes
    print("received message: %s" % data)


    i = i + 1

    d = {'data':data}

    df = df.append(d, ignore_index=True)

    if i % 1000 == 0:
        print(df)
        df.to_csv(r'C:\Users\jules\OneDrive\F1 2021 Telemetry\Python Script\data.csv', index=False)