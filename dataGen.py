import sqlite3
import random
from random import randint,
from faker import Faker
from datetime import datetime

# Initialize Faker
fake = Faker()

# Create or connect to the SQLite3 database
conn = sqlite3.connect('db.sqlite3')
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


# Generate and insert 1000 rows of fake data into auth_user table
for _ in range(1000):
    id = _
    password = fake.password()
    last_login = fake.date_time_this_decade()
    is_superuser = random.choice([True, False])
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = first_name[0] + last_name + randint(100, 999)
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

# Generate and insert 1000 rows of fake data into account_billingaddress table.  Names and user_id from auth_user table
    
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

# Generate and insert 1000 rows of fake data into the "account_stripemodel" table.  Names and some address fields from auth_user and account_billingaddress tables.
    
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

# Product information manually created and organized into dictionary
products = {
        "name":[
        "32 inch Outdoor Fire Pit & BBQ Pit w/ Accessories", 
        "2TB Samsung 980 PRO M.2 PCIe Gen 4 x4 NVMe Internal Solid State Drive",
        "64GB Nintendo Switch OLED Console (White)",
        "2-Count 5-52.5 lbs. FitRx Smart Bell Quick Select Adjustable Dumbbell (Black)",
        "eufy Clean RoboVac L50 SES Vacuum Cleaner",
        "Logitech G305 Lightspeed Wireless Gaming Mouse (Various Colors)",
        "120-Piece DeWALT Maxfit Ultra Steel Drill/Driving Bit Set w/ Storage Case",
        "Apple AirPods Bluetooth Earbuds w/ Lightning Charging Case (2nd Gen)",
        "2-Pack Govee 15 inch Wi-Fi RGBIC Smart TV Light Bars",
        "Thule Arcos Exterior Platform Hard Shell Cargo Box Carrier",
        "Timex Men's Expedition Scout 40mm Fabric Strap Watch w/ Blue Dial",
        "Galanz 3.3 cu. ft. Retro Compact Refrigerator (Red)",
        "Govee Bluetooth RGB LED Light Strips: 66.5' $14, 100'",
        "Dyson V8 Cordless Stick Origin Vacuum",
        "8 inch MIYABI Mizu SG2 Micro-Carbide Powder Stainless Steel Chef's Knife",
        "Huanuo Dual Monitor Adjustable Spring Stand Monitor Mount (13inch - 27inch Monitors)",
        "Arcade1up Marvel vs Capcom Head-to-Head Arcade Table",
        "Winix C909 4-Stage Air Purifier",
        "Lasko Ceramic Mini Tower Heater",
        "700c Giordano Duetto Tandem Bike",
        "JBL Bar 2.0 All-in-One Compact Soundbar",
        "Lisen 15W Wireless MagSafe Phone Car Vent Mount Charger",
        "40-Piece LEGO Super Heroes Batman 1992 Building Toy Set",
        "Yankee Candle Red Apple Wreath Scented, Classic 22oz Large Jar Single Wick Candle",
        "1.32-Lb Optimum Nutrition Micronized Creatine Monohydrate Powder (Unflavored)"
        ],
    "description":[
        "Fire Pits for Outside 32 Wood Burning Fire Pit Tables with Screen Lid Poker BBQ Net Ice Tray Food Clip and Cover Backyard Patio Garden Outdoor Fire Pit/Ice Pit/BBQ Fire Pit Black",
        "Next-level SSD performance: Unleash the power of the Samsung 980 PRO PCIe 4.0 NVMe SSD for next-level computing. 980 PRO delivers 2x the data transfer rate of PCIe 3.0, while maintaining compatibility with PCIe 3.0.",
        "Introducing the newest member of the Nintendo Switch family Play at home on the TV or on-the-go with a vibrant 7-inch OLED screen with the Nintendo Switch™ system - OLED model.",
        "These adjustable dumbbells let you customize each SmartBell’s weight in increments ranging from 5 to 52.5 lbs. The simple one-handed quick-select design makes them easy to use: just grip the handle and rotate it towards your desired weight. ",
        "Experience spotless, hands-free floorcare using the eufy RoboVac L50 Robot Vacuum Cleaner with Self-Empty Station. Ideal for hardwood floors and carpets, enjoy up to 60 days* of hands-free cleaning as the robot vacuum's impressive 4,000 Pa** suction power collects dirt and crumbs then auto empties into a dust bag within the separate bin. ",
        "HERO Gaming Sensor: Next-gen HERO mouse sensor delivers up to 10x the power efficiency over other gaming mice with exceptional accuracy and responsiveness thanks to 400 IPS precision and up to 12000 DPI sensitivity",
        "DEWALT MAXFIT Ultra Screwdriving bits help maximize your DEWALT power tool system. Featuring an ANTI-SNAP design, MAXFIT ULTRA Screwdriving Bits are reengineered to deliver up to 800 more screws per bit",
        "HIGH-QUALITY SOUND — Powered by the Apple H1 headphone chip, AirPods (2nd generation) deliver rich, vivid sound.",
        "Created For Your TV: Bring your entertainment, movies, sports, and gaming to life with the Govee RGBIC TV Light Bars. Use with the Govee Home App to control your light bars remotely or brighten your walls with preset scene modes and music modes.",
        "Easy to mount, Easy to Use. Box sits low to the ground, making it ergonomic and easy to load and unload cargo. Aerodynamic design for little impact on fuel consumption or on the range of your electric car. Premium cargo box, giving the car up to 14 cu ft of easily accessed, extra loading space",
        "Adjustable blue 20mm nylon strap with brown genuine leather trim fits up to 8-inch wrist circumference. Blue dial with date window at 3 o'clock; full Arabic numerals. Case Finish: Matte. Gray 40mm brass case with mineral glass crystal",
        "Retro Compact Refrigerator uses R600a high-efficiency and low-energy consumption compressor, it can cool food quickly with lower energy. Leveling legs can adjust feet and keep level placement anywhere",
        "100ft Extra Long Lighting: These LED strip lights for room are long enough to decorate and colorize larger areas giving you more coverage and more design options. Suitable for bedrooms, kitchens, stairs, dining rooms, ceilings, and home decorations.",
        "Dyson V8 Origin cordless vacuum cleaner is engineered with the power, versatility, tools and run time to clean homes with pets",
        "Micro Carbide powder steel SG2 construction (MC63); core is surrounded with a hammered stainless steel Damascus textured finish",
        "Fits two 13inch - 27inch flat/curved monitors w/ Vesa pattern 75x75 & 100x100. Each arm holds 4.4lbs - 14.3lbs. Swivel/tilt & rotate stand",
        "Bringing you authentic retro gaming experiences in an affordable and classic form, Arcade1Up head-to-heads are must-haves for your family game room, man cave, or a welcome distraction in the office",
        "Featuring a 4-stage air purification system, this unit removes 99.99% of airborne particles as small as 0.003 microns in size. Winix’s PlasmaWave® Technology may help to reduce the presence of airborne pollutants and contaminants.",
        "The CT14401 Ready Heat 14-inch Personal Ceramic Tower Heater from Lasko is perfect for tabletop or floor use. This small but mighty electric space heater features 1500 watts of comforting warmth making it ideal for the bedroom, home office, kitchen and more.",
        "Built around a 6061 lightweight aluminum frame and fork, Shimano 16 Speed Claris drivetrain, strong and lightweight 36 hole double wall rims, alloy dual pivot brakes and upright riding position you and your cycling partner will appreciate the smart and practical design approach.",
        "Enhance the drama of a tense thriller, feel the roar of your team or sit back with your latest album, the JBL bar 2.0 all-in-1 really is all-in-1, with deep bass for your movies and music",
        "Expert Holder fit for MagSafe: Our Master Wireless Car Phone Charger with Non-blocking/Mag safe Function is designed to create the perfect mood for every drivers' experience.",
        "40-Piece LEGO Super Heroes Batman 1992 Building Toy Set",
        "A happy holiday homecoming with the festive aroma of sweet apples, cinnamon, walnuts, and maple. Paraffin-grade wax delivers a clear, consistent burn. 110-150 hours burn time",
        "5 grams pure creatine monohydrate per serving. Supports increases in energy, endurance and recovery. Maximum potency supports muscle size, strength, and power. Supreme absorbency micronized to get the most out of each dose"
    ], 
    "price":[16649.57,
        "10658.18",
        "29143.45",
        "33306.80",
        "41633.50",
        "4163.35",
        "2498.01",
        "9992.04",
        "5828.69",
        "108247.10",
        "1915.14",
        "19068.14",
        "2081.68",
        "35804.81",
        "18235.47",
        "4996.02",
        "58286.90",
        "16653.40",
        "1748.61",
        "70776.95",
        "16653.40",
        "3330.68",
        "832.67",
        "1249.01",
        "2747.81"
        ], 
    "image":["firepit.jpg",
        "980proSSD.jpg",
        "switchOLED.jpg",
        "dumbell.jpg",
        "eufyVacuum.jpg",
        "g305mouse.jpg",
        "dewaltBitSet.jpg",
        "airpods.jpg",
        "tvLightBar.jpg",
        "thuleTrailerCase.jpg",
        "timexWatch.jpg",
        "galanzFridge.jpg",
        "ledStrip.jpg",
        "dysonVacuum.jpg",
        "miyabiKnife.jpg",
        "dualMonitorStand.jpg",
        "arcadeTable.jpg",
        "airPurifier.jpg",
        "towerHeater.jpg",
        "tendemBike.jpg",
        "jblSoundBar.jpg",
        "ventMount.jpg",
        "legoBatman.jpg",
        "yakeeCandle.jpg",
        "creatine.jpg"
        ],
    }

