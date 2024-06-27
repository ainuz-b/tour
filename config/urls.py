from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi 
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="dreamtrip",
        description="look closely",
        default_version="v1",
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('tours/', include('tours.urls')),
    path('cart/', include('cart.urls')),
    path('review/', include('review.urls')),
    path('docs/', schema_view.with_ui('swagger'))
]

