from notecard.notecards.models import *
from django.db.models import  Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response

# If no query is entered, will bring you to blank search screen. Otherwise will pull results from keyword, and results from content and display in search.html
@login_required(login_url='/auth/login/')
def search(request):
    query = request.GET.get('q')
    results = Notecard.objects.filter(section__semester__user=request.user)
    if query:
        results = results.filter(Q(notecard_body__icontains=query)|Q(notecard_name__icontains=query))
    paginator = Paginator(results, 5)
   
    try:
        page = int(request.GET.get('page', 1))
        page = max(min(page, paginator.num_pages), 1)
    except ValueError:
        page = 1
   
    notecard_list = paginator.page(page)
    context = RequestContext(request)
    return render_to_response('notecards/search.html', {"results": results, "notecard_list": notecard_list,}, context_instance=context)