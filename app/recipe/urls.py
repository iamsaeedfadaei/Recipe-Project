from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views


router = DefaultRouter()  #default router is a django tool that automatically generate urls for our router!
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipe', views.RecipeViewSet)

app_name = 'recipe'  #for reverse url in tests


urlpatterns = [
    path('', include(router.urls)),
]


# from django.urls import path, include
# from rest_framework.routers import DefaultRouter

# from recipe import views


# router = DefaultRouter()
# router.register('tags', views.TagViewSet)

# app_name = 'recipe'

# urlpatterns = [
#     path('', include(router.urls))
# ]
