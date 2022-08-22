import psycopg2
import json

# Opening json file in read mode
with open('auth.json') as r:
    config = json.load(r)

create_script = '''CREATE TABLE IF NOT EXISTS patient(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(30) NOT NULL,
                    birthday VARCHAR(30) NOT NULL,
                    gender VARCHAR(15) NOT NULL,
                    spot INT);'''
# Class including all the actions' functionality
class Actions:
    def __init__(self, config):
        # From json File
        self.host = config['HOST']
        self.dbname = config['DB']
        self.user = config['USER']
        self.password = config['PASS']
        self.port = 5432
        self.conn = None

    # To connect the database
    def connect(self):
        if self.conn is None:
            self.conn = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port
            )
            print('Database connected successfully!')

    # Inserting a new user in the queue
    def new_entry(self, name, birthday, gender, spot):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("INSERT INTO patient(name,birthday,gender,spot)"
                    f"VALUES ('{name}', '{birthday}', '{gender}', {spot});")
        self.conn.commit()
        cur.close()

        print("Patient joined the queue")

    # Assigning a spot to the user
    def new_spot(self):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT MAX(spot)"
                    f"FROM patient")
        maximum = cur.fetchone()
        if maximum[0] is None:
            maximum = 1
        else:
            maximum = maximum[0] + 1
        cur.close()
        print("New patient joined the queue", maximum)
        return maximum

    # Fetch the spot of the user
    def get_spot(self, name):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT spot FROM patient "
                    f"WHERE name = '{name}';")
        spot = cur.fetchone()
        cur.close()
        return spot

    # Calculates the total people ahead
    def total_infront(self, name):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT spot FROM patient "
                    f" WHERE name = '{name}';")
        current_spot = cur.fetchone()
        if current_spot is not None:
            cur.execute("SELECT * FROM patient "
                        f"WHERE spot < {current_spot[0]};")
            total_list = list(cur.fetchall())
            total = len(total_list)
            cur.close()
            print(total, "total")
            return total
        return 0

    # Removing a person from the queue
    def leave(self, name, spot):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("DELETE FROM patient "
                    f"WHERE name='{name}';")
        self.conn.commit()
        cur.close()
        print(name, "left")
