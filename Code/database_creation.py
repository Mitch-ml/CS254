import sqlite3


def initailize_db(db_name):
    """Create a database for Jarvis that has two columns txt and action."""
    # Create database
    conn = sqlite3.connect(db_name)

    # Create cursor
    c = conn.cursor()

    # Create table and columns: txt and action
    c.execute(
        """CREATE TABLE training_data (
                txt text,
                action text
                )"""
    )

    # Commit table
    conn.commit()

    # Close database
    conn.close()


def insert_data(db_name, messages):
    """Insert values of training data into database.
    
    Arguments
    db_name : Name of database
    messages : A list a tuples (text, action)
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    with conn:
        c.executemany("INSERT INTO training_data VALUES (?,?)", messages)
    conn.close()


def db_head(db_name, n):
    """Print the first n rows of a database."""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    print(c.execute("SELECT * FROM training_data").fetchmany(n))
    conn.close()


# Initialize db
initailize_db("jarvis.db")

# Sample messages
messages = [
    ("What time is it right now?", "TIME"),
    ("What time is it, please?", "TIME"),
    ("What is the time now", "TIME"),
    ("Tell me the time right now!", "TIME"),
    ("Can you tell me the time?", "TIME"),
    ("Can you tell me what time it is?", "TIME"),
    ("Could you tell me the time?", "TIME"),
    ("Could you tell me what time it is?", "TIME"),
    ("Do you have the time？", "TIME"),
    ("Do you know what time it is?", "TIME"),

    ("I would like to order a pizza?", "PIZZA"),
    ("I would like a pizza?", "PIZZA"),
    ("Can I order a pizza?", "PIZZA")
    ("May I order a pizza?", "PIZZA")
    ( "Can I get a pizza?", "PIZZA")
    ("One large pizza please?", "PIZZA")
    ("One regular large pie,please!", "PIZZA"),
    ("Two regular slices，please!", "PIZZA"),
    ("Two slices of Sicilian,please!", "PIZZA"),
    ("Where's the nearest pizza place?", "PIZZA")

    # https://www.thespruce.com/how-to-respond-to-a-greeting-1216633
    ("It is so nice to see you again. Give your family my regards.", "GREET"),
    ("Hi! I have not seen you in a while. You look fabulous!", "GREET"),
    ( "Good morning! I wish I had more time to chat, but I have an appointment soon.", "GREET",),
    ("It is great seeing you. I hope you are doing well.", "GREET"),
    ("I am doing well! Thanks for asking. And how about you?", "GREET"),
    ( "Wow! It is been ages since we saw each other. \
        Let us get together soon when we both have more time to talk.", "GREET",
    )
    ("How's it going", "GREET")
    ("How are you", "GREET")
    ("How's it hanging", "GREET")
    ( "What's up", "GREET")
    ( "Long time no see", "GREET")

    ("How is the weather?", "WEATHER"),
    ("What is the weather like today? .", "WEATHER"),
    ("What does the weather forecast say?", "WEATHER"),
    ("Is it supposed to rain today?", "WEATHER"),
    ("Will it be sunny today?", "WEATHER"),
    ("Should I pack a raincoat today?", "WEATHER"),
    ("Should I bring an umbrella with me to work?", "WEATHER"),
    ("Will it snow today?", "WEATHER")
    ("Will it rain today?", "WEATHER")
    ("What's the weather forcast for today?", "WEATHER")

    ("Tell me a joke!", "JOKE"),
    ("Make me laugh.", "JOKE"),
    ("Tell me a funny story.", "JOKE"),
    ("Cheer me up.", "JOKE"),
    ("Could you tell me a joke?", "JOKE"),
    ("I want to laugh.", "JOKE"),
    ("Do you have any funny stories?", "JOKE"),
    ("What jokes do you know?", "JOKE"),
    ("Give me some jokes.", "JOKE"),
    ("Let's share some jokes", "JOKE"),
]

# Insert messages
insert_data("jarvis.db", messages)

# Preview first 5 rows
db_head("jarvis.db", 5)
