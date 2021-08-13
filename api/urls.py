from django.urls import path

from rest_framework import routers

from api import views

router = routers.SimpleRouter()
router.register("sentences", views.SentenceViewset)

urlpatterns = router.urls

urlpatterns += [
    path("words/<str:word_type>/<int:pk>/vote-to-remove/", views.vote_to_remove, name="vote-to-remove"),
    path("sentences/<int:pk>/mark-incorrect/", views.mark_sentence_incorrect,
         name="mark-incorrect"),
]
