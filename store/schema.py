import graphene
from graphene_django.types import DjangoObjectType
from .models import Product
from .models import Cart, CartItem

class ProductType(DjangoObjectType):
    inStock = graphene.Boolean(source='in_stock')

    class Meta:
        model = Product
        fields = "__all__"
class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem
        fields = "__all__"

class CartType(DjangoObjectType):
    total = graphene.Float()
    cartitem_set = graphene.List(CartItemType)

    class Meta:
        model = Cart
        fields = "__all__"

    def resolve_total(self, info):
        return sum(item.product.price * item.quantity for item in self.cartitem_set.all())

    def resolve_cartitem_set(self, info):
        return self.cartitem_set.all()

class Query(graphene.ObjectType):
    products = graphene.List(
        ProductType,
        category=graphene.String(required=False), 
        inStock=graphene.Boolean(required=False)
    )
    cart = graphene.Field(CartType)  # <-- You missed this!
    cartitems = graphene.List(CartItemType)

    def resolve_products(self, info, category=None, inStock=None):
        products = Product.objects.all()

        if category:
            products = products.filter(category__iexact=category)

        if inStock is not None:
            products = products.filter(in_stock=inStock)  
        return products

    def resolve_cart(self, info):
        return Cart.objects.first()

    def resolve_cartitems(self, info):
        return CartItem.objects.all()


schema = graphene.Schema(query=Query)

