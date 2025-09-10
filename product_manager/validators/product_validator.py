from product_manager.models.product_model import Product

class ProductValidator:
    def validate(self, name: str, price: float):
        if not name or not price or price <= 0:
            raise ValueError("Nom et prix sont requis, et le prix doit être positif.")