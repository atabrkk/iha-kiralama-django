from django.urls import path
from . import views

urlpatterns = [

    path("add/", views.add_uav, name="add_uav"),
    path("search/", views.search, name='search'),
    path("search_reservations/", views.search_reservations, name='search_reservations'),
    path("all-uavs/", views.get_all_uav, name='all-uavs'),
    path("category/<slug:category_slug>/", views.uavs_by_category, name='uavs_by_category'),
    path("uav_list_filtered/", views.uav_list_filtered, name='uav_list_filtered'),
    path("reservations_filtered/", views.reservations_filtered, name='reservations_filtered'),
    path("all-uavs/uav/<slug:slug>/", views.get_uav, name='get_uav'),
    path("all-uavs/edit/<slug:slug>/", views.edit_uav, name='edit_uav'),
    path("all-uavs/delete/<slug:slug>/", views.delete_uav, name='delete_uav'),
    path("create_rental/<slug:slug>/", views.create_rental, name='create_rental'),
    path("user-reservations/", views.user_reservations, name='user_reservations'),
    path("user-reservations/edit_user_uav/<int:pk>/", views.edit_user_uav, name='edit_user_uav'),
    path("user-reservations/delete_user_uav/<int:pk>/", views.delete_user_uav, name='delete_user_uav'),

    # path("search/", views.search, name='search'),
    # path("category/<slug:category_slug>/", views.posts_by_category, name='posts_by_category'),
    # path("<slug:slug>/", views.blog, name='blog'),

]
