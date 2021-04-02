from rest_framework.routers import SimpleRouter

from training.core.views import PersonViewSet, UserViewSet

router = SimpleRouter()
router.register("user", UserViewSet, basename="user")
router.register("person", PersonViewSet, basename="person")
