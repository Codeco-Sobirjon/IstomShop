import datetime
import json
import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse
import os
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db import transaction

from shop.models import (
    Product,
    OurPartner,
    Service,
    Consultant,
    Banner, ProductImage, SubCategory, MainCategories, ProductCard,
)
from shop.serializer.utils import Util


class OurPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurPartner
        fields = [
            "id",
            "name",
            "image",
        ]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "description",
            "image",
        ]


class ConsultantSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Consultant
        fields = [
            "id",
            "name",
            "phone",
            "description",
        ]

    def create(self, validated_data):
        create = Consultant.objects.create(**validated_data)
        return create


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "product",
            "image",
        ]


class ProductListSerializer(serializers.ModelSerializer):
    images_set = serializers.JSONField(write_only=True, required=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "quantity",
            "price_type",
            'vendor_code',
            "image",  # Main image field
            "sub_category",
            "characteristics",
            "advantages",
            "manufactured_city",
            "firm",
            "images_set",  # Field to handle image list from the request
            "created_at",
        ]

    def create(self, validated_data):
        # Pop the 'images_set' data (defaulting to an empty list if not provided)
        images_set = validated_data.pop('images_set', [])
        print(f"Images: {images_set}")

        # Get the sub_category ID
        category_id = validated_data.get('sub_category')

        # Create the product
        product = Product.objects.create(**validated_data)

        # Create ProductImage instances for each image in the images_set
        for image_url in images_set:
            print(f"Processing image: {image_url}")
            try:
                # Download the image
                response = requests.get(image_url)
                response.raise_for_status()  # Raise an error if the request failed

                # Parse the image filename from the URL
                parsed_url = urlparse(image_url)
                image_name = os.path.basename(parsed_url.path)

                # Save the image to the ProductImage model
                product_image = ProductImage(
                    product=product,
                )
                product_image.image.save(image_name, ContentFile(response.content))
                product_image.save()

            except requests.exceptions.RequestException as e:
                print(f"Failed to download image from {image_url}: {str(e)}")

        return product


class ProductSerializer(serializers.ModelSerializer):
    images_set = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "quantity",
            "price_type",
            'vendor_code',
            "image",
            "category",
            "characteristics",
            "advantages",
            "manufactured_city",
            "firm",
            "images_set",
            "created_at",
        ]

    def get_images_set(self, obj):
        images = ProductImage.objects.filter(product=obj.id)
        return ProductImageSerializer(images, many=True).data

    def get_category(self, obj):
        # Initialize the list to hold category data
        category_data = []

        if obj.sub_category:
            main_category = obj.sub_category.main_categories
            main_category_data = {
                'main_category_id': main_category.id,
                'main_category_name': main_category.name,
                'sub_category': []
            }
            main_category_data['sub_category'].append({
                'sub_category_id': obj.sub_category.id,
                'sub_category_name': obj.sub_category.name
            })
            category_data.append(main_category_data)

        return category_data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if 'images_set' in representation and isinstance(representation['images_set'], list):
            for item in representation['images_set']:
                if 'image' in item and item['image']:
                    item['image'] = request.build_absolute_uri(item['image']) if request else item['image']
        return representation


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = [
            "id",
            "header",
            'title',
            "description",
            'discount',
            'price',
            "image",
        ]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory  # Assuming the model is named SubCategory
        fields = ['id', 'name']


class MainCategoryListSerializer(serializers.ModelSerializer):
    sub_category = serializers.JSONField(write_only=True)

    class Meta:
        model = MainCategories
        fields = [
            'id',
            'name',
            'sub_category'
        ]

    def create(self, validated_data):
        sub_categories_data = validated_data.pop('sub_category')
        print(sub_categories_data)
        main_category = MainCategories.objects.create(**validated_data)

        for sub_category_data in sub_categories_data:
            SubCategory.objects.create(
                name=sub_category_data['title'],
                main_categories=main_category
            )
        return main_category


class MainCategoriesSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()

    class Meta:
        model = MainCategories
        fields = [
            'id',
            'name',
            'sub_category'
        ]

    def get_sub_category(self, obj):
        # Assuming a ForeignKey or OneToMany relationship from MainCategories to SubCategory
        sub_categories = SubCategory.objects.filter(main_categories=obj)
        return SubCategorySerializer(sub_categories, many=True).data


class ProductCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCard
        fields = [
            "id",
            "product",
            "quantity",
            "price_type",
            'full_name',
            'email',
            'phone',
            "created_at",
        ]


class ProductCardCreateSerializer(serializers.ModelSerializer):
    product_data = serializers.JSONField(write_only=True)
    total_price = serializers.IntegerField(write_only=True)
    class Meta:
        model = ProductCard
        fields = [
            "id",
            "product",
            "quantity",
            "price_type",
            "total_price",
            'full_name',
            'email',
            'phone',
            "created_at",
            "product_data"
        ]

    def create(self, validated_data):
        product_data = validated_data.pop('product_data')
        for product in product_data:
            try:
                get_product = Product.objects.get(id=product['product'])
            except ObjectDoesNotExist:
                raise serializers.ValidationError({'msg': "Product not found"})
            create = ProductCard.objects.create(product=get_product, quantity=product['quantity'], total_price=int(product['quantity']) * int(get_product.price), price_type=get_product.price_type, full_name=validated_data['full_name'], email=validated_data['email'], phone=validated_data['phone'])

        email_body = (f"Здравствуйте {create.full_name},\nВаш номер телефона: {create.phone}\n"
                      f"Дата: {create.created_at}\n"
                      f"Список покупок\n"
                      f"{self.format_data(product_data)}\n"
                      f"Итоговая цена: {validated_data['total_price']}\n"
                      f"Благодарим Вас за покупку нашей продукции \n"
                      f"IstomShop"
                      )
        email_data = {
            "email_body": email_body,
            "to_email": validated_data['email'],
            "email_subject": "Verify your email",
        }
        Util.send(email_data)
        return create

    def format_data(self, product_data):
        product_ids = [item['product'] for item in product_data]
        products = Product.objects.filter(id__in=product_ids)
        product_id_to_name = {product.id: [product.name, product.price] for product in products}

        # Format the product_data for the email body
        purchases_list = []
        for item in product_data:
            product_name = product_id_to_name.get(item['product'], "Unknown Product")
            quantity = item.get('quantity', 0)
            purchases_list.append(f"Наименование товара: {product_name[0]}: {quantity} * {product_name[1]} = {int(quantity) * int(product_name[1])}")

        # Join the formatted strings into a single string for the email body
        purchases_str = "\n".join(purchases_list)
        return purchases_str
