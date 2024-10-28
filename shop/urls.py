from django.urls import path
from shop.views.views import BannerViews,MainCategoriesDetailsView, ProductViews, ServiceViews, OurPartnerViews, ConsultantViews, ProductDetailView,CategoriesView, CategoryDetailsView, ProductCardCreateView

urlpatterns = [
    path('/banner', BannerViews.as_view(), name='banner'),
    path('/product/', ProductViews.as_view(), name='product'),
    path('/product/<int:pk>', ProductDetailView.as_view(), name='product'),
    path('/service', ServiceViews.as_view(), name='service'),
    path('/our_partner', OurPartnerViews.as_view(), name='our_partner'),
    path('/consultation', ConsultantViews.as_view(), name='consultation'),
    path('/categories', CategoriesView.as_view()),
    path('/category_product/<int:pk>/', CategoryDetailsView.as_view()),
    path('/main/categories/products/<int:pk>/', MainCategoriesDetailsView.as_view()),
    path("/card/", ProductCardCreateView.as_view(), name="card")
]
