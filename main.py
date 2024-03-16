import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect("hostel_management.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_n (
        roll_no INTEGER PRIMARY KEY,
        student_name TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_ph1 (
        roll_no INTEGER PRIMARY KEY,
        student_phone1 INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_ph2 (
        roll_no INTEGER PRIMARY KEY,
        student_phone2 INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_r (
        roll_no INTEGER PRIMARY KEY,
        student_room_no INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaint_table (
        complaint_no INTEGER PRIMARY KEY,
        roll_no INTEGER,
        FOREIGN KEY (roll_no) REFERENCES student_n(roll_no)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaint_info (
        complaint_no INTEGER PRIMARY KEY,
        description TEXT,
        complaint_type TEXT,
        FOREIGN KEY (complaint_no) REFERENCES complaint_table(complaint_no)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS mess_table (
        sr_no INTEGER PRIMARY KEY,
        roll_no INTEGER,
        FOREIGN KEY (roll_no) REFERENCES student_n(roll_no)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS mess_info (
        sr_no INTEGER PRIMARY KEY,
        feedback TEXT,
        FOREIGN KEY (sr_no) REFERENCES mess_table(sr_no)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS laundry_table (
        sr_no INTEGER PRIMARY KEY,
        roll_no INTEGER,
        FOREIGN KEY (roll_no) REFERENCES student_n(roll_no)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS laundry_info (
        sr_no INTEGER PRIMARY KEY,
        given_on DATE,
        received_on DATE,
        completed TEXT,
        FOREIGN KEY (sr_no) REFERENCES laundry_table(sr_no)
    )
""")

# Define procedures
def insert_data(roll, name, phone1, phone2, room):
    cursor.execute("INSERT INTO student_n (roll_no, student_name) VALUES (?, ?)", (roll, name))
    cursor.execute("INSERT INTO student_ph1 (roll_no, student_phone1) VALUES (?, ?)", (roll, phone1))
    cursor.execute("INSERT INTO student_ph2 (roll_no, student_phone2) VALUES (?, ?)", (roll, phone2))
    cursor.execute("INSERT INTO student_r (roll_no, student_room_no) VALUES (?, ?)", (roll, room))
    conn.commit()

def add_complaint(c_no, roll, disc, c_type):
    cursor.execute("INSERT INTO complaint_table (complaint_no, roll_no) VALUES (?, ?)", (c_no, roll))
    cursor.execute("INSERT INTO complaint_info (complaint_no, description, complaint_type) VALUES (?, ?, ?)", (c_no, disc, c_type))
    conn.commit()

def add_mess(sno, roll, feed):
    cursor.execute("INSERT INTO mess_table (sr_no, roll_no) VALUES (?, ?)", (sno, roll))
    cursor.execute("INSERT INTO mess_info (sr_no, feedback) VALUES (?, ?)", (sno, feed))
    conn.commit()

def add_laundry(sno, roll, g_date, r_date, comp):
    cursor.execute("INSERT INTO laundry_table (sr_no, roll_no) VALUES (?, ?)", (sno, roll))
    cursor.execute("INSERT INTO laundry_info (sr_no, given_on, received_on, completed) VALUES (?, ?, ?, ?)", (sno, g_date, r_date, comp))
    conn.commit()

def update_laundry(sno, comp):
    cursor.execute("UPDATE laundry_info SET completed = ? WHERE sr_no = ?", (comp, sno))
    conn.commit()

def retrieve(roll):
    cursor.execute("SELECT student_name FROM student_n WHERE roll_no = ?", (roll,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return "Sorry, no data found."
def show_all_data():
    # Display student data
    cursor.execute("SELECT * FROM student_n")
    print("\nStudent Data:")
    for row in cursor.fetchall():
        print(row)

    # Display complaint data
    cursor.execute("SELECT * FROM complaint_table")
    print("\nComplaint Data:")
    for row in cursor.fetchall():
        print(row)

    # Display mess feedback data
    cursor.execute("SELECT * FROM mess_info")
    print("\nMess Feedback Data:")
    for row in cursor.fetchall():
        print(row)

    # Display laundry request data
    cursor.execute("SELECT * FROM laundry_info")
    print("\nLaundry Request Data:")
    for row in cursor.fetchall():
        print(row)

# if __init__ == "__main__"
# def main():
#     # Your code here
#     print("hi")


# if __name__ "__main__":
#     main()
def main():
    while True:
        print("\nHostel Management System Menu:")
        print("1. Add Student")
        print("2. Add Complaint")
        print("3. Add Mess Feedback")
        print("4. Add Laundry Request")
        print("5. Update Laundry Status")
        print("6. Retrieve Student Name")
        print("7. show all")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            roll = int(input("Enter Roll Number: "))
            name = input("Enter Student Name: ")
            phone1 = int(input("Enter Phone 1: "))
            phone2 = int(input("Enter Phone 2: "))
            room = int(input("Enter Room Number: "))
            insert_data(roll, name, phone1, phone2, room)
            print("Student added successfully!")

        elif choice == '2':
            c_no = int(input("Enter Complaint Number: "))
            roll = int(input("Enter Roll Number: "))
            disc = input("Enter Complaint Description: ")
            c_type = input("Enter Complaint Type: ")
            add_complaint(c_no, roll, disc, c_type)
            print("Complaint added successfully!")

        elif choice == '3':
            sno = int(input("Enter Serial Number: "))
            roll = int(input("Enter Roll Number: "))
            feed = input("Enter Mess Feedback: ")
            add_mess(sno, roll, feed)
            print("Mess Feedback added successfully!")

        elif choice == '4':
            sno = int(input("Enter Serial Number: "))
            roll = int(input("Enter Roll Number: "))
            g_date = input("Enter Given Date (yyyy-mm-dd): ")
            r_date = input("Enter Received Date (yyyy-mm-dd): ")
            comp = input("Enter Completion Status (y/n): ")
            add_laundry(sno, roll, g_date, r_date, comp)
            print("Laundry Request added successfully!")

        elif choice == '5':
            sno = int(input("Enter Serial Number for Laundry Request: "))
            comp = input("Enter Updated Completion Status (y/n): ")
            update_laundry(sno, comp)
            print("Laundry Request status updated successfully!")

        elif choice == '6':
            roll = int(input("Enter Roll Number to Retrieve Student Name: "))
            student_name = retrieve(roll)
            print(f"Student Name: {student_name}")

        elif choice == '7':
            show_all_data()
        
        elif choice =='8':
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

# Close the database connection
conn.close()

# Example usage
# insert_data(102, 'ramu', 9863354, 47534724, 13)
# add_complaint(122, 102, 'good service', 'mess')
# add_mess(1, 102, 'v.v.v.good')
# update_laundry(1, 'y')
# student_name = retrieve(102)
# print(f"Student Name: {student_name}")

# # Close the database connection
# conn.close()

