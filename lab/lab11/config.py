from configparser import ConfigParser
import psycopg2
def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

def create_table():
    """ Create PhoneBook table in PostgreSQL """
    conn = None

    try:
        config = load_config() 
        conn = psycopg2.connect(**config)  
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PhoneBook (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                phone_number TEXT NOT NULL
            )
            """)
        conn.commit()
        print("Table 'PhoneBook' created successfully.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

def insert_from_console():
    conn = None

    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        username = input("Enter username: ")
        phone_number = input("Enter phone number: \n")

        cursor.execute("INSERT INTO PhoneBook (username, phone_number) VALUES (%s, %s)", (username, phone_number))
        conn.commit()
        print("Data inserted from console successfully.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

def update_data():
    conn = None

    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        
        username = input("Enter username to update: ")
        new_phone_number = input("Enter new phone number: ")

        cursor.execute("UPDATE PhoneBook SET phone_number = %s WHERE username = %s", (new_phone_number, username))
        conn.commit()
        print("Data updated successfully.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

def query_data():
    conn = None

    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

       
        username_filter = input("Enter username to filter: ")
        cursor.execute("SELECT * FROM PhoneBook WHERE username = %s", (username_filter,))
        rows = cursor.fetchall()

     
        if rows:
            print("Results:")
            for row in rows:
                print("ID:", row[0])
                print("Username:", row[1])
                print("Phone Number:", row[2])
        else:
            print("No results found for the given username.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")
        
def delete_data():
    conn = None

    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

       
        username_to_delete = input("Enter username to delete: ")
        cursor.execute("DELETE FROM PhoneBook WHERE username = %s", (username_to_delete,))
        conn.commit()
        print("Data deleted successfully.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

def query_data_with_pattern(pattern):
    conn = None

    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        
        cursor.execute("SELECT * FROM PhoneBook WHERE username LIKE %s OR phone_number LIKE %s", (f"%{pattern}%", f"%{pattern}%"))
        rows = cursor.fetchall()

        if rows:
            print("Результаты:")
            for row in rows:
                print("ID:", row[0])
                print("Имя пользователя:", row[1])
                print("Номер телефона:", row[2])
        else:
            print("Нет результатов для указанного шаблона.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с базой данных закрыто.")

def insert_many_users(user_data):
    conn = None
    invalid_data = []

    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        for username, phone_number in user_data:
           
            if len(phone_number) != 10 or not phone_number.isdigit():
                invalid_data.append((username, phone_number))
                continue

           
            cursor.execute("INSERT INTO PhoneBook (username, phone_number) VALUES (%s, %s)", (username, phone_number))

        conn.commit()

        if invalid_data:
            print("The following data is invalid and was not inserted:")
            for username, phone_number in invalid_data:
                print("Username:", username, "Phone Number:", phone_number)
        else:
            print("All data inserted successfully.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

def drop_table():
    conn = None

    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        
        cursor.execute("DROP TABLE IF EXISTS PhoneBook")
        conn.commit()
        print("Table 'PhoneBook' dropped successfully.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

def insert_or_update_user_from_console():
    conn = None

    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        username = input("Enter username: ")
        phone_number = input("Enter phone number: ")

       
        cursor.execute("SELECT * FROM PhoneBook WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            
            cursor.execute("UPDATE PhoneBook SET phone_number = %s WHERE username = %s", (phone_number, username))
            print("User", username, "updated successfully.")
        else:
            
            cursor.execute("INSERT INTO PhoneBook (username, phone_number) VALUES (%s, %s)", (username, phone_number))
            print("User", username, "added successfully.")

        conn.commit()

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")


if __name__ == '__main__':

    config = load_config()
    insert_or_update_user_from_console()