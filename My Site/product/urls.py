from django.urls import path

from . import views

app_name = "product"

urlpatterns = [
    path('',views.product_list,name="product_list"),
    path('filter/<str:order>',views.product_list,name="product_filter"),
    path('<int:id>',views.product_detail, name ="product_detail"),
    path('update/<int:id>',views.product_update, name ="product_update"),
    path('updatecomment/<int:c_id>/<int:p_id>',views.comment_update, name ="comment_update"),
    path("category/<slug:category>",views.Product_Category,name="category"),
    path("tag/<slug:tag>",views.Product_Tag,name="tag"),
    # path("search/",views.post_list,name="search"),
    path("Dashboard/",views.Dashboard,name="Dashboard"),
]