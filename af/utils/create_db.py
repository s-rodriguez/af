from datetime import datetime
import random
import string

import sqlite3


def random_letters():
    return ''.join([random.choice(string.ascii_lowercase) for x in range(0, random.randint(6, 10))])


def random_year_of_birth():
    return random.randint(1930, 2000)


def random_gender():
    return random.choice(['Male', 'Female'])


def random_ethnicity():
    return random.choice(['A', 'B', 'C'])


def random_zip():
    return int(''.join([str(random.randint(1,9)) for i in range(0, 5)]))


def random_diagnosis():
    return random.randint(1, 4)


def create_record():
    name = random_letters()
    surname = random_letters()
    year_of_birth = random_year_of_birth()
    gender = random_gender()
    ethnicity = random_ethnicity()
    z = random_zip()
    diagnosis = random_diagnosis()
    return name, surname, year_of_birth, gender, ethnicity, z, diagnosis


def create_db(records_amount):
    conn = sqlite3.connect(r"medical_info.db")
    cursor = conn.cursor()
    print "Delete table if exists"
    cursor.execute('''DROP TABLE IF EXISTS patients ''')

    print "Create table"
    cursor.execute('''CREATE TABLE patients
     (name text, surname text, year_of_birth integer, gender text, ethnicity text, zip integer, diagnosis integer)''')

    print "Populate table"

    print "Creating records.."
    records = [create_record() for i in range(records_amount)]

    print "Inserting records into the db"
    cursor.executemany('INSERT INTO patients VALUES (?,?,?,?,?,?,?)', records)

    cursor.close()
    conn.commit()
    conn.close()

def read_db_info():
    conn = sqlite3.connect(r"medical_info.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    for r in cursor:
        print r

if __name__ == '__main__':
    records_amount = 10000
    create_db(records_amount)
    read_db_info()
