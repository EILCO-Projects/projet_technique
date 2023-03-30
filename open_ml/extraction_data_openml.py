import openml
import pathlib
openml.config.apikey = '401dcc51b3954ae4ba9fceb0fefc7fe8'

# Récupération de la liste des tâches
datasets = openml.datasets.list_datasets(output_format="dataframe")

# Get specific dataset
dataset = openml.datasets.get_dataset(61)

run = openml.runs.get_run(81)

flow = openml.flows.get_flow(run.flow_id)
print(flow.parameters)






# for e in run.parameter_settings:
# table = [v for _,v in e.items()]
# print(table[:-1])

# benchmark = openml.study.get_suite("OpenML-friendly")

# task = openml.tasks.list_tasks(output_format="dataframe", task_id=benchmark.tasks)

# evaluations = openml.evaluations.list_evaluations(
#     function="area_under_roc_curve",
#     tasks=benchmark.tasks,
#     output_format="dataframe"
# )


# Qualities (Autocorrelation, etc...)
# print(dataset.qualities)

# Features
# for k,v in dataset.features.items():
#     print(k,':',str(v)[6:-1])

# tag = dataset.tag
# del(dataset.tag)

# Retrieve dataset info
# tag = dataset.tag #list
# name = dataset.name

# Create file with data under json format
# X, y, _, _ = dataset.get_data(dataset_format="dataframe")
# with open(f'{dataset.name}.json', 'w') as f:
#     X.to_json(f.name)
#     dataset.data = (f'{pathlib.Path().resolve()}/{f.name}')

# # Récupération de la liste des modèles supervisés
# classifiers = openml.models.list_models(model_type=1, output_format='dataframe')

# # Récupération de la liste des exécutions pour chaque tâche
# runs = {}
# for task_id in tasks['tid']:
#     try:
#         task_runs = openml.runs.list_runs(task=[task_id], output_format='dataframe')
#         runs[task_id] = task_runs
#     except openml.exceptions.OpenMLServerException:
#         pass

# # Affichage des résultats
# print('Liste des tâches :')
# print(tasks.head())

# print('\nListe des modèles supervisés :')
# print(classifiers.head())

# print('\nListe des exécutions :')
# for task_id, task_runs in runs.items():
#     print(f'Tâche {task_id} :')
#     print(task_runs.head())
