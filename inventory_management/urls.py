from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),  # Include the inventory app URLs
    path('', RedirectView.as_view(url='/inventory/login/', permanent=True)),  # Redirect root URL to login page
]
