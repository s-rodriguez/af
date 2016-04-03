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
        city = RandomRecord.get_random_city()
        profession = RandomRecord.get_random_profession()
        problem = RandomRecord.get_random_problem()
        return ssn, gender, birth, race, zip_code, city, profession, problem

    @staticmethod
    def get_random_birth():
        # USAR RANDOM DE DATETIME
        year = random.randint(1950, 1999)
        month = random.randint(1, 12)
        day = random.randint(1, 31)
        return "{0}/{1}/{2}".format(day, month, year)

    @staticmethod
    def get_random_race():
        return random.choice(['female', 'male'])

    @staticmethod
    def get_random_gender():
        return random.choice(['black', 'white'])

    @staticmethod
    def get_random_problem():
        problems_list = ['hiv', 'cancer', 'short of breath', 'chest pain', 'painful eye',
                         'wheezing', 'obesity', 'hypertension', 'fever', 'vomiting', 'flu', 'asthma',
                         'diabetes', 'depression', 'alzheimer', 'arthritis', 'epilepsy',
                         'epilepsy', 'lupus', 'migraine', 'scoliosis', 'ulcers']
        return random.choice(problems_list)

    @staticmethod
    def get_random_city():
        city_list = ['Rosario', 'Santa Fe Cap', 'Reconquista', 'Rafaela', 'Firmat', 'Sunchales',
                         'La Plata', 'Avellaneda', 'Ciudad de Buenos Aires', 'Mar del Plata', 'La Matanza', 'San Martin', 'Bahia Blanca', 'Tandil', 'Pergamino',
                         'Parana', 'Gualeguay', 'Gualeguaychu', 'Victoria', 'Colon', 'Concepcion del Uruguay',
                         'Cordoba Cap', 'Sierra de los Padres', 'Mina Clavero', 'Rio Cuarto', 'Rio Tercero', 'Villa Gral Belgrano',
                         'Mendoza Cap', 'San Rafael', 'Malargue', 'Las Heras', 'Guaymallen', 'Maipu',
                         'Salta Cap', 'Cachi', 'Cafayate', 'Iruya', 'Tartagal', 'Angastaco']
        return random.choice(city_list)

    @staticmethod
    def get_random_profession():
        profession_list = ['Endocrinology', 'Cardiology', 'Geriatrics', 'Paediatrics', 'Neurology', 'Radiology',
                         'Civil Attorney', 'Criminal Attorney', 'Employment Attorney', 'Family Attorney', 'Administrative Attorney',
                         'Civil Engineering', 'Chemical Engineering', 'Software Engineering', 'Mechanical Engineering', 'Industrial Engineering',
                         'Mathematician', 'Biologist', 'Physicist', 'Chemist', 'Geologist',
                         'Plumber', 'Electrician', 'Carpenter', 'Shoemaker', 'Blacksmith', 'Builder']
        return random.choice(profession_list)


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
               CITY        CHAR(32),
               PROFESSION CHAR(32),
               PROBLEM        CHAR(20));''')

        print "[+] Table created successfully"

        print "[+] Inserting records into table ..."
        for i in range(0, number_of_records):
            new_record = RandomRecord.get_random_record()
            query = "INSERT INTO SICKNESS VALUES ( ?, ?, ?, ?, ?, ?,?, ?)"
            conn.execute(query, new_record)

        conn.commit()
        print "[+] Done!"

if __name__ == "__main__":
    db_directory, db_name = get_directory_and_db_name()
    args = (db_directory, db_name, 100)
    create_db(*args)
