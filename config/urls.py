from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import CartView, CreateOrderView, OrderListView, ProductViewSet, RegisterView
from core.views import AddToCartView, LoginView, CategoryViewSet, UpdateCartItemView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')

admin.site.site_header = "Администрация Mini-Ozon"
admin.site.site_title = "Админка Mini-Ozon"
admin.site.index_title = "Добро пожаловать в Администрацию Mini-Ozon"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('api/cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('api/cart/item/<int:pk>/update/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('api/cart/', CartView.as_view(), name='cart-detail'),
    path('api/orders/create/', CreateOrderView.as_view()),
    path('api/orders/history/', OrderListView.as_view(), name='order-history'),
]
