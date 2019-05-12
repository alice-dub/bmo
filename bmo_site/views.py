from django.http import HttpResponse
from django.template import loader

#def search(request):
#    template = loader.get_template('search.html')
#    print(request)
#    requete = request.POST['search']
#    #if requete:
#    #	Resultat = ['Resultat1', 'Resultat2', 'Resultat3']
#    context = {'Requete' : 'Resultat1', 'resultat': ''}  
#    return HttpResponse(template.render(context, request))

def search(request):
    template = loader.get_template('search.html')
    context={}
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            #lookups= Q(title__icontains=query) | Q(content__icontains=query)

            results= ["Resultat1", "Resultat2"]

            context={'results': results,
                     'submitbutton': submitbutton}

            return HttpResponse(template.render(context, request))

        else:
            return HttpResponse(template.render(context, request))
    else:
        return HttpResponse(template.render(context, request))
