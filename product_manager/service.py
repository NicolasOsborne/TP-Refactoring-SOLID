from product_manager.models import Product
from product_manager.repository import ProductRepository

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def create_product(self, name: str, description: str, price: float, category: str) -> Product:
        if not name or not price or price <= 0:
            raise ValueError("Nom et prix sont requis, et le prix doit être positif.")
        product = Product(name=name, description=description, price=price, category=category)
        return self.repository.add(product)

    def get_product(self, product_id: int) -> Optional[Product]:
        return self.repository.get_by_id(product_id)

    def get_all_products(self) -> List[Product]:
        return self.repository.get_all()

    def update_product(self, product_id: int, name: str, description: str, price: float, category: str) -> Product:
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ValueError("Produit non trouvé.")
        if not name or not price or price <= 0:
            raise ValueError("Nom et prix sont requis, et le prix doit être positif.")
        
        product.name = name
        product.description = description
        product.price = price
        product.category = category
        self.repository.update(product)
        return product

    def delete_product(self, product_id: int) -> bool:
        return self.repository.delete(product_id)