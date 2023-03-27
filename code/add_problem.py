from neo4j import GraphDatabase
import json

# Connexion à la base de données Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "Avenger158"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Lecture du fichier JSON
with open('problems.json') as f:
    fl = json.load(f)

# Écriture des données dans la base de données Neo4j
with driver.session() as session:
    for key, data in fl.items():
        for item in data:
            # algo=key,
            # name=item['Probleme']
            # description=item['Description']
            # session.run(
            #     """
            #         MATCH (a:Algo {name:$algo})
            #         MERGE (p:Probleme {name: $name, description: $description})
            #         MERGE (a)-[:RESOUT]->(p)
            #     """,
            #     algo=algo[0],
            #     name=name,
            #     description=description
            # )
            
            # When you try to add problems that refers to unknwon model, the
            # below code create a new one and link it to the related problem.

            algo=key,
            name=item['Probleme']
            description=item['Description']
            session.run(
                """
                    MATCH (t:TypeDeModele{name:"Apprentissage Non Supervisé"})
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
