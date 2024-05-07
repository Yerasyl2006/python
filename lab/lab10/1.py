import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost",
    database="labs",
    user="postgres",
    password="12345678",
    port="5432"
)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Phonebook(
            surname VARCHAR(255) ,
            name VARCHAR(255),
            number INT
            );  
            """)
conn.commit()

def update(sn, mode, newv):
    cur.execute("""UPDATE PhoneBook
    SET {} = '{}'
    WHERE surname = '{}'
    """.format(mode, newv, sn))
    conn.commit()

def delete(sn):
    cur.execute("""DELETE FROM Phonebook
    WHERE surname='{}'
    """.format(sn))
    conn.commit()



mode = "enter"
while True:
    print("Type 'enter' if you want to add more data and type 'stop' to break")
    mode = input()
    if mode == "stop":
        break
    mytuple = []
    print("enter surname:")
    mytuple.append(input())
    print("enter name:")
    mytuple.append(input())
    print("enter number:")
    mytuple.append(input())
    mytuple = tuple(mytuple)
    cur.execute("""INSERT INTO PhoneBook (surname, name ,number) VALUES
    {};
    """.format(mytuple))
    conn.commit()

while True:
    print("Want to insert data from csv file? yes/no:")
    mode = input()
    if mode == "no":
        break
    print("enter the name of the file")
    mode = input()
    with open(mode + '.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute("INSERT INTO PhoneBook VALUES (%s,%s,%s)", row)
            conn.commit()


while True:
    print("Type 'update' to update some data or 'stop' to break")
    mode = input()
    if mode == "stop":
        break
    cur.execute("""SELECT * FROM PhoneBook""")
    print(cur.fetchall())
    print("Enter surname")
    idtochange = input()
    print("What you want to change? name/number")
    mode = input()
    print("Enter new name/number")
    newvalue = input()
    update(idtochange, mode, newvalue)


while True:
    print("want to delete some data? yes/no")
    mode = input()
    if mode == "no":
        break
    cur.execute("""SELECT * FROM PhoneBook""")
    print(cur.fetchall())
    print("Enter surname")
    idtodelete = input()
    delete(idtodelete)
    conn.commit()

cur.close()
conn.close()