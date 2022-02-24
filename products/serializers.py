from rest_framework import serializers

from products.models import Product, Discount, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('delete_timestamp','created','last_updated','deleted_at','is_deleted','is_active')
        # fields = '__all__'


class ProductSerializer2(serializers.Serializer):
    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.inventory = validated_data.get('inventory', instance.inventory)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.category = validated_data.get('category', instance.category)
        return instance

    name = serializers.CharField()
    price = serializers.IntegerField()
    description = serializers.CharField()
    image = serializers.FileField(required=False)
    inventory = serializers.IntegerField()
    slug = serializers.SlugField()
    brand = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    discount = serializers.PrimaryKeyRelatedField(queryset=Discount.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
