from rest_framework.routers import SimpleRouter
from training.core.views import UserViewSet


router = SimpleRouter()
router.register("user", UserViewSet, basename="user")
