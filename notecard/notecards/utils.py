from django.core.paginator import Paginator, EmptyPage, InvalidPage

def paginate_me(request,object, pgs):

    paginator = Paginator(object, pgs)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        object_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        object_list = paginator.page(paginator.num_pages)

    return object_list, paginator