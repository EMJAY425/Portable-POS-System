class Node:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(root, value):

    if root is None:
        return Node(value)

    if value < root.value:
        root.left = insert(root.left, value)

    elif value > root.value:
        root.right = insert(root.right, value)

    # If the same value already exists, we do not add it again.
    else:
        print(f"{value} already exists in the tree.")

    # We return the root so the tree stays connected.
    return root


# This function is used to look for a value inside the tree.
def search(root, target):

    # If we reach an empty part of the tree, the value is not found.
    if root is None:
        return False

    # If the current node is the same as the target, we found it.
    if root.value == target:
        return True

    # If the target is smaller, search on the left side.
    if target < root.value:
        return search(root.left, target)

    # If the target is greater, search on the right side.
    return search(root.right, target)


# Inorder Traversal means: Left → Root → Right.
def inorder(root):

    # We only continue if the current node exists.
    if root is not None:

        # First, visit the left side.
        inorder(root.left)

        # Then, print the current node.
        print(root.value, end=" ")

        # Lastly, visit the right side.
        inorder(root.right)


# Preorder Traversal means: Root → Left → Right.
def preorder(root):

    # We only continue if the current node exists.
    if root is not None:

        # First, print the current node.
        print(root.value, end=" ")

        # Then, visit the left side.
        preorder(root.left)

        # Lastly, visit the right side.
        preorder(root.right)


# Postorder Traversal means: Left → Right → Root.
def postorder(root):

    # We only continue if the current node exists.
    if root is not None:

        # First, visit the left side.
        postorder(root.left)

        # Then, visit the right side.
        postorder(root.right)

        # Lastly, print the current node.
        print(root.value, end=" ")


# Level-order Traversal means printing from top to bottom, left to right.
def level_order(root):

    # If the tree is empty, there is nothing to display.
    if root is None:
        print("The tree is empty.")
        return

    # We use a list as a queue.
    queue = []

    # We start with the root node.
    queue.append(root)

    # This loop runs while there are still nodes waiting in the queue.
    while queue:

        # We remove the first node from the queue.
        current = queue.pop(0)

        # We print the current node.
        print(current.value, end=" ")

        # If there is a left child, add it to the queue.
        if current.left is not None:
            queue.append(current.left)

        # If there is a right child, add it to the queue.
        if current.right is not None:
            queue.append(current.right)


# This function finds the smallest value in a subtree.
def find_min(root):

    # In a BST, the smallest value is found by moving left.
    while root.left is not None:
        root = root.left

    # This returns the smallest node.
    return root


# This function removes a value from the Binary Search Tree.
def delete(root, value):

    # If the tree is empty, there is nothing to delete.
    if root is None:
        return root

    # If the value is smaller, search on the left side.
    if value < root.value:
        root.left = delete(root.left, value)

    # If the value is greater, search on the right side.
    elif value > root.value:
        root.right = delete(root.right, value)

    # If the value matches the current node, this is the node to delete.
    else:

        # If the node has no left child, replace it with the right child.
        if root.left is None:
            return root.right

        # If the node has no right child, replace it with the left child.
        elif root.right is None:
            return root.left

        # If the node has two children, find the smallest value
        # from the right subtree.
        temp = find_min(root.right)

        # Copy that smallest value into the current node.
        root.value = temp.value

        # Delete the duplicate value from the right subtree.
        root.right = delete(root.right, temp.value)

    # Return the updated tree.
    return root


# This function counts how many nodes are inside the tree.
def tree_size(root):

    # If the current node is empty, it counts as 0.
    if root is None:
        return 0

    # Count the current node, plus the left side, plus the right side.
    return 1 + tree_size(root.left) + tree_size(root.right)


# This function gets the height of the tree.
def tree_height(root):

    # If the tree is empty, height is -1.
    if root is None:
        return -1

    # Get the height of the left side.
    left_height = tree_height(root.left)

    # Get the height of the right side.
    right_height = tree_height(root.right)

    # The height is the taller side plus 1.
    return 1 + max(left_height, right_height)


