reservations = []
next_id = 1

def add_reservation():
    global next_id
    name = input("Enter name: ")
    if name.isdigit():
        print("Invalid name.\n")
        return
    date = input("Enter date (YYYY-MM-DD): ")
    if date.isalpha():
        print("Invalid date.\n")
        return
    time = input("Enter time (HH:MM): ")
    if time.isalpha():
        print("Invalid time.\n")
        return

    reservation = {
        "id": next_id,
        "name": name,
        "date": date,
        "time": time
    }

    reservations.append(reservation)
    print("Reservation added successfully!\n")
    next_id += 1

def view_reservations():
    if not reservations:
        print("No reservations found.\n")
        return

    for r in reservations:
        print(f"ID: {r['id']} | Name: {r['name']} | Date: {r['date']} | Time: {r['time']}")
    print()

def linear_search(res_id):
    for r in reservations:
        if r["id"] == res_id:
            return r
    return None

def binary_search(res_id):
    low = 0
    high = len(reservations) - 1

    while low <= high:
        mid = (low + high) // 2
        if reservations[mid]["id"] == res_id:
            return reservations[mid]
        elif reservations[mid]['id'] < res_id:
            low = mid + 1
        else:
            high = mid - 1

    return None

def search_reservation():
    try:
        res_id = int(input("Enter reservation ID to search: "))
    except ValueError:
        print("Invalid input.\n")
        return

    print("1. Linear Search")
    print("2. Binary Search (list must be sorted)")

    choice = input("Choose search method: ")

    if choice == "1":
        result = linear_search(res_id)
    elif choice == "2":
        # Sort first for binary search
        reservations.sort(key=lambda x: x["id"])
        result = binary_search(res_id)
    else:
        print("Invalid choice.\n")
        return

    if result:
        print("Reservation Found:")
        print(result, "\n")
    else:
        print("Reservation not found.\n")

def update_reservation():
    try:
        res_id = int(input("Enter reservation ID to update: "))
    except ValueError:
        print("Invalid input.\n")
        return

    reservation = linear_search(res_id)

    if reservation:
        reservation["name"] = input("Enter new name: ")
        reservation["date"] = input("Enter new date: ")
        reservation["time"] = input("Enter new time: ")
        print("Reservation updated!\n")
    else:
        print("Reservation not found.\n")

def delete_reservation():
    try:
        res_id = int(input("Enter reservation ID to delete: "))
    except ValueError:
        print("Invalid input.\n")
        return

    for i in range(len(reservations)):
        if reservations[i]["id"] == res_id:
            reservations.pop(i)
            print("Reservation deleted.\n")
            return

    print("Reservation not found.\n")

def main():
    while True:
        print("===== RESERVATION SYSTEM =====")
        print("1. Add Reservation")
        print("2. View Reservations")
        print("3. Search Reservation")
        print("4. Update Reservation")
        print("5. Delete Reservation")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_reservation()
        elif choice == "2":
            view_reservations()
        elif choice == "3":
            search_reservation()
        elif choice == "4":
            update_reservation()
        elif choice == "5":
            delete_reservation()
        elif choice == "6":
            print("Exiting program...")
            break
        else:
            print("Invalid choice.\n")

main()