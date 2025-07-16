import graphene
from graphene_django.types import DjangoObjectType
from .models import Product, Cart, CartItem

# GraphQL Types
class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem

class CartType(DjangoObjectType):
    class Meta:
        model = Cart

# Queries
class Query(graphene.ObjectType):
    products = graphene.List(ProductType, category=graphene.String(), in_stock=graphene.Boolean())
    cart = graphene.Field(CartType)
    categories = graphene.List(graphene.String)

    def resolve_products(self, info, category=None, in_stock=None):
        products = Product.objects.all()
        if category:
            products = products.filter(category=category)
        if in_stock is not None:
            products = products.filter(in_stock=in_stock)
        return products

    def resolve_cart(self, info):
        cart, _ = Cart.objects.get_or_create(id=1)
        return cart

    def resolve_categories(self, info):
        return Product.objects.values_list('category', flat=True).distinct()

# Mutations
class AddToCart(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)

    cart = graphene.Field(CartType)

    def mutate(self, info, product_id):
        product = Product.objects.get(id=product_id)
        cart, _ = Cart.objects.get_or_create(id=1)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += 1
            item.save()
        return AddToCart(cart=cart)

class RemoveFromCart(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)

    cart = graphene.Field(CartType)

    def mutate(self, info, product_id):
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(id=1)
        CartItem.objects.filter(cart=cart, product=product).delete()
        return RemoveFromCart(cart=cart)

class Mutation(graphene.ObjectType):
    add_to_cart = AddToCart.Field()
    remove_from_cart = RemoveFromCart.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
