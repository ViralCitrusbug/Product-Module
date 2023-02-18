from rest_framework import mixins, generics
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class ProductListView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def create(self, request, *args, **kwargs):
        data = {
            "name":request.POST.get("name"),
            "category":{"name":request.POST.get("category")},
            "price":request.POST.get("price"),
            "info":request.POST.get("info"),
            "is_active":request.POST.get("is_active"),
            "product_image":request.FILES.get("product_image"),
        }
        new_product = self.serializer_class(data=data)
        if new_product.is_valid():
            new_product.save()
            return Response(new_product.data)
        else:
            return Response(new_product.errors, status=400)
