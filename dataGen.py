import sqlite3
import random
from faker import Faker
from datetime import datetime

# Initialize Faker
fake = Faker()

# Create or connect to the SQLite3 database
conn = sqlite3.connect('dbTest.sqlite3')
cursor = conn.cursor()

# Create the "auth_user" table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS "auth_user" (
        "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "password" VARCHAR(128) NOT NULL,
        "last_login" DATETIME NULL,
        "is_superuser" BOOLEAN NOT NULL,
        "username" VARCHAR(150) NOT NULL UNIQUE,
        "last_name" VARCHAR(150) NOT NULL,
        "email" VARCHAR(254) NOT NULL,
        "is_staff" BOOLEAN NOT NULL,
        "is_active" BOOLEAN NOT NULL,
        "date_joined" DATETIME NOT NULL,
        "first_name" VARCHAR(150) NOT NULL
    )
''')

# Create the "account_billingaddress" table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS "account_billingaddress" (
        "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "name" VARCHAR(200) NOT NULL,
        "phone_number" VARCHAR(10) NOT NULL,
        "house_no" VARCHAR(300) NOT NULL,
        "landmark" VARCHAR(120) NOT NULL,
        "city" VARCHAR(120) NOT NULL,
        "state" VARCHAR(120) NOT NULL,
        "user_id" INTEGER NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
        "pin_code" VARCHAR(6) NOT NULL
    )
''')

# Create the "account_stripemodel" table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS "account_stripemodel" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "card_id" text NULL,
        "user_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
        "card_number" varchar(16) NULL UNIQUE,
        "exp_month" varchar(2) NULL,
        "exp_year" varchar(4) NULL,
        "customer_id" varchar(200) NULL,
        "email" varchar(254) NULL,
        "address_city" varchar(120) NULL,
        "address_country" varchar(120) NULL,
        "address_state" varchar(120) NULL,
        "address_zip" varchar(6) NULL,
        "name_on_card" varchar(200) NULL
    )
''')

# Create the "account_ordermodel" table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS "account_stripemodel" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "name" varchar(120) NOT NULL,
        "card_number" varchar(16) NULL,
        "address" varchar(300) NULL,
        "paid_status" bool NOT NULL,
        "total_price" decimal NULL,
        "is_delivered" bool NOT NULL,
        "delivered_at" varchar(200) NULL,
        "user_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
        "ordered_item" varchar(200) NULL,
        "paid_at" datetime NULL
    )
''')


# Generate and insert 50 rows of fake data with modified username and email
for _ in range(50):
    id = _
    password = fake.password()
    last_login = fake.date_time_this_decade()
    is_superuser = random.choice([True, False])
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = first_name[0] + last_name
    email = username.lower() + '@example.com'  # Email starts with the username
    is_staff = random.choice([True, False])
    is_active = random.choice([True, False])
    date_joined = fake.date_time_this_decade()
    
    cursor.execute('''
        INSERT INTO "auth_user" (
            "id", "password", "last_login", "is_superuser", "username", "last_name",
            "email", "is_staff", "is_active", "date_joined", "first_name"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (id, password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name))

#data for account_billingaddress table
    
    name = first_name + ' ' + last_name
    phone_number = fake.numerify(text='##########')
    house_no = fake.building_number()
    landmark = fake.street_name()
    city = fake.city()
    state = fake.state()
    user_id = id
    pin_code = fake.numerify(text='######')
    
    cursor.execute('''
        INSERT INTO "account_billingaddress" (
            "name", "phone_number", "house_no", "landmark", "city", "state", "user_id", "pin_code"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, phone_number, house_no, landmark, city, state, user_id, pin_code))

# Generate and insert 50 rows of fake data into the "account_stripemodel" table
    
    card_id = fake.uuid4()
    card_number = fake.credit_card_number(card_type=None)
    exp_month = fake.credit_card_expire(start='now', end='+10y', date_format='%m')
    exp_year = fake.credit_card_expire(start='now', end='+10y', date_format='%Y')
    customer_id = fake.uuid4()
    address_city = city
    address_country = fake.country()
    address_state = state
    address_zip = fake.zipcode()
    name_on_card = name
    
    cursor.execute('''
        INSERT INTO "account_stripemodel" (
            "card_id", "user_id", "card_number", "exp_month", "exp_year",
            "customer_id", "email", "address_city", "address_country",
            "address_state", "address_zip", "name_on_card"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (card_id, user_id, card_number, exp_month, exp_year, customer_id, email, address_city, address_country, address_state, address_zip, name_on_card))


# Commit changes and close the database connection
conn.commit()
conn.close()