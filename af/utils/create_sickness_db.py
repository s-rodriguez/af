import os
import random
import sqlite3

from af import af_directory


def get_directory_and_db_name():
    directory = os.path.join(af_directory(), 'utils', 'tests')
    name = 'sicknesslarge.db'
    return directory, name


class RandomRecord:

    @staticmethod
    def get_random_record():
        ssn = str(random.randrange(1000000,9000000))
        birth = RandomRecord.get_random_birth()
        race = RandomRecord.get_random_race()
        gender = RandomRecord.get_random_gender()
        zip_code = str(random.randrange(1000, 9999))
        problem = RandomRecord.get_random_problem()
        return ssn, race, birth, gender, zip_code, problem

    @staticmethod
    def get_random_birth():
        # USAR RANDOM DE DATETIME
        year = random.randint(1950, 1999)
        month = random.randint(1, 12)
        day = random.randint(1, 31)
        return "{0}/{1}/{2}".format(day, month, year)

    @staticmethod
    def get_random_race():
        return random.choice(['black', 'white'])

    @staticmethod
    def get_random_gender():
        return random.choice(['female', 'male'])

    @staticmethod
    def get_random_problem():
        problems_list = ['hiv', 'cancer', 'short of breath', 'chest pain', 'painful eye',
           'wheezing', 'obesity', 'hypertension', 'fever', 'vomiting', 'flu']
        return random.choice(problems_list)


def create_db(directory, db_name, number_of_records=100):
    print "[+] Creating Database if not exists ..."
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.isfile(os.path.join(directory, db_name)):
        os.remove(os.path.join(directory, db_name))

    with sqlite3.connect(os.path.join(directory, db_name)) as conn:
        cursor = conn.cursor()
        print "[+] Connection to database succesfull"

        print "[+] Creating table sickness ..."

        conn.execute('''CREATE TABLE sickness
               (SSN INT,
               RACE           CHAR(12)    NOT NULL,
               BIRTH           CHAR(12)    NOT NULL,
               GENDER        CHAR(12),
               ZIP         CHAR(6),
               PROBLEM        CHAR(20));''')

        print "[+] Table created successfully"

        print "[+] Inserting records into table ..."
        for i in range(0, number_of_records):
            new_record = RandomRecord.get_random_record()
            query = "INSERT INTO SICKNESS VALUES ( ?, ?, ?, ?, ?, ?)"
            conn.execute(query, new_record)

        conn.commit()
        print "[+] Done!"

if __name__ == "__main__":
    db_directory, db_name = get_directory_and_db_name()
    args = (db_directory, db_name, 1000)
    create_db(*args)
