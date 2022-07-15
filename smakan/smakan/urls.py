from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('polls.urls')),
]

admin.site.site_header = "SMAKAN Administration"
admin.site.site_title = "By Dylan"
admin.site.index_title = "SMACC2's Makan App"