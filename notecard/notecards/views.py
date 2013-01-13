from django.http import HttpResponseRedirect, Http404
from notecard.notecards.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.cache import cache
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
# 60 Minute cache time
cache_time = 1800

@login_required(login_url='/auth/login/')
def semester_list(request):
    # Find all of user's semesters or 404
    cache_key = str(request.user) + 'users_semester_list_cache_key'
    semester = cache.get(cache_key)
    if not semester:
        semester = Semester.objects.filter(user=request.user)
        cache.set(cache_key, semester, cache_time)

    ## paginate each semester
    paginator = Paginator(semester, 6)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        semester_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        semester_list = paginator.page(paginator.num_pages)

    context = RequestContext(request)
    return render_to_response('notecards/semester_list.html', {"semester_list": semester_list, "paginator": paginator,}, context_instance=context)

@login_required(login_url='/auth/login/')
def section_list(request, semester_id):
    # Get chosen semester
    try:
        cache_key = str(semester_id) + 'single_semester_cache_key'
        semester = cache.get(cache_key)
        if not semester:
            semester = Semester.objects.get(id__iexact=semester_id)
            cache.set(cache_key, semester, cache_time)
    except Semester.DoesNotExist:
        raise Http404

    # get all sections related to the semester owned by the user
    cache_key_2 = str(semester_id) + 'users_section_list_cache_key'
    section = cache.get(cache_key_2)
    if not section:
        section = Section.objects.filter(semester__id=semester_id)
        section = section.filter(semester__user=request.user)
        cache.set(cache_key_2, section, cache_time)

    # pagination
    paginator = Paginator(section, 6)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        section_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        section_list = paginator.page(paginator.num_pages)

    # check if user owns the related semester - if not, returns to semester_list
    if semester.user == request.user:
        context = RequestContext(request)
        return render_to_response('notecards/section_list.html', {"section_list": section_list, "semester": semester, "paginator": paginator,}, context_instance=context)
    else:
        url = reverse('semester_list')
        return HttpResponseRedirect(url)

@login_required(login_url='/auth/login/')
def notecard_list(request, section_id):
    # Look up the section or raise 404
    try:
        cache_key = str(section_id) + 'single_section_cache_key'
        section = cache.get(cache_key)
        if not section:
            section = Section.objects.get(id__iexact = section_id)
            cache.set(cache_key, section, cache_time)
    except Section.DoesNotExist:
        raise Http404

    semester_id = section.semester.id
    cache_key_2 = str(semester_id) + 'single_semester_cache_key'
    semester = cache.get(cache_key_2)
    if not semester:
        # create semester variable to test if owned by user
        semester = Semester.objects.get(section__id__iexact = section_id)
        cache.set(cache_key_2, semester, cache_time)

    cache_key_3 = str(section_id) + 'users_notecard_list_cache_key'
    notecard = cache.get(cache_key_3)
    if not notecard:
        # get all notecards related to the section of the semester owned by the user
        notecard = Notecard.objects.filter(section__id=section_id)
        notecard = notecard.filter(section__semester__user=request.user)
        cache.set(cache_key_3, notecard, cache_time)

    # pagination
    paginator = Paginator(notecard, 6)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        notecard_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        notecard_list = paginator.page(paginator.num_pages)

    # check if user owns the related semester - if not, returns to semester_list
    if semester.user == request.user:
        context = RequestContext(request)
        return render_to_response('notecards/notecard_list.html', {"section": section, "notecard_list": notecard_list, "paginator": paginator,}, context_instance=context)
    else:
        url = reverse('semester_list')
        return HttpResponseRedirect(url)

@login_required(login_url='/auth/login/')
def notecard_detail(request, notecard_id):
    # Look up the username or raise 404
    try:
        cache_key = str(notecard_id) + 'single_notecard_cache_key'
        notecard = cache.get(cache_key)
        if not notecard:
            notecard = Notecard.objects.get(id__iexact=notecard_id)
            cache.set(cache_key, notecard, cache_time)
    except Notecard.DoesNotExist:
        raise Http404

    semester_id = notecard.section.semester.id
    cache_key_2 = str(semester_id) + 'single_semester_cache_key'
    semester = cache.get(cache_key_2)
    if not semester:
        semester = Semester.objects.get(section__notecard__id__iexact = notecard_id)
        cache.set(cache_key_2, semester, cache_time)

    # check if user owns the related semester - if not, returns to semester_list
    if semester.user == request.user:
        context = RequestContext(request)
        return render_to_response('notecards/notecard_detail.html', {"notecard": notecard}, context_instance=context)
    else:
        url = reverse('semester_list')
        return HttpResponseRedirect(url)

