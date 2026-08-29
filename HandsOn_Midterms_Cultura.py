import os

FileName = "employees.txt"
Dept = ["IT Department", "Law Firm Department", "Architect Department"]

def file():
    if not os.path.exists(FileName):
        with open(FileName, 'w') as f:
            pass

def read_records():
    records = []
    if os.path.exists(FileName):
        with open(FileName, 'r') as f:
            for line in f:
                if line.strip():
                    records.append(line.strip().split('|'))
    return records

def save_all_records(records):
    with open(FileName, 'w') as f:
        for rec in records:
            f.write("|".join(rec) + "\n")

def register_employee():
    while True:
        emp_id = input("Enter Employee ID: ")
        name = input("Enter Full Name: ")

        while True:
            dept = input(f"Enter Department {Dept}: ")
            if dept in Dept:
                break
            print("Error: Invalid Department. Please try again.")

        salary = input("Enter Salary: ")

        with open(FileName, 'a') as f:
            f.write(f"{emp_id}|{name}|{dept}|{salary}\n")

        print("Record saved successfully.")
        again = input("Do you want to add another employee? (y/n): ").lower()
        if again != 'y':
            break

def view_all_employees():
    records = read_records()
    if not records:
        print("\nNo records found.")
        return

    print(f"\n{'ID':<10} | {'Name':<25} | {'Department':<25} | {'Salary':<10}")
    print("-" * 85)
    for r in records:
        print(f"{r[0]:<10} | {r[1]:<25} | {r[2]:<25} | {r[3]:<10}")

def update_employee():
    while True:
        records = read_records()
        target_id = input("Enter Employee ID to update: ")
        found = False

        for i, rec in enumerate(records):
            if rec[0] == target_id:
                found = True
                print("\nWhat do you want to edit?")
                print("1. ID\n2. Name\n3. Department\n4. Salary\n5. All")
                choice = input("Choice: ")

                if choice == '1' or choice == '5':
                    records[i][0] = input("Enter New ID: ")
                if choice == '2' or choice == '5':
                    records[i][1] = input("Enter New Name: ")
                if choice == '3' or choice == '5':
                    while True:
                        new_dept = input(f"Enter New Dept {Dept}: ")
                        if new_dept in Dept:
                            records[i][2] = new_dept
                            break
                        print("Invalid Department.")
                if choice == '4' or choice == '5':
                    records[i][3] = input("Enter New Salary: ")

                save_all_records(records)
                print("Update successful.")
                break

        if not found:
            print("Employee ID not found.")

        again = input("Update another employee? (y/n): ").lower()
        if again != 'y':
            break

def remove_employee():
    records = read_records()
    target_id = input("Enter ID to delete: ")
    for i, rec in enumerate(records):
        if rec[0] == target_id:
            print(f"Record found: {rec}")
            confirm = input("Are you sure you want to delete this record? (y/n): ").lower()
            if confirm == 'y':
                records.pop(i)
                save_all_records(records)
                print("Record deleted.")
            return
    print("Record not found.")

def main():
    file()
    while True:
        print("\n--- HR Employee Management System ---")
        print("1. Register Employee")
        print("2. View All Employees")
        print("3. Update Employee Info")
        print("4. Remove Employee")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            register_employee()
        elif choice == '2':
            view_all_employees()
        elif choice == '3':
            update_employee()
        elif choice == '4':
            remove_employee()
        elif choice == '5':
            print("Exiting system...")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()