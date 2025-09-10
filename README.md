# Nicolas OSBORNE

# Clean Architecture - TP Refactoring SOLID

## Contexte

Ce TP est réalisé dans le cadre du module "Clean Architecture" en M2 Ingénierie du Web à l'ESGI, dispensé par Laurent BELLON.

## Objectif du TP

Ce TP a pour objectif la refactorisation du code d'un petit système de gestion de produits déjà existant, de manière à respecter les principes SOLID de Clean Architecture.
Voici les différentes étapes à réaliser pour ce TP :

- Identifier les violations des principes SOLID
- Appliquer les principes pour les corriger
- Implémenter une nouvelle fonctionnalité de recherche par catégorie ou par prix maximum

L'énoncé des attentes et des étapes de réalisation du TP, ainsi que la base de code de départ sont disponibles dans le fichier [TP_Enonce](TP_Enonce.md).

## Étape 1 : Analyse et Identification des Violations

En explorant et analysant le code existant, il est possible de mettre en évidence une certaine rigidité dans le code, et une violation de plusieurs principes fondamentaux SOLID. Voici la liste des principes, et les emplacements où le code viole ces principes :

1.  **Principe de Responsabilité Unique (SRP) :**
    La classe `ProductService` viole le SRP car elle a de multiples responsabilités :

- Elle s'occupe d'orchestrer la logique métier (CRUD des produits) :

```python
 def create_product

 def get_product

 def get_all_products

 def update_product

 def delete_product
```

- Elle gère la validation des données (vérification du nom et du prix) :

```python
if not name or not price or price <= 0:
   raise ValueError("Nom et prix sont requis, et le prix doit être positif.")

if not product:
   raise ValueError("Produit non trouvé.")

if not name or not price or price <= 0:
   raise ValueError("Nom et prix sont requis, et le prix doit être positif.")
```

- Elle gère la persistance des données directement via le `ProductRepository` :

```python
def __init__(self):
   self.repository = ProductRepository()
```

Si l'on souhaite changer une règle de validation, la manière dont les données sont persistées, ou bien encore l'ajout d'une nouvelle logique métier, cela implique d'effectuer des modifications dans `ProductService`, ce qui est une violation du principe SRP.

2.  **Principe Ouvert/Fermé (OCP) :**
    À nouveau, c'est la classe `ProductService` qui viole le principe OCP. En effet, si l'on souhaite ajouter une nouvelle règle de validation d'un produit, on doit venir modifier directement les méthodes dans `ProductService` (`create_product` ou `update_product` par exemple).
    La classe n'est donc pas "Fermée à la modification" comme le souhaite le principe OCP.

3.  **Principe de Substitution de Liskov (LSP) :**
    En l'état, il n'existe pas encore de hiérarchie dans les classes, donc il n'y a pas de violation du principe LSP dans le code de base. Cependant, si l'on vient à créer de nouvelles classes dérivées de Product, c'est un principe à bien penser à prendre en compte.

4.  **Principe de Ségrégation d'Interface (ISP) :**
    Dans le code de base, il n'existe pas encore d'interface, donc encore une fois il n'y a pas de violation du principe ISP.

5.  **Principe d'Inversion des Dépendances (DIP) :**
    Enfin, comme expliqué précédemment dans le deuxième point sur l'OCP, la classe de haut niveau `ProductService` dépend directement de la classe de bas niveau `ProductRepository`, au lieu de dépendre d'une abstraction via une interface, ce qui est une violation du principe DIP.

## Étape 2 : Application du Principe de Responsabilité Unique (SRP)

Afin d'appliquer le Principe SRP, il est nécessaire de découper `ProductService` en classes distinctes, chacune avec sa propre responsabilité :

- `ProductValidator` : Validation d'un produit
- `ProductCreator` : Création d'un produit
- `ProductRetriever` : Lecture d'un ou des produit(s)
- `ProductUpdater` : Mise à jour d'un produit
- `ProductDeleter` : Suppression d'un produit

Chaque classe est séparée dans un fichier distinct pour bien séparer les responsabilités, et chaque classe a bien sa responsabilité unique.

## Étape 3 : Application du Principe Ouvert/Fermé (OCP) et d'Inversion des Dépendances (DIP)

