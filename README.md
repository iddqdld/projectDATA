# projectDATA

installation 

creation de virtual enviroment

``` python -m venv venv ```

``` .\venv\Scripts\Activate.bat ``` 

installation de biblio

``` pip install -r requirements.txt ```

to update req 

``` pip freeze > requirements.txt ```

Instructions pour contribuer au projet
1. Cloner le dépôt
Pour récupérer le projet localement :

bash
Copy
git clone <URL_DU_DÉPÔT>  
2. Créer une nouvelle branche
Synchronisez-vous avec la branche main :

bash
Copy
git checkout main  
git pull origin main  
Créez une branche pour vos modifications :

bash
Copy
git checkout -b nom-de-votre-branche  
Exemple :

bash
Copy
git checkout -b feature/login  
3. Travailler et pousser les modifications
Après vos changements, poussez la branche :

bash
Copy
git push origin nom-de-votre-branche  
4. Demander une revue et une fusion
Créez une Pull Request (PR) vers main via GitHub/GitLab.

Je vérifierai les modifications avant le merge.

📜 Règles importantes
⚠️ Interdiction de pousser directement vers main.

Utilisez des noms de branches descriptifs :

bash
Copy
# Bon :  
fix/header-error  
docs/update-readme  
# Mauvais :  
ma-branche  
test123  
Synchronisez votre branche avec main régulièrement :

bash
Copy
git pull origin main  
Seul le mainteneur (moi) peut merger dans main.

Merci pour votre collaboration ! 🌟

