from django.http import HttpResponse
from django.template import loader
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_pdfs_rank(query):
    with connection.cursor() as cursor:
       cursor.execute("""SELECT url, pub_date FROM search_index
                      JOIN list_pdf using(id)
                      WHERE document @@ phraseto_tsquery('fr', %s)
                      ORDER BY ts_rank(document, phraseto_tsquery('fr', %s))
                      DESC""",
                      [query, query])
       rows = cursor.fetchall()
    return [[r[0], r[1]] for r in rows]

def get_pdfs_date(query):
    with connection.cursor() as cursor:
       cursor.execute("""SELECT url, pub_date FROM search_index
                      JOIN list_pdf using(id)
                      WHERE document @@ phraseto_tsquery('fr', %s)
                      ORDER BY pub_date DESC""",
                      [query])
       rows = cursor.fetchall()
    return [[r[0], r[1]] for r in rows]

def search(request):
    template = loader.get_template('search.html')
    context={}
    sort = request.GET.get('sort')
    if request.method == 'GET':
        query= request.GET.get('q')
        sort= request.GET.get('sort')
        if query is not None:
            if sort == 'date':
                results = get_pdfs_date(query)
            elif sort == 'perti':
                results = get_pdfs_rank(query)
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
                     'sort': sort,
                     'query':query}
    return HttpResponse(template.render(context, request))