L'objectif de cette étape est de découpler les nouvelles classes de services créées lors de l'étape précédente et l'implémentation du `ProductRepository`.
Il faut pour cela créer une interface `IProductRepository` pour introduire une abstraction, afin que les classes de haut niveau (`ProductCreator`, `ProductRetriever`, `ProductUpdater`, `ProductDeleter`) ne dépendent plus directement du module de plus bas niveau `ProductRepository`, mais de cette nouvelle interface `IProductRepository` via l'injection de dépendances par constructeur.
Ainsi, cette nouvelle implémentation permettra de respecter le principe d'Inversion des Dépendances DIP.

Pour ce qui est du principe OCP, grâce à cette nouvelle abstraction, le code est désormais bien "Ouvert à l'extension, mais fermé à la modification".
Désormais, si ce système devait venir à gérer des types de produits différents (par exemple `PhysicalProduct` et `DigitalProduct`), il n'est plus nécessaire de devoir modifier directement la classe d'origine `ProductService`, mais il suffirait de créer de nouvelles classes comme `PhysicalProductCreator` qui implémenterait une classe `PhysicalProductValidator` et `IProductRepository`.
Ainsi, ajouter de nouvelles règles de validation, de nouveaux types de produits ou de nouvelles sources de données ne casserait pas l'OCP et permettraient au contraire d'effectivement garder un code "Ouvert à l'extension, mais fermé à la modification".

## Étape 4 : Application du Principe de Ségrégation des Interface (ISP) et de Substitution de Liskov (LSP)

Après l'étape précédente et la création de l'interface `IProductRepository`, nous pouvons voir que celle-ci contient toutes les opérations CRUD :

```python
class IProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product) -> Product:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    def update(self, product: Product) -> bool:
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        pass
```

Or, chaque client de cette interface n'a généralement besoin que d'une seule (ou deux) de ces méthodes :

- `ProductCreator` n'a besoin que de la méthode `add`
- `ProductDeleter` n'a besoin que de la méthode `delete`
- `ProductUpdater` n'a besoin que des méthodes `get_by_id` et `update`
- `ProductRetriever` n'a besoin que des méthodes `get_by_id` et `get_all`

Ainsi, l'interface `IProductRepository` peut être considérée comme "fat", et constituer une violation du principe ISP de Ségrégation des Interfaces.
Nous pouvons donc la diviser en interfaces plus petites et plus spécifiques :

- `IProductReader` (avec `get_by_id` et `get_all`)
- `IProductWriter`

Enfin, en ce qui concerne le principe de Substitution de Liskov LSP, nous n'avons pas introduit de hiérarchies de classes (différents types de validation de produits ou de types de produits). La seule hiérarchie introduite est celle de l'implémentation de l'interface `IProductRepository` par `ProductRepository`, et elle respecte bien le LSP.

## Étape 5 : Implémentation d'une Nouvelle Fonctionnalité

L'étape finale de ce TP est l'implémentation d'une fonctionnalité de recherche par catégorie.
Voici les étapes à suivre pour réaliser cette implémentation :

- Ajout d'une interface de recherche `find_by_category` dans `IProductReader` :

```python
@abstractmethod
class IProductReader(ABC):
   # ... #
   def get_by_category(self, category: str) -> List[Product]:
      pass
```

- Mettre à jour l'implémentation du `ProductRepository` avec `find_by_category` :

```python
class ProductRepository(IProductRepository):
   # ... #
   def get_by_category(self, category: str) -> List[Product]:
     return [p for p in self._products.values() if p.category == category]
```

- Création du service de recherche par catégorie `product_searcher.py` :

```python
class ProductSearcher:
 def __init__(self, reader: IProductReader):
     self.reader = reader

 def find_by_category(self, category: str) -> List[Product]:
     return self.reader.get_by_category(category)
```

La nouvelle fonctionnalité est bien ajoutée, et respecte bien les principes SOLID :

- **SRP :** La nouvelle fonctionnalité est bien séparée dans une classe dédiée `ProductSearcher`.
- **OCP :** La nouvelle fonctionnalité a été ajoutée en étendant une interface existante `IProductReader` sans modifier les classes des services existantes (comme `ProductCreator` ou `ProductDeleter`).
- **LSP :** Le `ProductRepository` respecte toujours le contrat de hiérarchie des classes.
- **ISP :** La nouvelle méthode `get_by_category` est ajoutée à l'interface de "lecture" `IProductReader` afin de garder une certaine logique à la méthode, sans la rendre trop "fat".
- **DIP :** La nouvelle fonctionnalité `ProductSearcher` dépend bien de l'abstraction `IProductReader`et non d'une implémentation directe de `ProductRepository`.
