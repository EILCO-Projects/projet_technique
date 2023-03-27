from neo4j import GraphDatabase
import json

# Connexion à la base de données Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "Avenger158"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Lecture du fichier JSON
with open('problem_renforcem.json') as f:
    fl = json.load(f)

# Écriture des données dans la base de données Neo4j
with driver.session() as session:
    for key, data in fl.items():
        for item in data:
            algo = item['Nom'],
            for problem in item['Problemes']:
                name = problem['Nom']
                description = problem['Description']
                session.run(
                    """
                        MATCH (t:TypeDeModele{name:"Apprentissage Par Renforcement"})
                        MERGE (m:Modele {name:$algo})
                        MERGE (m)-[:EST_DE_TYPE]->(t)
                        MERGE (a:Algo {name:$algo})
                        MERGE (a)-[:IMPLEMENTE]->(m)
                        MERGE (p:Probleme {name: $name, description: $description})
                        MERGE (a)-[:RESOUT]->(p)
                    """,
                    algo=algo[0],
                    name=name,
                    description=description
                )
