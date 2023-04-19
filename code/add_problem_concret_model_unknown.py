from neo4j import GraphDatabase
import json
import os

# Connexion à la base de données Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "Avenger158"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Lecture du fichier JSON
with open('../data/problemes_concrets_non_supervises.json') as f:
    fl = json.load(f)

# Écriture des données dans la base de données Neo4j
with driver.session() as session:
    for key, data in fl.items():
        for item in data:
            algo = item['model_name']
            name = item['problem_name']
            description = item['problem_description']
            hyperparametre = item['hyperparameters']
            inputs = item['data']

            with open(f'../inputs_for_problems/unsupervised/{name}.txt', 'w') as f:
                for k, v in inputs.items():
                    f.write(f'{k} : {v}\n')

            inputLink = os.path.dirname(
                os.getcwd()) + f"/inputs_for_problems/unsupervised/{name}.txt"

            session.run(
                """
                    MATCH (t:TypeDeModele{name:"Apprentissage Non Supervisé"})
                    MERGE (m:Modele {name:$algo})
                    MERGE (m)-[:EST_DE_TYPE]->(t)
                    MERGE (a:Algo {name:$algo})
                    MERGE (a)-[:IMPLEMENTE]->(m)
                    MERGE (p:Probleme {name: $name, description: $description,  data_url:$inputs})
                    MERGE (a)-[:RESOUT]->(p)
                """,
                algo=algo,
                name=name,
                description=description,
                inputs=inputLink
            )
            for k, v in hyperparametre.items():
                hypName = k
                if (type(v) == list):
                    hypValue = ', '.join(v if type(v) == str else str(v))
                elif (type(v) == str):
                    hypValue = v
                elif (type(v) == dict):
                    hypValue = json.dumps(v)
                else:
                    hypValue = str(v)

                session.run(
                    """
                        MATCH (p:Probleme{name:$name})
                        MERGE (h:Hyperparametre {name: $hyp, valeurs: $val})
                        MERGE (h)-[:EST_UN_HYPERPARAMETRE]->(p)
                    """,
                    name=name,
                    hyp=hypName,
                    val=hypValue
                )
