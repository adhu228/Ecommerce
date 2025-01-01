from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MypasswordResetForm, MypasswordChangeForm, MySetPasswordForm

urlpatterns = [
    path('', views.home, name='home'),
    path("Category/<slug:val>", views.CategoryViews.as_view(), name="Category"),
    path("product-detail/<int:pk>", views.ProductDetails.as_view(), name="product-detail"),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.ProfileView.as_view(), name='Profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.Orders, name='orders'),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    # path('removecart/',views.remove_cart),
     path('remove-cart/', views.remove_cart, name='remove_cart'),
    path('payment-success/', views.payment_success, name='payment_success'),

    path('pluswishlist/',views.plus_wishlist),
    path('minuswishlist/<int:product_id>/', views.minus_wishlist, name='minuswishlist'),  
    path('search/',views.search,name='search'),
    path('wishlist/', views.wishlist_view, name='wishlist'),


    # Login & Registration
    path('registration/', views.CustomerRegistrationView.as_view(), name='CustomerRegistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    # Password Management
    path('Passwordchange/', auth_view.PasswordChangeView.as_view(
        template_name='app/Changepassword.html',
        form_class=MypasswordChangeForm,
        success_url="/passwordchangedone"), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(
        template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('password_reset/', auth_view.PasswordResetView.as_view(
        template_name='app/password_reset.html',
        form_class=MypasswordResetForm), name='password-reset'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(
        template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html',
        form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(
        template_name='app/password_reset_complete.html'), name='password_reset_complete'),
]
