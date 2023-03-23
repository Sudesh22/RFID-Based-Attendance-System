import sqlite3, socket

conn = sqlite3.connect('test.db')
c = conn.cursor()
# c.execute("""CREATE TABLE IF NOT EXISTS LoginDetails(
#                 id integer primary key,
#                 name text,
#                 email text,
#                 password text)
#             """)

# c.execute("INSERT INTO Students VALUES (?,?,?,?,?,?,?)", ("Castro", "D9 14 2B B9", "217 20 43 185", 4, "student", "Male", "CastroN@gmail.com"))
# c.execute("INSERT INTO LoginDetails VALUES (?,?,?,?)", (1, "abc", "abc@gmail.com", "abc@123"))
# print(c.execute("SELECT * FROM Attendance WHERE rowid = (SELECT MAX(rowid) FROM Attendance)").fetchall())
print(len(c.execute("SELECT * FROM Attendance ").fetchall()))
conn.commit()
conn.close()

def delete_table(name):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("DROP TABLE " + name)
    conn.commit()
    conn.close()

def delete(name,id):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("DELETE from " + name + " WHERE rowid = ?", (id,))
    conn.commit()

# delete("Attendance", 4) 
# delete_table('Attendance')