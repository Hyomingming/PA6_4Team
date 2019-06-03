from django.conf.urls import url

from .views import HomePageView, SearchResultsView

urlpatterns = [
    url('search/', SearchResultsView.as_view(), name='search_results'),
    url('', HomePageView.as_view(), name='home'),
]

