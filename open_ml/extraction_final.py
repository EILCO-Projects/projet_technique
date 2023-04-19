import openml
import time
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "Avenger158"
driver = GraphDatabase.driver(uri, auth=(username, password))

openml.config.apikey = '401dcc51b3954ae4ba9fceb0fefc7fe8'


with driver.session() as session:
    all_runs = openml.runs.list_runs(offset=200, size=100)

    for run_id in all_runs:
        try:
            # Récupération de l'objet OpenMLRun pour chaque run
            run = openml.runs.get_run(run_id)
            flow = openml.flows.get_flow(run.flow_id)
            dataset = openml.datasets.get_dataset(run.dataset_id)
            task = openml.tasks.get_task(run.task_id)

            typeModel = ""
            if (task.task_type.upper() == "SUPERVISED CLASSIFICATION") or (task.task_type.upper() == "SUPERVISED REGRESSION") or (task.task_type.upper() == "LEARNING CURVE") or (task.task_type.upper() == "SUPERVISED DATASTREAM CLASSIFICATION"):
                typeModel = "Apprentissage Supervisé"
            elif (task.task_type.upper() == "CLUSTERING") or (task.task_type.upper() == "MACHINE LEARNING CHALLENGE") or (task.task_type.upper() == "SURVIVAL ANALYSIS") or (task.task_type.upper() == "SUBGROUP DISCOVERY"):
                typeModel = "Apprentissage Non Supervisé"
            else:
                typeModel = "Apprentissage Par Renforcement"

            session.run(
                """
                    MATCH (t:TypeDeModele{name:"Apprentissage Par Renforcement"})
                    MERGE (a:Algo {name:$name})
                    MERGE (a)-[:EST_DE_TYPE]->(t)
                    MERGE (p:Probleme{name:$runname, description: $description, data_url: $data_url})
                    MERGE (a)-[:RESOUT]->(p)
                """,
                typeDeModele=typeModel,
                name=flow.name,
                runname=dataset.name,
                description=dataset.description,
                data_url=dataset.original_data_url,
            )

            tags = flow.tags
            for tag in tags:
                session.run(
                    """
                    MATCH (p:Probleme{name:$name})
                    MERGE (t:Tag {name:$tag})
                    MERGE (t)-[:DESCRIT]->(p)
                """,
                    name=dataset.name,
                    tag=tag
                )

            for param in run.parameter_settings:
                i = 0
                for k, v in param.items():
                    # print(k,':',str(v)[6:-1])
                    i += 1
                    if (k != "oml:component"):
                        if (i == 1):
                            hypName = v
                        else:
                            hypValue = v
            session.run(
                """
                    MATCH (p:Probleme{name:$name})
                    MERGE (h:Hyperparametre {name: $hyp, valeurs: $val})
                    MERGE (h)-[:EST_UN_HYPERPARAMETRE]->(a)
                """,
                name=dataset.name,
                hyp=hypName,
                val=hypValue
            )

        except Exception as e:
            print("Error processing run ID", run_id, ":", str(e))
