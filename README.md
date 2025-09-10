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
