from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^submit-score$', views.submit_score, name='submit-score'),
	url(r'^get-top-scores$', views.get_top_scores, name='get-top-scores')
]
