import sqlite3
from datetime import datetime, timedelta

def db(db_str):
    con = sqlite3.connect('data.db')
    c = con.cursor()
    print(db_str)
    c.execute(db_str)
    output = c.fetchall()
    con.commit()
    con.close()
    return output

def db_create_table():
    db_str = "CREATE TABLE jobs(account INTEGER, job TEXT, time datetime)"
    db(db_str)

def db_delete_table(table):
    db_str = f"DROP TABLE {table}"
    db(db_str)

def db_add(account, job, time):
    db_str = f"INSERT INTO jobs VALUES ({account}, '{job}', '{time}')"
    db(db_str)

def db_update(account, job, time):
    db_str = f"SELECT * FROM jobs WHERE account='{account}' and job = '{job}'"
    existing = len(db(db_str))
    print("Current Records: ", existing)
    if existing == 1:
        db_str = f"UPDATE jobs SET time='{time}' WHERE account = {account} AND job = '{job}'"
        db(db_str)
    else:
        print("Records not updated")

def db_delete(rowid):
    if rowid == "all":
        db_str = f"DELETE from jobs"
    else:
        db_str = f"DELETE from jobs WHERE rowid = {rowid}"
    db(db_str)

def db_view(account='all'):
    if account == 'all':
        db_str = "SELECT * FROM jobs ORDER BY time"
    else:
        db_str = f"SELECT * FROM jobs WHERE account='{account}' ORDER BY time"
    output = db(db_str)
    count = 0
    for x in output:
        if count < 30:
            if x[2] is None:
                time = "None"
            else:
                time = string_to_time(x[2])
                time = time_to_string(time)
            tabs = "\t"
            if len(x[1]) <= 5: tabs += "\t"
            if len(x[1]) <= 9: tabs += "\t"
            print("Account:", x[0], " Job:", x[1], tabs + "Time:", x[2])
        count += 1

def string_to_time(time):
    try:
        return datetime.fromisoformat(time)
    except:
        return datetime.now()

def time_to_string(time):
    if time <= datetime.now():
        return "Now"
    else:
        return time.strftime('%d %b %I:%M%p')


def initial_entries():
    db_delete('all')
    time = datetime.now() + timedelta(days=14)
    for x in range(1,4):
        for y in ["build", "attack", "build_b", "attack_b", "clock", "coin", "research", "research_b"]:
            db_add(x, y, time)

def add_entries():
    time = datetime.now() + timedelta(days=14)
    for x in range(1,4):
        for y in ["donate",]:
            db_add(x, y, time)

def update_entries():
    time = datetime.now() + timedelta(minutes=5)
    for x in range(1,3):
        for y in ["build",]:
            db_update(x, y, time)



# db_delete('all')
# db_delete_table('jobs')
# db_create_table()
# db_add(2, "attack", datetime.datetime.now())

# update_entries()
for x in [2,]:
    db_update(x, "attack", datetime.now() + timedelta(minutes=-20))
db_view()