@login_required(login_url='/auth/login/')
def new_semester(request):
    semester = Semester(user = request.user)

    if request.method == 'POST':
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            semester.semester_name = form.cleaned_data['semester_name']
            semester.save()
            cache_key = str(request.user) + 'users_semester_list_cache_key'
            cache.delete(cache_key)
            return HttpResponseRedirect('/')
    else:
        form = SemesterForm()
    initialData = {'form': form}
    csrfContext = RequestContext(request, initialData)
    return render_to_response('notecards/new_semester.html', csrfContext)

@login_required(login_url='/auth/login/')
def edit_semester(request, semester_id):
    cache_key = str(semester_id) + 'single_semester_cache_key'
    semester = cache.get(cache_key)
    if not semester:
        semester = get_object_or_404(Semester, pk=semester_id)
        cache.set(cache_key, semester, cache_time)
    vars = {}

    if semester.user != request.user:
        raise Http404

    if request.method == 'POST': #if the form has been submitted
        form = SemesterForm(request.POST, instance=semester) # a form bound to the POST data
        if form.is_valid(): #all validation rules pass
            # process the data in form.cleaned_data
            semester.semester_name = form.cleaned_data['semester_name']
            semester.save()
            cache_key_2 = str(request.user) + 'users_semester_list_cache_key'
            cache.delete_many([cache_key, cache_key_2])
            return HttpResponseRedirect('/')
    else:
        form = SemesterForm(initial={'semester_name': semester.semester_name})
        #Package up some variables to return
    vars['semester'] = semester
    vars['form'] = form
    context = RequestContext(request)
    return render_to_response('notecards/edit_semester.html', vars, context_instance=context)

@login_required(login_url='/auth/login/')
def new_section(request, semester_id):
    vars = {}
    semester = Semester.objects.get(id__iexact=semester_id)

    # check if semester user is logged in user
    if semester.user != request.user:
        raise Http404

    if request.method == 'POST': #if the form has been submitted
        form = SectionForm(request.POST) # a form bound to the POST data
        if form.is_valid(): #all validation rules pass
            # process the data in form.cleaned_data
            section_name = form.cleaned_data['section_name']
            section = Section(semester=semester, section_name=section_name)
            section.save()
            cache_key = str(semester_id) + 'users_section_list_cache_key'
            cache.delete(cache_key)
            url = reverse('section_list', kwargs={'semester_id': semester_id})
            return HttpResponseRedirect(url)
    else:
        form = SectionForm() # an unbound form
        #Package up some variables to return
    vars['semester'] = semester
    vars['form'] = form
    context = RequestContext(request)
    return render_to_response('notecards/new_section.html', vars, context_instance=context)

@login_required(login_url='/auth/login/')
def edit_section(request, section_id):
    vars = {}
    cache_key = str(section_id) + 'single_section_cache_key'
    section = cache.get(cache_key)
    if not section:
        section = get_object_or_404(Section, pk=section_id)
        cache.set(cache_key, section, cache_time)

    # check if section's user is logged in user
    if section.semester.user != request.user:
        raise Http404

    if request.method == 'POST': #if the form has been submitted
        form = SectionForm(request.POST, instance=section) # a form bound to the POST data
        if form.is_valid(): #all validation rules pass
            # process the data in form.cleaned_data
            section.section_name = form.cleaned_data['section_name']
            section.save()
            semester_id = section.semester.id
            cache_key_2 = str(semester_id) + 'users_section_list_cache_key'
            cache.delete_many([cache_key, cache_key_2])
            url = reverse('section_list', kwargs={'semester_id': section.semester.id})
            return HttpResponseRedirect(url)
    else:
        form = SectionForm(initial={'section_name': section.section_name}) # an unbound form
        #Package up some variables to return
    vars['section'] = section
    vars['form'] = form
    context = RequestContext(request)
    return render_to_response('notecards/edit_section.html', vars, context_instance=context)

@login_required(login_url='/auth/login/')
def new_notecard(request, section_id):
    vars = {}
    # Look up the game or raise 404
    try:
        section = Section.objects.get(id__iexact=section_id)
    except Section.DoesNotExist:
        raise Http404

    if section.semester.user != request.user:
        raise Http404

    if request.method == 'POST': #if the form has been submitted
        form = NotecardForm(request.POST) # a form bound to the POST data
        if form.is_valid(): #all validation rules pass
            # process the data in form.cleaned_data
            notecard_name = form.cleaned_data['notecard_name']
            notecard_body = form.cleaned_data['notecard_body']
            notecard = Notecard(section=section, notecard_name=notecard_name, notecard_body=notecard_body)
            notecard.save()
            # set and clear cache for the
            cache_key = str(section_id) + 'users_notecard_list_cache_key'
            cache.delete_many([cache_key, 'unknown_list_cache_key'])
            url = reverse('notecard_list', kwargs={'section_id': section_id})
            return HttpResponseRedirect(url)
    else:
        form = NotecardForm() # an unbound form
        #Package up some variables to return
    vars['section'] = section
    vars['form'] = form
    context = RequestContext(request)
    return render_to_response('notecards/new_notecard.html', vars, context_instance=context)

