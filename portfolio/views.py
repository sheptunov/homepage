from django.shortcuts import HttpResponse, render_to_response, RequestContext, get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from forms import FeedbackForm
from models import Message, Project, Entity

def index(request):
    form = FeedbackForm()
    debug = []
    projects = get_list_or_404(Project)
    for item in projects:
        item.image = item.get_images()[0]
        debug.append(item.get_images()[0])
    context = {'form': form, 'projects': projects, "debug": debug }
    # Send message
    if request.method == "POST":
        form = FeedbackForm(request.POST or None)
        context['form'] = form
        if form.is_valid():
            form.save()
            return HttpResponse("HTTP 200 OK")
        else:
            return HttpResponse("WOOPS %s" % (form.data))
    return render_to_response('portfolio/index.html', context, context_instance=RequestContext(request))

def get_project(request, project_id=1):
    if request.method == "GET":
        pass
    project = get_object_or_404(Project, id=project_id)
    if "/project" in request.get_full_path():
        menu = {"active": "projects"}
    context = {"project": project, "menu": menu}
    return render_to_response('portfolio/block-project-detail.html', context, context_instance=RequestContext(request))