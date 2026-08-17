from abc import ABC, abstractmethod


class EcommerceProvider(ABC):
    """
    Base interface for all e-commerce providers.

    Every provider must return products using
    the same normalized dictionary structure.
    """

    name = "Unknown"

    @abstractmethod
    def get_products(
        self,
        categories=None,
        limit=20
    ):
        """
        Retrieve products from the e-commerce provider.
        """
        raise NotImplementedError