@login_required(login_url='/auth/login/')
def edit_notecard(request, notecard_id):
    vars = {}
    cache_key = str(notecard_id) + 'single_notecard_cache_key'
    notecard = cache.get(cache_key)
    if not notecard:
        notecard = get_object_or_404(Notecard, pk=notecard_id)
        cache.set(cache_key, notecard, cache_time)
        ## if notecard found, sets section_id for URL reverse after edit submission
    section_id = notecard.section.id
    if notecard.section.semester.user != request.user:
        raise Http404
    form = NotecardForm(request.POST, instance=notecard)
    if form.is_valid():
        cache_key_2 = str(section_id) + 'users_notecard_list_cache_key'
        if notecard.known:
            cache_key_3 = str(section_id) + 'known_list_cache_key'
        else:
            cache_key_3 = str(section_id) + 'unknown_list_cache_key'
        cache.delete_many([cache_key,cache_key_2,cache_key_3])
        if request.POST.get('delete'):
            notecard.delete()
            url = reverse('notecard_list', kwargs={'section_id': notecard.section_id})
            return HttpResponseRedirect(url)
        elif request.method == 'POST': #if the form has been submitted
            notecard.notecard_name = form.cleaned_data['notecard_name']
            notecard.notecard_body = form.cleaned_data['notecard_body']
            notecard.save()
            url = reverse('notecard_list', kwargs={'section_id': notecard.section_id})
            return HttpResponseRedirect(url)
    else:
        form = NotecardForm(initial={'notecard_name': notecard.notecard_name, 'notecard_body': notecard.notecard_body}) # an unbound form
        #Package up some variables to return
    vars['notecard'] = notecard
    vars['form'] = form
    context = RequestContext(request)
    return render_to_response('notecards/edit_notecard.html', vars, context_instance=context)

@login_required(login_url='/auth/login/')
def known_list(request, section_id):
    try:
        section = Section.objects.get(id__iexact = section_id)
    except Section.DoesNotExist:
        raise Http404
    cache_key = str(section_id) + 'known_list_cache_key'
    known_list = cache.get(cache_key)
    if not known_list:
        known_list = Notecard.objects.filter(known=1, section=section)
        known_list = known_list.filter(section__semester__user=request.user)
        cache.set(cache_key, known_list, cache_time)
    semester = Semester.objects.get(section__id__iexact = section_id)

    paginator = Paginator(known_list, 1)

    # check if known list is populated and user owns the related semester - if not, returns to notecard_list
    if known_list and semester.user == request.user:
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        try:
            known = paginator.page(page)
        except (EmptyPage, InvalidPage):
            known = paginator.page(paginator.num_pages)
        context = RequestContext(request)
        return render_to_response('notecards/known.html', {"known": known, "section": section, "paginator": paginator,}, context_instance=context)
    else:
        url = reverse('notecard_list', kwargs={'section_id': section_id})
        return HttpResponseRedirect(url)

@login_required(login_url='/auth/login/')
def unknown_list(request, section_id):
    try:
        section = Section.objects.get(id__iexact = section_id)
    except Section.DoesNotExist:
        raise Http404
    cache_key = str(section_id) + 'unknown_list_cache_key'
    unknown_list = cache.get(cache_key)
    if not unknown_list:
        unknown_list = Notecard.objects.filter(known=0, section=section)
        unknown_list = unknown_list.filter(section__semester__user=request.user)
        cache.set(cache_key, unknown_list, cache_time)
    semester = Semester.objects.get(section__id__iexact = section_id)

    paginator = Paginator(unknown_list, 1)

    # check if known list is populated and user owns the related semester - if not, returns to notecard_list
    if unknown_list and semester.user == request.user:
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            unknown = paginator.page(page)
        except (EmptyPage, InvalidPage):
            unknown = paginator.page(paginator.num_pages)
        context = RequestContext(request)
        return render_to_response('notecards/unknown.html', {"unknown": unknown, "section": section, "paginator": paginator,}, context_instance=context)
    else:
        url = reverse('notecard_list', kwargs={'section_id': section_id})
        return HttpResponseRedirect(url)

@login_required(login_url='/auth/login/')
@require_POST
def toggle_known(request, notecard_id):
    # grabs the notecard id of the notecard where known toggle was clicked and
    # toggles the value. Returns to the known/unknown list after removing that notecard
    notecard = Notecard.objects.get(pk=notecard_id)
    section_id = notecard.section.id
    cache_key = str(section_id) + 'unknown_list_cache_key'
    cache_key_2 = str(section_id) + 'known_list_cache_key'
    cache_key_3 = str(section_id) + 'users_notecard_list_cache_key'
    cache.delete_many([cache_key,cache_key_2,cache_key_3])
    notecard.known = not notecard.known
    notecard.save()
    return HttpResponseRedirect(request.POST['next'])