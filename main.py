import psycopg2

conn = psycopg2.connect(database='psycopg', user='postgres', password='s5130462')
def create(connection):
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
                    phone_number VARCHAR(15),
                    user_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES customer(id) ON DELETE CASCADE
                );
                """)
        conn.commit()
            