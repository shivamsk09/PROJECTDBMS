import mysql.connector as mysql

def create_connection():
    return mysql.connect(host="localhost", user="root", passwd="MySQL Password")

def create_database(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS TODO")
    cursor.execute("USE TODO")

def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_todo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task VARCHAR(50) NOT NULL,
            status ENUM('pending', 'completed') DEFAULT 'pending'
        )
    """)

def main():
    try:
        with create_connection() as connect:
            with connect.cursor() as cursor:
                create_database(cursor)
                create_table(cursor)
                print("Table created...")

                while True:
                    print("\n1) Insert Task")
                    print("2) View Tasks")
                    print("3) Update Task")
                    print("4) Delete Task")
                    print("5) Exit")

                    choice = input("Enter your choice: ")

                    if choice == '1':
                        task = input("Enter task: ")
                        cursor.execute("INSERT INTO tb_todo (task) VALUES (%s)", (task,))
                        connect.commit()
                        print("Task added.")

                    elif choice == '2':
                        cursor.execute("SELECT * FROM tb_todo")
                        for i in cursor:
                            print(i)

                    elif choice == '3':
                        task_id = input("Enter task ID: ")
                        status = input("Enter new status (pending/completed): ")
                        if status in ['pending', 'completed']:
                            cursor.execute("UPDATE tb_todo SET status=%s WHERE id=%s", (status, task_id))
                            connect.commit()
                            print("Task updated.")
                        else:
                            print("Invalid status. Please enter 'pending' or 'completed'.")

                    elif choice == '4':
                        task_id = input("Enter task ID: ")
                        cursor.execute("DELETE FROM tb_todo WHERE id=%s", (task_id,))
                        connect.commit()
                        print("Task deleted.")

                    elif choice == '5':
                        print("Exiting...")
                        break

                    else:
                        print("Invalid choice. Try again.")
    except mysql.Error as err:
        print(f"Error: {err}")

if _name_ == "_main_":
    main()
