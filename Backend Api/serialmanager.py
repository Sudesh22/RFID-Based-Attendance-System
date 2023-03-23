import serial, sqlite3, requests
from main import IPAddr, port

ser = serial.Serial('COM6', 115200, timeout=2)

while(1):
    x = ser.readline().decode().lstrip("/r, /n")
    # print(x)
    try:
        if x.startswith("In hex:"):
            hexval = x
            print(hexval)
            list_ = hexval.split("  ")
            hex_db = list_[1].lstrip("/r, /n")[0:-2]
            # print("a"+hex_db+"a")
            conn = sqlite3.connect('test.db')
            c = conn.cursor()
            data = c.execute("SELECT * from Students WHERE Rfid_Hex = ?", (hex_db,)).fetchone()
            print(data)
            conn.close()
            requests.post("http://"+IPAddr+":"+str(port), json = {"name": data[0], "Hex_id": data[1], "Dec_id": data[2], "Roll_No": data[3], "post": "student"}).status_code
    except:
        requests.post("http://"+IPAddr+":"+str(port), json = {"error": "User not in Database!"}).status_code