from neo4j import GraphDatabase
import json

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
            hyperparametre = json.dumps(item['hyperparameters'])
            inputs = json.dumps(item['data'])

            session.run(
                """
                    MATCH (t:TypeDeModele{name:"Apprentissage Non Supervisé"})
                    MERGE (m:Modele {name:$algo})
                    MERGE (m)-[:EST_DE_TYPE]->(t)
                    MERGE (a:Algo {name:$algo})
                    MERGE (a)-[:IMPLEMENTE]->(m)
                    MERGE (p:Probleme {name: $name, description: $description})
                    MERGE (a)-[:RESOUT]->(p)
                    MERGE (e:ExempleConcret {name: $name, description: $description, hyperparametre: $hyp, inputs:$inputs})
                    MERGE (e)-[:EST_UN_EXEMPLE_DE]->(p)
                """,
                algo=algo,
                name=name,
                description=description,
                hyp=hyperparametre,
                inputs=inputs
            )
