from django.http import HttpResponse
from django.template import loader

def search(request):
    template = loader.get_template('search.html')
    context = {}
    return HttpResponse(template.render(context, request))

