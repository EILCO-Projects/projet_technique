from neo4j import GraphDatabase
import json

# Connexion à la base de données Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "Avenger158"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Lecture du fichier JSON
with open('algo_superv.json') as f:
    fl = json.load(f)

# Écriture des données dans la base de données Neo4j
with driver.session() as session:
    for key, data in fl.items():
        for item in data:
            modelName=item['name']
            algoName=item['algorithm'],
            hyperparametres=json.dumps(item['hyperparameters'])
            session.run(
                """
                    MATCH (t:TypeDeModele{name:'Apprentissage Supervisé'})
                    CREATE (m:Modele {name:$modelName})
                    CREATE (m)-[:EST_DE_TYPE]->(t)
                    CREATE (a:Algo {name: $algoName, hyperparametres: $hyperparametres})
                    CREATE (a)-[:IMPLEMENTE]->(m)

                """,
                modelName=modelName,
                algoName=algoName[0],
                hyperparametres=hyperparametres
            )
