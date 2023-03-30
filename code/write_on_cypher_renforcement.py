from neo4j import GraphDatabase
import json

# Connexion à la base de données Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "Avenger158"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Lecture du fichier JSON
with open('../data/algo_renforcem.json') as f:
    fl = json.load(f)

# Écriture des données dans la base de données Neo4j
with driver.session() as session:
    for key, data in fl.items():
        for item in data:
            name=item['Nom']
            hyperparametres=item['Hyperparametres']
            session.run(
                """
                    MATCH (t:TypeDeModele{name:'Apprentissage Par Renforcement'})
                    MERGE (a:Algo {name: $algoname})
                    MERGE (a)-[:EST_DE_TYPE]->(t)
                """,
                algoname=name
            )

            for k, v in hyperparametres.items():
                    hypName = k
                    if (type(v) == list):
                        hypValues = '|'.join(str(e) if isinstance(
                            e, (int, float)) else e for e in v)

                    elif (type(v) == dict):
                        hypValues = json.dumps(v)
                    else:
                        hypValues = str(v)
                    session.run(
                        """
                            MATCH (a:Algo {name:$algoName})
                            MERGE (h:Hyperparametre {name: $name, valeurs: $valeurs})
                            MERGE (h)-[:EST_UN_HYPERPARAMETRE]->(a)
                        """,
                        algoName=name,
                        name=hypName,
                        valeurs=hypValues
                    )
