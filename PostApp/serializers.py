from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from .models import Product, Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]

    def create(self, validated_data):
        try:
            return Category.objects.get(name=validated_data.get("name"))
        except:
            return super().create(validated_data)


class ProductSerializer(ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        cat_name = validated_data.pop("category")
        category = CategorySerializer(data=cat_name)
        if category.is_valid():
            cat = category.save()
            validated_data.update({"category": cat})
            return self.Meta.model.objects.create(**validated_data)
        else:
            print(category.errors)
            return Response(category.errors)

    def update(self, instance, validated_data):
        cat_name = validated_data.pop("category")
        category = CategorySerializer(data=cat_name)
        if category.is_valid():
            cat = category.save()
            validated_data.update({"category": cat})
            product = self.Meta.model.objects.filter(pk=instance.pk)
            product.name = validated_data.get("name")
            return product
        else:
            return Response(category.errors)
        
