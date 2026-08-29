reservations = []
next_id = 1


def insertion_sort(field="id", ascending=True):

    for i in range(1, len(reservations)):
        key_item = reservations[i]
        j = i - 1
        val_i = key_item[field].lower() if isinstance(key_item[field], str) else key_item[field]

        while j >= 0:
            val_j = reservations[j][field].lower() if isinstance(reservations[j][field], str) else reservations[j][
                field]

            if ascending:
                if val_j > val_i:
                    reservations[j + 1] = reservations[j]
                    j -= 1
                else:
                    break
            else:
                if val_j < val_i:
                    reservations[j + 1] = reservations[j]
                    j -= 1
                else:
                    break

        reservations[j + 1] = key_item

    direction = "Ascending" if ascending else "Descending"
    print(f"List sorted by {field.upper()} in {direction} order.\n")

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

    reservation = {"id": next_id, "name": name, "date": date, "time": time}
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
    print("2. Binary Search (Requires Ascending ID Sort)")
    choice = input("Choose: ")
    if choice == "1":
        result = linear_search(res_id)
    elif choice == "2":
        insertion_sort(field="id", ascending=True)
        result = binary_search(res_id)
    else:
        return
    if result:
        print("Found:", result, "\n")
    else:
        print("Not found.\n")


def update_reservation():
    try:
        res_id = int(input("Enter ID to update: "))
    except:
        return
    res = linear_search(res_id)
    if res:
        res["name"] = input("New name: ")
        res["date"] = input("New date: ")
        res["time"] = input("New time: ")
        print("Updated!\n")


def delete_reservation():
    try:
        res_id = int(input("Enter ID to delete: "))
    except:
        return
    for i in range(len(reservations)):
        if reservations[i]["id"] == res_id:
            reservations.pop(i)
            print("Deleted.\n")
            return


def main():
    while True:
        print("===== RESERVATION SYSTEM =====")
        print("1. Add Reservation")
        print("2. View Reservations")
        print("3. Search Reservation")
        print("4. Update Reservation")
        print("5. Delete Reservation")
        print("6. Sort Reservations")
        print("7. Exit")

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
            print("Sort by: 1. ID | 2. Name")
            f_choice = input("Choice: ")
            field = "id" if f_choice == "1" else "name"

            print("Order: 1. Ascending | 2. Descending")
            o_choice = input("Choice: ")
            asc = True if o_choice == "1" else False

            insertion_sort(field=field, ascending=asc)
        elif choice == "7":
            break


main()