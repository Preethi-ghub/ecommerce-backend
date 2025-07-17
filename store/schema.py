import graphene
from graphene_django.types import DjangoObjectType
from .models import Product

# Define the GraphQL type for Product
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"

    inStock = graphene.Boolean(source='in_stock') 

# Define the Query
class Query(graphene.ObjectType):
    products = graphene.List(
        ProductType,
        category=graphene.String(required=False),
        in_stock=graphene.Boolean(required=False)
    )

    def resolve_products(self, info, category=None, in_stock=None):
        products = Product.objects.all()
        if category:
            products = products.filter(category=category)
        if in_stock is not None:
            products = products.filter(inStock=in_stock)
        return products

schema = graphene.Schema(query=Query)

