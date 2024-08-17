import os
import platform
import mysql.connector
from mysql.connector import Error

try:
    db = mysql.connector.connect(
        host="localhost",
        user=input("\t\t Enter the username of MYSQL user: "),
        password=input("\t\t Enter the password: "),
    )
    print("\t\t\t Connection successfully created")
    cursor = db.cursor()
    
    # Create the library database and tables if they don't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS COURSE")
    cursor.execute("USE COURSE;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS course_details (
            c_id INT PRIMARY KEY,
            stream VARCHAR(255),
            c_name VARCHAR(255)
        )
    """)
except Error as e:
    print(f"There was an error connecting to the database: {e}")
    db = None

def course_insert():
    try:
        c_id = int(input("Enter the course ID: "))
        stream = input("Enter the Stream Name: ")
        c_name = input("Enter available opportunities or courses in this stream: ")
        course = (c_id, stream, c_name)
        sql = "INSERT INTO course_details (c_id, stream, c_name) VALUES (%s, %s, %s)"
        cursor.execute(sql, course)
        db.commit()
        print("Course inserted successfully.")
    except Error as e:
        print(f"Error: {e}")
    except ValueError:
        print("Invalid input. Please enter the correct data types.")

def c_view():
    try:
        print("Select the search criteria:")
        print("1. c_id")
        print("2. Stream")
        print("3. All")
        ch = int(input("Enter the choice: "))
        if ch == 1:
            s = int(input("c_id: "))
            sql = "SELECT * FROM course_details WHERE c_id=%s"
            cursor.execute(sql, (s,))
        elif ch == 2:
            s = input("Enter Stream Name: ")
            sql = "SELECT * FROM course_details WHERE stream=%s"
            cursor.execute(sql, (s,))
        elif ch == 3:
            sql = "SELECT * FROM course_details"
            cursor.execute(sql)
        else:
            print("Invalid choice.")
            return
        res = cursor.fetchall()
        if res:
            print("The course details are as follows:")
            print("(course_id, Stream_Name, Course_opportunities)")
            for x in res:
                print(x)
        else:
            print("No results found.")
    except Error as e:
        print(f"Error: {e}")
    except ValueError:
        print("Invalid input. Please enter the correct data types.")

def remove_course():
    try:
        cid = int(input("Enter the course ID of the course to be deleted: "))
        sql = "DELETE FROM course_details WHERE c_id=%s"
        cursor.execute(sql, (cid,))
        db.commit()
        print("Course removed successfully.")
    except Error as e:
        print(f"Error: {e}")
    except ValueError:
        print("Invalid input. Please enter the correct data types.")

def menu_set():
    print("Enter 1: To Add course")
    print("Enter 2: To View course")
    print("Enter 3: To Remove course")
    try:
        user_input = int(input("Please select an above option: "))  # Take input from user
        print("\n")  # Print new line
        if user_input == 1:
            course_insert()
        elif user_input == 2:
            c_view()
        elif user_input == 3:
            remove_course()
        else:
            print("Enter correct choice...")
    except ValueError:
        print("Invalid input. Please enter a number.")

def run_again():
    while True:
        menu_set()
        run_again = input("Want to run again? (Y/n): ").lower()
        if run_again != "y":
            break
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

if db:
    try:
        run_again()
    finally:
        cursor.close()
        db.close()
else:
    print("Failed to connect to the database.")
