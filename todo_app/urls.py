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
    path('create/', views.create_redirect_to_today_list, name="create"),
    path('delete/<todo_id>',views.delete,name="delete"),
    path('yes_finish/<todo_id>',views.yes_finish,name="yes_finish"),
    path('no_finish/<todo_id>',views.no_finish,name="no_finish"),
    path('update/<todo_id>',views.update,name="update"),
    path('description/<int:id>/', views.description, name='description'),
    path('category/<int:category_id>/', views.category_view, name='category_view'),
    path('add-category/', views.add_category, name='add_category'),
    path('category/<int:category_id>/add/', views.add_todo_to_category, name='add_todo_to_category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('category/<int:parent_id>/add-category/', views.add_category, name='add_subcategory'),
    path('category/<int:Category_id>/update/', views.update_cat, name='update_cat'),
    path('daily-list/create/', views.create_daily_list, name='create_daily_list'),
    path('daily-list/<int:list_id>/', views.daily_list_detail, name='daily_list_detail'),
    path('add_todo_item/<int:todo_id>/', views.add_todo_item, name='add_todo_item'),
    path('subtask/<int:item_id>/update/', views.update_subtask, name='update_subtask'),
    path('subtask/<int:item_id>/delete/', views.delete_subtask, name='delete_subtask'),
    path('delete_subtask/<int:item_id>/', views.delete_subtask, name='delete_subtask'),
    path('user-info/', views.user_info, name='user_info'),
    path("accounts/", include("accounts.urls")),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', include(router.urls)),
    path("toggle_subtask_done/<int:item_id>/", views.toggle_subtask_done, name="toggle_subtask_done"),
    path("toggle_finish_status/<int:todo_id>/", views.toggle_finish_status, name="toggle_finish_status"),
    path('toggle_subtask/<int:item_id>/', views.toggle_subtask_done, name='toggle_subtask'),


    
    
]




