import graphene
from graphene_django.types import DjangoObjectType
from .models import Product


class ProductType(DjangoObjectType):
    inStock = graphene.Boolean(source='in_stock')

    class Meta:
        model = Product
        fields = "__all__"

class Query(graphene.ObjectType):
    products = graphene.List(
        ProductType,
        category=graphene.String(required=False),
        inStock=graphene.Boolean(required=False)
    )

    def resolve_products(self, info, category=None, inStock=None):
        products = Product.objects.all()

        if category:
            products = products.filter(category__iexact=category)

        if inStock is not None:
            products = products.filter(in_stock=inStock)  
        return products


schema = graphene.Schema(query=Query)

