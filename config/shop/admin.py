from django.contrib import admin
from config.shop.models import Product, OurPartner, Service, Consultant, Banner, MainCategories, SubCategory, ProductImage, \
    ProductCard
from import_export.admin import ImportExportModelAdmin


class MainCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('id', 'name',)
    list_filter = ('id', 'name',)


class SubCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name', 'main_categories')
    search_fields = ('id', 'name', 'main_categories')
    list_filter = ('id', 'name', 'main_categories')


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'quantity', 'price_type', 'image', 'sub_category', 'sub_category', 'characteristics', 'advantages', 'manufactured_city', 'firm', 'created_at')
    search_fields = ('name', 'description', 'price', 'quantity', 'price_type', 'image', 'sub_category', 'sub_category', 'characteristics', 'advantages', 'manufactured_city', 'firm', 'created_at')
    list_filter = ('name', 'description', 'price', 'quantity', 'price_type', 'image', 'sub_category', 'sub_category', 'characteristics', 'advantages', 'manufactured_city', 'firm', 'created_at')


class OurPartnerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'image')
    search_fields = ('name', 'image')
    list_filter = ('name', 'image')


class ProductImageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product', 'image')
    list_filter = ('product', 'image')


class ServiceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'description', 'image')
    search_fields = ('title', 'description', 'image')
    list_filter = ('title', 'description', 'image')


class ConsultantAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'phone', 'description')
    search_fields = ('name', 'phone', 'description')
    list_filter = ('name', 'phone', 'description')


class BannerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'description', 'image')
    search_fields = ('title', 'description', 'image')
    list_filter = ('title', 'description', 'image')


class ProductCardAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'total_price', 'quantity', 'price_type', 'email', 'created_at')
    search_fields = ('product', 'total_price', 'quantity', 'price_type', 'email', 'created_at')
    list_filter = ('product', 'total_price', 'quantity', 'price_type', 'email', 'created_at')


admin.site.register(Banner, BannerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OurPartner, OurPartnerAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Consultant, ConsultantAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(MainCategories, MainCategoryAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductCard, ProductCardAdmin)
