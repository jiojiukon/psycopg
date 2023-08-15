import psycopg2

comands = """
ct - создать таблицы 
ap - добавить телефон в бд
up - обновить телефон
ac - добавить клиента в бд
uc - обновить данные клиента
s - найти клиента
"""

conn = psycopg2.connect(database='psycopg', user='postgres', password='s5130462')
    
def create_tables():
    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS customer(
                        id SERIAL PRIMARY KEY,
                        first_name VARCHAR(30) NOT NULL,
                        last_name VARCHAR(30) NOT NULL,
                        email VARCHAR(100) NOT NULL UNIQUE
                    );
                    """)
        cur.execute("""
                CREATE TABLE IF NOT EXISTS phone(
                    id SERIAL PRIMARY KEY,
                    phone_number VARCHAR(15) UNIQUE,
                    user_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES customer(id) ON DELETE CASCADE
                );
                """)
        conn.commit()

def add_phone(*phone_info):
    values = f"""{'%s,'*len(phone_info)}"""[:-1]    
    with conn.cursor() as cur:
        if len(phone_info) == 3:
            cur.execute(f"""
                        INSERT INTO phone(phone_number, user_id, id) VALUES({values});
                        """,(phone_info))        
        else:
            cur.execute(f"""
                        INSERT INTO phone(phone_number, user_id) VALUES({values});
                        """,(phone_info))        
        conn.commit()

def update_phone(new_phone, phone_id):
    with conn.cursor() as cur:
        cur.execute(f"""
                    UPDATE phone SET phone_number=%s WHERE id=%s ;
                    """, (new_phone, phone_id))
        conn.commit()
        
def add_customer(user_info, phone_number=None ):
    with conn.cursor() as cur:
        cur.execute(f"""
                    INSERT INTO customer(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id;
                    """, user_info
                    )
        userId = cur.fetchone()[0]
        add_phone(phone_number,userId)

            
        conn.commit()

def update_customer(*user_info):
    with conn.cursor() as cur:
        cur.execute(f"""
                    UPDATE customer SET first_name=%s, last_name=%s, email=%s WHERE id=%s ;
                    """, (user_info))
        conn.commit()

def del_customer(customer_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phones WHERE user_id=%s;
            """, (customer_id,))
        conn.commit()
    
def search_customer(keyword, column):
    with conn.cursor() as cur:
        if column != 'phone_number':
            cur.execute(f""" 
                    SELECT * FROM customer WHERE {column}=%s;
                    """, (keyword,))
            return print(cur.fetchone())
        else:
            cur.execute(f""" 
                    SELECT * FROM phone WHERE {column}=%s;
                    """, (keyword,))
            user_id = cur.fetchone()[-1]
            cur.execute(f""" 
                    SELECT * FROM customer WHERE id=%s;
                    """, (user_id,))
            return print(cur.fetchone())


if __name__ == "__main__":
    while True:
        with conn.cursor() as cur:
            comand = input('Введите команду: ')
            if comand == 'ct':
                create_tables()
                print('Таблицы созданы.')
            elif comand == 'ap':
                phone_info = [input('Введите номер телефона:'), input('Введите id клиента:'), input('Введите id телефона:')]
                data =  [x for x in phone_info if x!='']
                add_phone(*data)
                print('Телефон добавлен.')
            elif comand == 'ac':
                cusomer_info = [input('Введите имя клиента:'), input('Введите фамилию клиента:'), input('Введите email клиента:')]
                add_customer(cusomer_info, input('Введите телефон клиента:'))
                print('Клиент добавлен.')
            elif comand == 'uc':
                customer_info = [input('Введите имя клиента:'), input('Введите фамилию клиента:'), input('Введите email клиента:'), input('Введите id клиента:')]
                update_customer(*customer_info)
            elif comand == 's':
                keyword, column = input('Поисковой запрос:'), input('Где искать? (id - 1, имя - 2, фамилия - 3, email - 4, Номер телефона - 5)')
                c = {'1':'id', '2':'first_name', '3':'last_name', '4':'email',  '5':'phone_number'}
                search_customer(keyword, c[column])
            elif comand == 'h':
                print(comands)
            elif comand == 'q':
                break