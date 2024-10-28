from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from shop.models import (
    Product,
    OurPartner,
    Service,
    Consultant,
    Banner, MainCategories, SubCategory, ProductCard,
)
from shop.serializer.serializer import (
    ProductSerializer,
    OurPartnerSerializer,
    ServiceSerializer,
    ConsultantSerializer, MainCategoriesSerializer,
    ProductCardCreateSerializer, MainCategoryListSerializer, ProductListSerializer
)
from shop.services.pagination import StandardResultsSetPagination
from shop.services.paginator import PaginationMethod


class OurPartnerViews(APIView):

    def get(self, request):
        our_partner = OurPartner.objects.all().order_by('-id')
        serializer = OurPartnerSerializer(our_partner, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceViews(APIView):

    def get(self, request):
        service = Service.objects.all().order_by('-id')
        serializer = ServiceSerializer(service, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductViews(APIView, PaginationMethod):
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    def post(self, request):
        serializer = ProductListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        product = Product.objects.all().order_by('-id')
        product = self.filter_by_name(product, request)
        product = self.filter_by_popular_product(product, request)
        product = self.filter_rating_product(product, request)
        product = self.filter_by_price(product, request)
        serializer = super().page(product, ProductSerializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def filter_by_name(self, product, request):
        name = request.query_params.get('name', '')
        if name:
            product = product.filter(name__icontains=name)
        return product

    def filter_by_popular_product(self, products_queryset, request):
        is_popular = request.query_params.get('is_popular', None)
        products_queryset = is_popular and products_queryset.filter(
            id__in=ProductCard.objects
            .values('product_id')
            .annotate(most_sold_product=Sum('quantity'))
            .order_by('-most_sold_product')
            .values_list('product_id', flat=True)
        ) or products_queryset
        return products_queryset

    def filter_rating_product(self, products_queryset, request):
        is_rating = request.query_params.get('is_rating', None)
        products_queryset = is_rating and products_queryset.filter(
            id__in=ProductCard.objects
            .values('product_id')
            .annotate(most_sold_product=Sum('quantity'))
            .order_by('-most_sold_product')
            .values_list('product_id', flat=True)
        ) or products_queryset
        return products_queryset

    def filter_by_price(self, products_queryset, request):
        is_max_min = request.query_params.get('is_max_min', '')
        products_queryset = is_max_min.isdigit() and int(is_max_min) == 1 and products_queryset.order_by('-price') or products_queryset.order_by('price')
        return products_queryset


class ProductDetailView(APIView):

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BannerViews(APIView):

    def get(self, request):
        banner = Banner.objects.all().order_by('-id')
        serializer = ProductSerializer(banner, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConsultantViews(APIView):

    def post(self, request):
        serializer = ConsultantSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CategoriesView(APIView):

    def post(self, request):
        serializer = MainCategoryListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': "Successfully added"}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = MainCategories.objects.all()
        serializers = MainCategoriesSerializer(queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class CategoryDetailsView(APIView, PaginationMethod):
    pagination_class = StandardResultsSetPagination

    def get(self, request, pk):
        queryset = get_object_or_404(SubCategory, id=pk)
        filtering_data = Product.objects.select_related('sub_category').filter(
            sub_category=queryset
        )
        serializer = super().page(filtering_data, ProductSerializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MainCategoriesDetailsView(APIView, PaginationMethod):
    pagination_class = StandardResultsSetPagination

    def get(self, request, pk):
        queryset = get_object_or_404(MainCategories, pk=pk)
        filtering_data = Product.objects.filter(
            sub_category__main_categories__id=queryset.id
        )
        serializer = super().page(filtering_data, ProductSerializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductCardCreateView(APIView):

    def post(self, request):
        serializer = ProductCardCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
