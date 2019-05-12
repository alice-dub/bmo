from django.http import HttpResponse
from django.template import loader
from django.db import connection

def get_pdfs(query):
    with connection.cursor() as cursor:
       cursor.execute("""SELECT url FROM search_index
                      WHERE document @@ phraseto_tsquery('fr', %s)
                      ORDER BY ts_rank(document, phraseto_tsquery('fr', %s))
                      DESC""",
                      [query, query])
       rows = cursor.fetchall()

    return [r[0] for r in rows]

def search(request):
    template = loader.get_template('search.html')
    context={}
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            results = get_pdfs(query)

            context={'results': results,
                     'submitbutton': submitbutton}
    return HttpResponse(template.render(context, request))
