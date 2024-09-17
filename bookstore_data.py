# Database capstone project
# Imports
import sqlite3

# Creates the database/Checks if its there
db = sqlite3.connect('ebookstore.db')
cursor = db.cursor()  # Get a cursur object

# Drops the table if it already exist
cursor.execute('DROP TABLE IF EXISTS book')
cursor.execute('''
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)
''')
db.commit()

# Inserting Values into database default
books = [
    (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
    (3002, 'Harry Potter and the Philosophers Stone', 'J.K. Rowling', 40),
    (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis ', 25),
    (3004, 'The Lord of the Rings', 'J.R.R Tolkien ', 37),
    (3005, 'Alice in Wonderland', 'Lewis Carroll ', 12)
]

cursor.executemany(
    '''INSERT INTO book(id, title, author, qty) VALUES(?, ?, ?, ?)''', books
    )
db.commit()


# Just simple line maker for astetics will always be same length
def line(symbol):
    print(symbol*20)


def enter_books():
    '''
    Able to add more books into the database
    '''
    line('*')
    print("Enter books")
    line('-')
    new_books = [
        (
            int(input("Enter the ID: ")),  # Prompt user for book ID
            input("Enter the Title: "),  # Prompt user for book title
            input("Enter the Author: "),  # Prompt user for book author
            int(input("Enter the quantity: "))  # Prompt user for book quantity
        )
    ]
    cursor.executemany(
        '''INSERT INTO book(id, title, author, qty) VALUES(?, ?, ?, ?)''',
        new_books
        )
    db.commit()
    print('New book added successfully')


def update_books():
    '''
    Able to update a book based on a given id
    '''
    line('*')
    print("Update books")
    line('-')
    book_id = input("Enter the ID of the book you want to update:  ")
    update_choice = input("What would you like to update(title,author,qty): ")
    # Checks what they want to change
    if update_choice == 'title':
        new_title = input("Please enter the new titile: ")
        db.execute(
            '''UPDATE book SET title = ? WHERE id = ?''', (new_title, book_id)
            )
        db.commit()
    elif update_choice == 'author':
        new_author = input("Please enter the new author: ")
        db.execute(
            '''UPDATE book SET author = ? WHERE id = ?''',
            (new_author, book_id)
            )
        db.commit()
    elif update_choice == 'qty':
        new_qty = input("Please enter the new qty: ")
        db.execute(
            '''UPDATE book SET qty = ? WHERE id = ?''', (new_qty, book_id)
            )
        db.commit()
    else:
        print("ERROR! Please enter a coloum choice")


def delete_books():
    '''
    Locates a specified book based on the id and deletes it
    '''
    line('*')
    print("Delete books")
    line('-')
    book_id = input("Enter the ID of the book you want to delete:  ")
    # Level of error checking in the code
    verification = input("Are you sure? Please enter(y/n): ")
    if verification == 'y':
        db.execute('''DELETE FROM book WHERE id = ?''', (book_id,))
        db.commit()
        if cursor.rowcount > 0:
            print("Book deleted successfully.")
        else:
            print("Book not found.")
    elif verification == 'n':
        print("Rewrite!")
    else:
        print("ERROR! Please enter only (y) or (n)")


def search_books():
    '''
    Searches through the books in the database
    based on different parameters
    '''
    line('*')
    print("Searching books")
    line('-')
    search_choice = input(
        "What would you like to search for(title,author,qty): "
        )
    # Checks what they want to change
    if search_choice == 'title':
        search_title = input("Please enter the title: ").strip()
        cursor.execute(
            '''SELECT * FROM book WHERE title = ?''', (search_title,)
            )
    elif search_choice == 'author':
        search_author = input("Please enter the author: ").strip()
        cursor.execute(
            '''SELECT * FROM book WHERE author = ?''', (search_author,)
            )
    elif search_choice == 'qty':
        try:
            search_qty = int(input("Please enter the quantity: ").strip())
            cursor.execute(
                '''SELECT * FROM book WHERE qty = ?''', (search_qty,)
                )
        except ValueError:
            print("ERROR! Please enter a valid number for quantity.")
            return
    else:
        print("ERROR! Please enter a valid column choice.")
        return

    # Fetch and display the results
    results = cursor.fetchall()
    if results:
        print("Search results:")
        for row in results:
            print(
                f"ID: {row[0]}, Title: {row[1]}, "
                f"Author: {row[2]}, Quantity: {row[3]}"
                )
    else:
        print("No matching records found.")

    line('*')


def menu():
    '''
    Main Menu function allows access to all features
    '''
    # Menu will keep appearing after method is run
    while True:
        line('*')
        print("Book store DataBase:")
        line('-')
        print('''1. Enter book
    2. Update book
    3. Delete book
    4. Search books
    0. Exit''')
        menu_option = input(
            "\nWelcome please select a menu option(1,2,3,4,0): "
            )
        # Each menu option
        if menu_option == "1":
            enter_books()
        elif menu_option == "2":
            update_books()
        elif menu_option == "3":
            delete_books()
        elif menu_option == "4":
            search_books()
        elif menu_option == "0":
            print("Exiting! Enjoy your day")
            db.close()
            exit()
        else:
            print("Please choose one of the options!")


menu()  # Runs the main menu method
