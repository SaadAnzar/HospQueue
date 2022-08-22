import psycopg2

con = psycopg2.connect(
    host='localhost',
    dbname='HospQueue',
    user='postgres',
    password='PostgreSQL@09',
    port=5432
)

cur = con.cursor()

print('Database is connected!')

create_script = '''CREATE TABLE IF NOT EXISTS patient(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(30) NOT NULL,
                    birthday VARCHAR(30) NOT NULL,
                    gender VARCHAR(15) NOT NULL,
                    spot INT);'''

cur.execute(create_script)

con.commit()
print("database created!")
cur.close()
con.close()