# SQLAlchemy

C’est un ORL, un truc qui soigne les bobos aux oreilles.
Bon ok c’est faux c’est un Object Relational Mapper, qui permet en gros de concevoir des bases de données relationnelles à partir de classes.

Il faut commencer par faire un fichier Model qui représentera la déclaration de la table.

## Déclaration du Modèle

Afin de déclarer une table, on utilisera une déclaration de classe standard :
```python
from sqlalchemy.ext.declarative import declarative_base

Schema = declarative_base()

class MaTable(Schema):
	…
```
On remarque que cette classe hérite d’une autre qui s’appelle `Schema` et qui représente tout notre système relationnel. On en reparle plus tard.

Une classe *SQLalchemy* ne représente pas véritable la table mais un enregistrement de celle-ci, aussi on appellera cette classe pour créer les données d’une ligne.

Dans la documentation, il est aussi possible de déclarer les tables avec la classe `Table` mais pour l’instant on va laisser ça de côté.
#### Nom de la table
tout d’abord la variable locale `__tablename__` va servir à nommer la table dans le système. Si jamais on veut accéder à un attribut de celle-ci, par exemple pour désigner une clef étrangère, on utilisera la syntaxe `<nom_tabe>.<attribut>`.
#### Attributs
Chaque attribut est ensuite déclaré comme une variable dans la classe, mais pas avec `self` devant, ni dans le `def init`. Non, on déclarera juste un attribut comme une instance de la classe `Column`. Il convient ensuite de lui passer en paramètre les contraintes souhaitées, comme le [type de donnée](https://docs.sqlalchemy.org/en/20/core/types.html) ou si c’est une clef.
```python
from sqlalchemy import Column, Integer, String
	…
	attribut_1 = Column(Integer, primary_key=True)
    attribut_2 = Column(String(255))
```
#### Clef étrangères
Les clef étrangères sont déclarées différemment des clef primaires. Il faut passer une classe `ForeignKey` à la colonne, mais aussi déclarer une fonction `relationship()` 
```python
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

    table2_id = Column(Integer, ForeignKey("table2.id"))
    table2 = relationship("Table2")
```
La fonction de relation permet de définir le type de relation et la logique en cas d’opérations, comme les [cascades](https://docs.sqlalchemy.org/en/20/orm/cascades.html#unitofwork-cascades).

## Utilisation du Modèle

#### Instanciation du moteur
Dans le script principal, la première chose à faire est d’instancier un moteur avec `create_engine`. Exemple :
```python
from sqlalchemy import create_engine

engine = create_engine(
	f"mysql+pymysql://{username}:{password}@{ip}:{port}/{db_name}"
	)
```
Ici la partie `mysql+pymysql` fait référence au [dialecte](https://docs.sqlalchemy.org/en/20/dialects/index.html) relationnel ainsi qu’au pilote de ce dialecte.

Une façon plus propre de procéder utilise la classe URL. C’est surtout utile en cas de caractères spéciaux dans le mot de passe.
```python
from sqlalchemy import URL

url_object = URL.create(
    "postgresql+pg8000",
    username="dbuser",
    password="kx@jj5/g",
    host="pghost10",
    port="8888",
    database="appdb",
)

engine = create_engine(url_object)
```

Ensuite une série de méthodes génériques peuvent être importées depuis le module **`sqlalchemy_utils`**, comme `database_exists`, `create_database` ou `drop_database`.
#### Importation du Modèle
Depuis notre module de modèle, il faut importer les classes de chacune de nos tables ainsi que bien sur la fameuse classe `Schema`.

La méthode `create_all` dans cette classe nous permet de lancer d’un coup la création de toute la base. On lui passe le moteur relationnel en paramètre. Me demandez pas pourquoi.
```python
Schema.metadata.create_all(engine)
```
#### Opérations sur la BDD
Une fois la base de donnée créée, il faut faire des opérations dessus comme les insert, les select, tu connais. Pour ce faire, on doit créer une session, qui sera notre point d’entrée dans les interactions avec la base de données.
Cette session est une instance d’une classe que nous devons appeler avec une fonction, comme nous l’avions fait pour Schema.
```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
```
#### Utilisation de la session
La session possède tout un tas de [méthodes](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) classiques : 

- `session.commit()` : Pour valider les changements réalisés sur la base. On peut tout annuler avec `.rollback()`, comme de coutume.
- `session.add()` : Pour ajouter un enregistrement dans une base. Il faut donc lui passer en paramètre l’instance de la classe de la table dans laquelle on souhaite écrire. Par exemple, le code ci dessous écrira dans la table User : 
```python
new_user = User(name='biloute', job='postier')
session.add(new_user)
```
#### Session Query
- `session.query(TableClass)`: C’est comme ça que l’on fait les SELECT avec SQLAlchemy. Il y a toute une série de méthodes pour affiner la recherche :
	- `query.filter_by(attribut='value')`: équivalent des WHERE.
	- `query.all()` : toute la table
#### Jointures
Une requête peut être assez complexe, voici un exemple de jointure : 
```python
result = session.query(
    User.name,
    User.job,
    City.name.label('city'),  # label fonctionne comme AS en sql
).join(City, User.city_id == City.id).all()
```
Ici on selectionne le nom et le métier sur la table Users, puis on récupère le nom de la ville avec la jointure sur l’id de ville. Easy.
Pour faire des jointures multiples, il n‘y a qu’a enchainer les méthodes `.join()`.