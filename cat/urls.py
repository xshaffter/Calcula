from django.urls import path, include
from cat.views.model import urls as model_urls

url_patterns = [
    path('', include(model_urls)),
]
