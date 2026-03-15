from product import PhysicalProduct, DigitalProduct


class ProductFactory:
    """
    Factory Pattern — creates Product objects without exposing
    construction details to the rest of the application.

    Usage:
        p = ProductFactory.create("physical", product_id="P1", name="Mug",
                                   price=9.99, stock=50, weight_kg=0.4)
        d = ProductFactory.create("digital", product_id="D1", name="eBook",
                                   price=4.99, stock=999, download_url="http://…")
    """

    @staticmethod
    def create_physical(product_id: str, name: str, price: float,
                        stock: int, weight_kg: float) -> PhysicalProduct:
        return PhysicalProduct(product_id, name, price, stock, weight_kg)

    @staticmethod
    def create_digital(product_id: str, name: str, price: float,
                       stock: int, download_url: str) -> DigitalProduct:
        return DigitalProduct(product_id, name, price, stock, download_url)

    @staticmethod
    def create(product_type: str, **kwargs):
        """Generic factory method — dispatches by product_type string."""
        pt = product_type.lower()
        if pt == "physical":
            return ProductFactory.create_physical(**kwargs)
        elif pt == "digital":
            return ProductFactory.create_digital(**kwargs)
        else:
            raise ValueError(f"Unknown product type: '{product_type}'. Use 'physical' or 'digital'.")