# This function helps us prepare the tree design before printing it.
def build_tree_lines(root):

    # If the current node is empty, return empty values.
    if root is None:
        return [], 0, 0, 0

    # Convert the current node value into string so we can print it.
    node_value = str(root.value)

    # Get the length of the current node value.
    node_width = len(node_value)

    # If the node has no left child and no right child,
    # it means this node is a leaf node.
    if root.left is None and root.right is None:
        return [node_value], node_width, 1, node_width // 2

    # If the node only has a left child.
    if root.right is None:

        # Build the lines for the left subtree.
        left_lines, left_width, left_height, left_middle = build_tree_lines(root.left)

        # Create the first line showing the current node.
        first_line = " " * (left_middle + 1) + "_" * (left_width - left_middle - 1) + node_value

        # Create the second line showing the branch going to the left.
        second_line = " " * left_middle + "/" + " " * (left_width - left_middle - 1 + node_width)

        # Add spaces to the left subtree lines so they align properly.
        shifted_lines = [line + " " * node_width for line in left_lines]

        # Return the complete printed structure.
        return [first_line, second_line] + shifted_lines, left_width + node_width, left_height + 2, left_width + node_width // 2

    # If the node only has a right child.
    if root.left is None:

        # Build the lines for the right subtree.
        right_lines, right_width, right_height, right_middle = build_tree_lines(root.right)

        # Create the first line showing the current node.
        first_line = node_value + "_" * right_middle + " " * (right_width - right_middle)

        # Create the second line showing the branch going to the right.
        second_line = " " * node_width + " " * right_middle + "\\" + " " * (right_width - right_middle - 1)

        # Add spaces before the right subtree lines so they align properly.
        shifted_lines = [" " * node_width + line for line in right_lines]

        # Return the complete printed structure.
        return [first_line, second_line] + shifted_lines, right_width + node_width, right_height + 2, node_width // 2

    # If the node has both left and right children.
    left_lines, left_width, left_height, left_middle = build_tree_lines(root.left)
    right_lines, right_width, right_height, right_middle = build_tree_lines(root.right)

    # Create the first line with the current node in the middle.
    first_line = (
        " " * (left_middle + 1)
        + "_" * (left_width - left_middle - 1)
        + node_value
        + "_" * right_middle
        + " " * (right_width - right_middle)
    )

    # Create the second line with the left and right branches.
    second_line = (
        " " * left_middle
        + "/"
        + " " * (left_width - left_middle - 1 + node_width + right_middle)
        + "\\"
        + " " * (right_width - right_middle - 1)
    )

    # If left and right subtrees have different heights,
    # add blank lines to make them the same height.
    if left_height < right_height:
        left_lines += [" " * left_width] * (right_height - left_height)
    elif right_height < left_height:
        right_lines += [" " * right_width] * (left_height - right_height)

    # Combine the left and right subtree lines.
    combined_lines = [
        left_line + " " * node_width + right_line
        for left_line, right_line in zip(left_lines, right_lines)
    ]

    # Return the complete printed structure.
    return [first_line, second_line] + combined_lines, left_width + right_width + node_width, max(left_height, right_height) + 2, left_width + node_width // 2


# This function displays the tree in normal top-to-bottom structure.
def display_tree(root):

    # If the tree is empty, print a message.
    if root is None:
        print("The tree is empty.")
        return

    # Build the tree lines first.
    lines, width, height, middle = build_tree_lines(root)

    # Print each line of the tree.
    for line in lines:
        print(line)


# This function changes the user's input depending on the chosen data type.
def convert_value(user_input, data_type):

    # If the user chose numbers, convert the input into an integer.
    if data_type == "number":
        return int(user_input)

    # If the user chose strings, keep the input as text.
    return user_input


# This function prints the menu options.
def show_menu():

    print("\n========== BINARY SEARCH TREE MENU ==========")
    print("1. Add / Insert Node")
    print("2. Search Node")
    print("3. Display Inorder Traversal")
    print("4. Display Preorder Traversal")
    print("5. Display Postorder Traversal")
    print("6. Display Level-order Traversal")
    print("7. Delete Node")
    print("8. Show Tree Size")
    print("9. Show Tree Height")
    print("10. Display Tree Structure")
    print("11. Exit")
    print("=============================================")


