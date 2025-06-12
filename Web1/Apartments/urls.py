from django.urls import path, include
from . import views

urlpatterns = [

    path('login/', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    path('SellerList/', include([
        path('', views.SellerList, name='SellerList'),
        path('Update/<int:apartment_id>', views.UpdateApartment, name='Update'),
        path('UpdateBuy/<int:apartment_id>', views.UpdateBuy, name='UpdateBuy'),
        path('Add/', views.AddApartment, name='Add'),
        path('Delete/<int:apartment_id>/', views.DeleteApartment, name='Delete'),
    ])),
    path('CustomerList/', include([
        path('', views.CustomerList, name='CustomerList'),
        path('Request/<int:apartment_id>/', views.create_request, name='Request'),
    ])),
    path('', views.Home, name='home'),
    path('ShowRequest/<int:apartment_id>/', views.show, name='ShowRequest'),
    path('logout/', views.logout_and_clear_session, name='logout'),
]
