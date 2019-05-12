from django.http import HttpResponse
from django.template import loader
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

        if query is not None:
            results = get_pdfs(query)

            context={'results': results}
            paginator = Paginator(results, 15)
            page = request.GET.get('page', 1)
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
            # If page is not an integer, deliver first page.
                results = paginator.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                results = paginator.page(paginator.num_pages)
            context={'results': results,
                     'query':query}
    return HttpResponse(template.render(context, request))
