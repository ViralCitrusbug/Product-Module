from rest_framework import mixins, generics
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

class ProductListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def list(self, request, *args, **kwargs):
        filter_data = {}
        if request.GET:
            for key, value in request.GET.items():
                filter_data[key] = value
            return Response(
                self.serializer_class(
                    self.queryset.filter(**filter_data), many=True
                ).data
            )
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = {
            "name": request.POST.get("name"),
            "category": {"name": request.POST.get("category")},
            "price": request.POST.get("price"),
            "info": request.POST.get("info"),
            "is_active": request.POST.get("is_active"),
            "product_image": request.FILES.get("product_image"),
        }
        new_product = self.serializer_class(data=data)
        if new_product.is_valid():
            new_product.save()
            return Response(new_product.data)
        else:
            return Response(new_product.errors, status=400)


class ProductDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def update(self, request, *args, **kwargs):
        try:
            data = {
                "name": request.POST.get("name"),
                "price": request.POST.get("price"),
                "info": request.POST.get("info"),
                "is_active": request.POST.get("is_active"),
                "product_image": request.FILES.get("product_image"),
            }
            new_product = Product.objects.filter(pk=self.kwargs.get("pk"))
            new_product.update(**data)
            return self.get(request, pk=self.kwargs.get("pk"))
        except Exception as e:
            print(e, "########################")
            Response("Something Went Wrong", status=400)

    def delete(self, request, pk):
        return self.destroy(request=request)

    def destroy(self, request, *args, **kwargs):
        product = Product.objects.filter(pk=self.kwargs.get("pk")).update(is_active=False)
        return self.get(request,self.kwargs.get("pk"))