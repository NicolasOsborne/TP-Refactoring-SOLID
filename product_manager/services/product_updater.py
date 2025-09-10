from typing import Optional
from product_manager.models.product_model import Product
from product_manager.validators.product_validator import ProductValidator
from product_manager.interfaces.product_repositories import IProductReader, IProductWriter

class ProductUpdater:
    def __init__(self, reader: IProductReader, writer: IProductWriter, validator: ProductValidator):
        self.reader = reader
        self.writer = writer
        self.validator = validator

    def update(self, product_id: int, name: str, description: str, price: float, category: str) -> Product:
        product = self.reader.get_by_id(product_id)
        if not product:
            raise ValueError("Produit non trouvé.")

        self.validator.validate(name, price)

        product.name = name
        product.description = description
        product.price = price
        product.category = category
        self.writer.update(product)
        return product