from neo4j import GraphDatabase
import spacy
# Traiter les informations renseignées par l'utilisateur et retourner les élements importants
nlp = spacy.load("fr_core_news_sm")

# Traitez le texte pour obtenir un objet Doc
doc = nlp(input("Votre question: "))

# Itérez sur les tokens et affichez leur forme lemmatisée
nouns = [token.lemma_ for token in doc if (token.pos_ == "NOUN")]
adj = [token.lemma_ for token in doc if (token.pos_ == "ADJ")]

data = ''
for a in adj:
    data += a + " "

for n in nouns:
    data += n + " "

uri = "bolt://localhost:7687"
username = "neo4j"
password = "Avenger158"
driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    res = session.run("""
        MATCH (n)
        WITH n, apoc.text.sorensenDiceSimilarity(n.name, $input_data) AS sim
        RETURN n.name as name, labels(n)[0] as label, sim
        ORDER BY sim DESC
     """, input_data=data)

    print('\nDes problèmes similaires\n')

    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(' Nom                                                                                                | Type                         | Similarité               ')
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for record in res:
        print(' ', record['name'], end="")
        for i in range(100 - len(record['name'])):
            print(' ', end="")

        print(' ', record['label'], end='')
        for i in range(28 - len(record['label'])):
            print(' ', end="")
        print(record['sim'])
        print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")

driver.close()