# This is the main function where our program starts.
def main():

    # At first, our tree is empty.
    root = None

    # Ask the user what type of data they want to use.
    print("Choose the type of values for your BST:")
    print("1. Numbers")
    print("2. Strings / Words")

    # Get the user's choice.
    type_choice = input("Enter your choice: ")

    # If the user chooses 1, the program will use numbers.
    if type_choice == "1":
        data_type = "number"
        starting_values = []

        # Add the starting values automatically.
        for value in starting_values:
            root = insert(root, value)

        print("\nStarting values added to the BST:")
        print(starting_values)

    # If the user chooses 2, the program will use strings.
    elif type_choice == "2":
        data_type = "string"
        starting_values = []

        # Add the starting words automatically.
        for value in starting_values:
            root = insert(root, value)

        print("\nStarting words added to the BST:")
        print(starting_values)

    # If the input is invalid, use numbers as the default.
    else:
        data_type = "number"
        starting_values = []

        for value in starting_values:
            root = insert(root, value)

        print("\nInvalid choice. Default type is Numbers.")
        print("Starting values added to the BST:")
        print(starting_values)

    # This loop keeps the program running until the user chooses Exit.
    while True:

        # Show the menu.
        show_menu()

        # Ask the user what they want to do.
        choice = input("Enter your choice: ")

        # Option 1 allows the user to insert one or more nodes.
        if choice == "1":

            # Ask the user for multiple values separated by spaces.
            print("\nYou can enter one or more values separated by spaces.")

            # If the selected type is number, show a number example.
            if data_type == "number":
                print("Example: 22 12 14 88 44 66")

            # If the selected type is string, show a string example.
            else:
                print("Example: Mango Apple Orange Banana")

            # Get the full line of input from the user.
            values_input = input("Enter value/s to insert: ")

            # Split the input by spaces.
            # Example: "22 12 14" becomes ["22", "12", "14"].
            values_list = values_input.split()

            # If the user pressed Enter without typing anything,
            # we do not insert anything.
            if len(values_list) == 0:
                print("No value entered.")

            else:
                try:
                    # Go through each value typed by the user.
                    for item in values_list:

                        # Convert each item depending on the selected data type.
                        value = convert_value(item, data_type)

                        # Insert each value into the BST.
                        root = insert(root, value)

                    # Tell the user that the values were inserted.
                    print("Node/s inserted successfully.")

                except ValueError:
                    # This happens when the user selected numbers but typed words.
                    print("Invalid input. Please enter numbers separated by spaces.")

        # Option 2 allows the user to search for a node.
        elif choice == "2":

            # Ask the user what value they want to search.
            value_input = input("Enter value to search: ")

            try:
                # Convert the input based on the selected type.
                value = convert_value(value_input, data_type)

                # Search the value in the BST.
                found = search(root, value)

                # Print the search result.
                if found:
                    print("Value found in the tree.")
                else:
                    print("Value not found in the tree.")

            except ValueError:
                print("Invalid input. Please enter a number.")

        # Option 3 displays Inorder Traversal.
        elif choice == "3":

            print("Inorder Traversal:")
            inorder(root)
            print()

        # Option 4 displays Preorder Traversal.
        elif choice == "4":

            print("Preorder Traversal:")
            preorder(root)
            print()

        # Option 5 displays Postorder Traversal.
        elif choice == "5":

            print("Postorder Traversal:")
            postorder(root)
            print()

        # Option 6 displays Level-order Traversal.
        elif choice == "6":

            print("Level-order Traversal:")
            level_order(root)
            print()

        # Option 7 deletes a node.
        elif choice == "7":

            # Ask the user what value they want to delete.
            value_input = input("Enter value to delete: ")

            try:
                # Convert the input based on the selected type.
                value = convert_value(value_input, data_type)

                # Check first if the value exists.
                if search(root, value):

                    # Delete the value.
                    root = delete(root, value)

                    print("Node deleted successfully.")

                else:
                    print("Value not found. Cannot delete.")

            except ValueError:
                print("Invalid input. Please enter a number.")

        # Option 8 displays the number of nodes.
        elif choice == "8":

            print("Tree size:", tree_size(root))

        # Option 9 displays the height of the tree.
        elif choice == "9":

            print("Tree height:", tree_height(root))

        # Option 10 displays the tree structure.
        elif choice == "10":

            print("Tree Structure:")
            display_tree(root)

        # Option 11 exits the program.
        elif choice == "11":

            print("Thank you for using the BST program.")
            break

        # This runs if the user enters an invalid menu choice.
        else:
            print("Invalid choice. Please try again.")


# This line starts the whole program.
main()