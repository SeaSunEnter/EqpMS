from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [

    # Asset Routes
    path('asset/', views.AssetAll.as_view(), name='asset_all'),
    path('asset/new/', views.AssetNew.as_view(), name='asset_new'),
    path('asset/<int:pk>/update/', views.AssetUpdate.as_view(), name='asset_update'),
    path('asset/<int:pk>/view/', views.AssetView.as_view(), name='asset_view'),

    # AssetCategory Routes
    path('assetcategory/', views.AssetCategoryAll.as_view(), name='ass_cat_all'),
    path('assetcategory/new/', views.AssetCategoryNew.as_view(), name='ass_cat_new'),
    path('assetcategory/<int:pk>/update/', views.AssetCategoryUpdate.as_view(), name='ass_cat_update'),

    # AssetUnit Routes
    path('assetunit/', views.AssetUnitAll.as_view(), name='ass_unt_all'),
    path('assetunit/new/', views.AssetUnitNew.as_view(), name='ass_unt_new'),
    path('assetunit/<int:pk>/update/', views.AssetUnitUpdate.as_view(), name='ass_unt_update'),


]
