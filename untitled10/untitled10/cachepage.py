from django.views.decorators.cache import cache_page
from django.http import HttpResponse
@cache_page(60)
def cachetest(request):
    return HttpResponse("hello world!")