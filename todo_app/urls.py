from django.urls import path, include
from . import views
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .api import TodosViewSet
from rest_framework_simplejwt.views import ( TokenObtainPairView ,  TokenRefreshView, )


router = DefaultRouter()
router.register(r'todos', TodosViewSet , basename='todos')

urlpatterns = [
    path('',views.index,name="index"),
    path('todo/',views.todo,name="todo"),
    path('about/',views.about,name="about"),
    path('create/',views.create,name="create"),
    path('delete/<Todos_id>',views.delete,name="delete"),
    path('yes_finish/<Todos_id>',views.yes_finish,name="yes_finish"),
    path('no_finish/<Todos_id>',views.no_finish,name="no_finish"),
    path('update/<Todos_id>',views.update,name="update"),
    path('description/<int:id>/', views.description, name='description'),
    path('category/<int:category_id>/', views.category_view, name='category_view'),
    path('add-category/', views.add_category, name='add_category'),
    path('category/<int:category_id>/add/', views.add_todo_to_category, name='add_todo_to_category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('user-info/', views.user_info, name='user_info'),
    path("accounts/", include("accounts.urls")),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', include(router.urls)),
    path('category/<int:parent_id>/add-category/', views.add_category, name='add_subcategory'),
    path('category/<int:Category_id>/update/', views.update_cat, name='update_cat')

    
    
]




