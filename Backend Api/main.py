from time import time
from flask import Flask, jsonify, request
import sqlite3, socket
from datetime import datetime
from flask_cors import CORS

IPAddr = socket.gethostbyname(socket.gethostname())  
port = 5000
app = Flask(__name__)
CORS(app)

conn = sqlite3.connect('test.db')
c = conn.cursor()
total = len(c.execute("SELECT * FROM Attendance ").fetchall())
conn.close()

@app.post("/")
def home():
    data = request.get_json()
    # print(data)

    name = data["name"]
    Hex_id = data["Hex_id"]
    Dec_id = data["Dec_id"]
    Roll_no = data["Roll_No"]
    post = data["post"]
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Attendance(
                    name text,
                    Hex_id text,
                    Dec_id text,
                    Roll_No int,
                    post text, 
                    day text,
                    time text)
                    """)
    day = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    print(isPresent(Hex_id, day))
    if isPresent(Hex_id, day):
        # print("details recd:",name,Hex_id, Dec_id, Roll_no, post)
        c.execute("INSERT INTO Attendance VALUES (?,?,?,?,?,?,?)", (name, Hex_id, Dec_id, Roll_no, post,day ,time))
        conn.commit()
        conn.close()
        return (data)
    else:
        conn.commit()
        conn.close()
        return ("t")
    
@app.post("/data")
def data():
    received = request.get_json()
    print(received)
    # conn = sqlite3.connect('test.db')
    # c = conn.cursor()
    # last_entry = c.execute("SELECT * FROM Attendance WHERE rowid = (SELECT MAX(rowid) FROM Attendance)").fetchall()
    # newtotal = len(c.execute("SELECT * FROM Attendance ").fetchall())
    # conn.close()
    # if newtotal>total:
    #     total=newtotal
    #     newtotal+=1
    #     if last_entry[5]==datetime.now().strftime("%Y-%m-%d"):
    #         return {"lastid": last_entry}
    #     else:
    #         return {"lastid": "nolast"}
    # else:
    return {"lastid": "nolast"}

def isPresent(Hex_id, day): 
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    try:
        Data = c.execute("SELECT * FROM Attendance WHERE Hex_id = ? AND day =?", (Hex_id,day)).fetchone()
        Valid = c.execute("SELECT * FROM Students WHERE Rfid_Hex = ?", (Hex_id,)).fetchone()
        print("data is:",type(Data))
        if (Data==None):
            return True
        else:
            return False
    except:
       return False

@app.post("/signin")
def signIn():
    email = request.get_json().get("email")
    password = request.get_json().get("password")
    if isValid(email, password):
        return jsonify(isValid(email,password)) 
    else:
         return jsonify({"status": "Error logging in"})

def isValid(email, password): 
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    Data = c.execute("SELECT * FROM loginDetails WHERE email = ? AND password = ?", (email, password)).fetchall()
    if (Data==[]):
        return {"status": "Error logging in"}
    else:
        if (email==Data[0][2] and password==Data[0][3]):
            conn.close()
            print(Data)
            return Data
        else:
            conn.close()
            return False

@app.post("/signup")
def signUp():
    data = request.get_json()
    print(data)

    name = data["name"]
    Hex_id = data["Hex_id"]
    Dec_id = data["Dec_id"]
    Roll_no = data["Roll_No"]
    post = data["post"]
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Students(
                    Name text,
                    Rfid_Hex text,
                    Rfid_Dec text,
                    Roll_no int,
                    Post text,
                    gender text,
                    email text)
                """)
    c.execute("INSERT INTO Students VALUES (?,?,?,?,?)", (name, Hex_id, Dec_id, Roll_no, post))
    conn.commit()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.debug=True  
    app.run(host=IPAddr, port=port)