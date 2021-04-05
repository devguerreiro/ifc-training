from rest_framework.routers import SimpleRouter

from training.core.views import PersonViewSet, UserViewSet

# https://www.django-rest-framework.org/api-guide/routers/#simplerouter
router = SimpleRouter()

# /api/v1/user
router.register("user", UserViewSet, basename="user")
# /api/v1/person
router.register("person", PersonViewSet, basename="person")
