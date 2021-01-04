from django.urls import path

from rest_framework import routers

from api import views

router = routers.SimpleRouter()
router.register("sentences", views.SentenceViewset)

urlpatterns = router.urls
