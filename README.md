# Recherche dans les bulletins municipaux officiels de la ville de Paris

Cet outil vous permet d'effectuer des recherches dans les bulletins de la ville de Paris, 
publiés bi-hebdomadairement sur https://www.paris.fr/bmo .

L'outil se décompose en trois parties : 

- Le script `init.sql` permet de créer les tables nécessaires. (à lancer au début du projet)
- Le script `test_import.py` permet de récupérer le contenu des pdfs distribués par la mairie et de remplir/mettre à jour la base de données.
(à lancer régulièrement, suivant la fréquence d'ajout de nouveaux PDFs)
- Une application Django produit une interface permettant de découvrir le contenu des BMOs.