# Create the "product_product" table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS "product_product" (
        "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "name" VARCHAR(200) NOT NULL,
        "description" TEXT NOT NULL,
        "price" DECIMAL NOT NULL,
        "stock" BOOLEAN NOT NULL,
        "image" VARCHAR(100) NULL
    )
''')

# Insert products into the "product_product" table
for _ in range(25):
    id = _
    name = products["name"][_]
    description = products["description"][_]
    price = products["price"][_]
    stock = random.choice([True, False])
    image = products["image"][_]

    cursor.execute('''
        INSERT INTO "product_product" (
            "id", "name", "description", "price", "stock", "image"
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (id, name, description, price, stock, image))

# Commit changes and close the database connection
conn.commit()
conn.close()

# Create the "account_ordermodel" table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS "account_ordermodel" (
        "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "name" VARCHAR(120) NOT NULL,
        "card_number" VARCHAR(4) NULL,
        "address" VARCHAR(300) NULL,
        "paid_status" BOOLEAN NOT NULL,
        "total_price" DECIMAL NULL,
        "is_delivered" BOOLEAN NOT NULL,
        "delivered_at" VARCHAR(200) NULL,
        "user_id" INTEGER NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
        "ordered_item" VARCHAR(200) NULL,
        "paid_at" DATETIME NULL
    )
