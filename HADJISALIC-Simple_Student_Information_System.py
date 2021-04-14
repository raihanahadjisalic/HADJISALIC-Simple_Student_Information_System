# Simple Student Information System
# Raihana A. Hadjisalic

import csv

student_information = ['name', 'id_number', 'year level', 'gender', 'course']
student_database = 'Studentdata.csv'

def main_display():
    print("--------------------------------------")
    print(" Welcome to Student Information System")
    print("---------------------------------------")
    print("1. Display Student")
    print("2. Add New Student")
    print("3. Edit Student")
    print("4. Delete Student")
    print("5. Search Student")
    print("6. Quit")
    print()

def display_student():
    global student_information
    global student_database

    print("--- Student Information ---")

    with open(student_database, "r", encoding = "utf-8") as f:
        reader = csv.reader(f)
        for x in student_information :
            print( x, end = "\n")
        print("\n-------------------------------------------------")
        
        for row in reader:
            for item in row:
                print( item, end = "\n")
            print()        
    input("Press any key to continue")

def add_student():
    print("-------------------------")
    print("       Add Student       ")
    print("-------------------------")
    global student_information
    global student_database

    student_data = []
    for field in student_information:
        value = input("Enter " + field + ": ")
        student_data.append(value)

    with open(student_database, "a", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows([student_data])

    print("Data saved successfully")
    input("Press any key to continue")
    return

def edit_student():
    global student_information
    global student_database

    print("--- Edit Student Information ---")
    ID_number = input("Enter ID number you want to edit: ")
    index_student = None
    edited_data = []
    with open(student_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        counter = 0
        for row in reader:
            if len(row) > 0:
                if ID_number == row[1]:
                    index_student = counter
                    print("Student Found: at index ",index_student)
                    student_data = []
                    for field in student_information:
                        value = input("Enter " + field + ": ")
                        student_data.append(value)
                    edited_data.append(student_data)
                else:
                    edited_data.append(row)
                counter += 1


    # Check if the record is found or not
    if index_student is not None:
        with open(student_database, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(edited_data)
    else:
        print("ID Number not found")

    input("Press any key to continue")

def delete_student():
    global student_information
    global student_database

    print("--- Delete Student ---")
    ID_number = input("Enter ID Number to delete: ")
    student_found = False
    edited_data = []
    with open(student_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        counter = 0
        for row in reader:
            if len(row) > 0:
                if ID_number != row[1]:
                    edited_data.append(row)
                    counter += 1
                else:
                    student_found = True

    if student_found is True:
        with open(student_database, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(edited_data)
        print("ID Number ", ID_number, "deleted successfully")
    else:
        print("ID Number not found")

    input("Press any key to continue")

def search_student():
    global student_information
    global student_database

    print("--- Search Student ---")
    ID_number = input("Enter ID Number: ")
    with open(student_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 0:
                if ID_number == row[1]:
                    print("----- Student Found -----")
                    print("Name: ", row[0])
                    print("ID Nmber: ", row[1])
                    print("Year Level: ", row[2])
                    print("Gender: ", row[3])
                    print("Course: ", row[4])
                    break
        else:
            print("ID Number not found")
    input("Press any key to continue")


while True:
    main_display()

    choice = input("Enter your choice: ")
    if choice == '1':
        display_student()
    elif choice == '2':
        add_student()
    elif choice == '3':
        edit_student()
    elif choice == '4':
        delete_student()
    elif choice == '5':
        search_student()
    else:
        break

print("-------------------------------")
print(" Thank you for using our system")
print("-------------------------------")

