from af.model.algorithms.Datafly import Datafly
from af.model.algorithms.IncognitoK import IncognitoK
from af.model.algorithms.IncognitoL import IncognitoL


def create_sickness_db(number_of_records):
    import af.utils.create_sickness_db as create_sickness_db
    db_directory, db_name = create_sickness_db.get_directory_and_db_name()
    create_sickness_db.create_db(db_directory, db_name, number_of_records)


if __name__ == "__main__":
    create_db = raw_input("Crear DB sickness? [y/N]: ")
    if create_db.lower() == "y":
        number_of_records = int(raw_input("Cantidad de registros random: "))
        create_sickness_db(number_of_records)

    print "\nCreando Data Config a partir de la base sicknesslarge.db"
    from af.utils import create_full_data_config
    dc = create_full_data_config.data_config

    algorithm = raw_input("\nAlgoritmo a usar (Datafly [1] / IncognitoK [2] / IncognitoL [3]): ")
    k_value = int(raw_input("Valor de K: "))

    if algorithm.lower() in ("1", "datafly", "datafly [1]"):
        algorithm_instance = Datafly(dc, k=k_value)

    elif algorithm.lower() in ("2", "incognitok", "incognitok [2]"):
        algorithm_instance = IncognitoK(dc, k=k_value)

    elif algorithm.lower() in ("3", "incognitol", "incognitol [3]"):
        l_value = int(raw_input("Valor de L: "))
        algorithm_instance = IncognitoL(dc, k=k_value, l=l_value)

    else:
        print "\nAlgoritmo seleccionado incorrecto"
        exit(-1)

    print "\n{0} anonimizando ...".format(algorithm_instance.__class__.__name__)
    algorithm_instance.anonymize()
    print "\nDone!"
