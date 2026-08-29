import csv
import os

FILENAME = "characters.csv"


def initialize_file():
    if not os.path.exists(FILENAME) or os.path.getsize(FILENAME) == 0:
        with open(FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Role", "Trait"])


def add_character():
    print("\n--- Add Character ---")
    char_id = input("Enter Character ID: ")
    name = input("Enter Name: ")
    role = input("Enter Role (Protagonist, Antagonist, Supporting): ")
    trait = input("Enter Special Trait: ")

    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([char_id, name, role, trait])
    print("Character added successfully!")


def view_all_characters():
    print("\n--- View All Characters ---")
    if not os.path.exists(FILENAME) or os.path.getsize(FILENAME) == 0:
        print("System Message: Character file is missing or empty.")
        return

    with open(FILENAME, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        print(f"{header[0]:<10} {header[1]:<25} {header[2]:<15} {header[3]:<20}")
        print("-" * 70)
        for row in reader:
            print(f"{row[0]:<10} {row[1]:<25} {row[2]:<15} {row[3]:<20}")


def search_character():
    print("\n--- Search Character ---")
    search_id = input("Enter Character ID to search: ")
    found = False

    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[0] == search_id:
                    print(f"\nID: {row[0]}\nName: {row[1]}\nRole: {row[2]}\nTrait: {row[3]}")
                    found = True
                    break

    if not found:
        print("Character not found.")


def update_character():
    print("\n--- Update Character ---")
    search_id = input("Enter Character ID to update: ")
    updated_rows = []
    found = False

    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r', newline='') as file:
            reader = list(csv.reader(file))
            if len(reader) > 0:
                updated_rows.append(reader[0])  # Keep header
                for row in reader[1:]:
                    if row[0] == search_id:
                        print(f"Current Info: {row}")
                        row[1] = input("Enter New Name: ")
                        row[2] = input("Enter New Role: ")
                        row[3] = input("Enter New Trait: ")
                        found = True
                    updated_rows.append(row)

        if found:
            with open(FILENAME, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)
            print("Character updated successfully!")
        else:
            print("Character not found.")
    else:
        print("File not found.")


def delete_character():
    print("\n--- Delete Character ---")
    search_id = input("Enter Character ID to delete: ")
    updated_rows = []
    found = False

    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r', newline='') as file:
            reader = list(csv.reader(file))
            if len(reader) > 0:
                updated_rows.append(reader[0])  # Keep header
                for row in reader[1:]:
                    if row[0] == search_id:
                        found = True
                        continue  # Skip the row to "delete" it
                    updated_rows.append(row)

        if found:
            with open(FILENAME, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)
            print("Character deleted successfully!")
        else:
            print("Character not found.")
    else:
        print("File not found.")


def main():
    initialize_file()
    while True:
        print("\n===== RAIN IN ESPAÑA CHARACTER SYSTEM =====")
        print("1. Add Character")
        print("2. View All Characters")
        print("3. Search Character")
        print("4. Update Character")
        print("5. Delete Character")
        print("6. Exit")
        print("============================================")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_character()
        elif choice == '2':
            view_all_characters()
        elif choice == '3':
            search_character()
        elif choice == '4':
            update_character()
        elif choice == '5':
            delete_character()
        elif choice == '6':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()