from neo4j import GraphDatabase
import json

# Connexion à la base de données Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "Avenger158"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Lecture du fichier JSON
with open('algo_renforcem.json') as f:
    fl = json.load(f)

# Écriture des données dans la base de données Neo4j
with driver.session() as session:
    for key, data in fl.items():
        for item in data:
            name=item['Nom']
            hyperparametres=json.dumps(item['Hyperparametres'])
            session.run(
                """
                    MATCH (t:TypeDeModele{name:'Apprentissage Par Renforcement'})
                    CREATE (m:Modele {name:$name})
                    CREATE (m)-[:EST_DE_TYPE]->(t)
                    CREATE (a:Algo {name: $algoname, hyperparametres: $hyperparametres})
                    CREATE (a)-[:IMPLEMENTE]->(m)
                """,
                name=name,
                algoname=name,
                hyperparametres=hyperparametres
            )