''')

# Generate and insert 5000 rows into the "account_ordermodel" table
for _ in range(5000):
    # Join the first three tables to get user, billing address, and credit card information
    cursor.execute('''
        SELECT 
            u.id AS user_id, b.name AS user_name, s.card_number, b.house_no, b.landmark, b.city, b.state, b.pin_code
        FROM auth_user AS u
        JOIN account_billingaddress AS b ON u.id = b.user_id
        JOIN account_stripemodel AS s ON u.id = s.user_id
        ORDER BY RANDOM()
        LIMIT 1
    ''')
    user_data = cursor.fetchone()

    # Select a random product from the "product_product" table
    cursor.execute('SELECT * FROM product_product ORDER BY RANDOM() LIMIT 1')
    product_data = cursor.fetchone()

    # Generate order data
    name = user_data[1]
    card_number = user_data[2][-4:] if user_data[2] else None
    address = f"{user_data[3]} {user_data[4]}, {user_data[5]}, {user_data[6]} {user_data[7]}"
    paid_status = random.choice([True, False])
    total_price = product_data[3]
    is_delivered = random.choice([True, False])
    delivered_at = fake.date_time_this_decade() if is_delivered else None
    ordered_item = product_data[1]
    paid_at = fake.date_time_this_decade() if paid_status else None

     # Insert data into the "account_ordermodel" table
    cursor.execute('''
        INSERT INTO "account_ordermodel" (
            "name", "card_number", "address", "paid_status", "total_price",
            "is_delivered", "delivered_at", "user_id", "ordered_item", "paid_at"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, card_number, address, paid_status, total_price, is_delivered, delivered_at, user_data[0], ordered_item, paid_at))

# Commit changes and close the database connection
conn.commit()
conn.close()
