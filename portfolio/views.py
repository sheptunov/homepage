from django.shortcuts import HttpResponse, render_to_response, render, RequestContext, get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from portfolio.forms import FeedbackForm
from portfolio.models import Message, Project, Image, Email
from django.core.mail import send_mail





def index(request):
    '''
    Index page.
    Also that view serve feedback(message) form submission, if http request type is POST(request.method == POST)
    '''
    form = FeedbackForm()
    projects = get_list_or_404(Project)
    for item in projects:
        item.image = item.get_images()[0]
    # Show hello for first time visit 
    request.session['show_hello'] = False
    show_hello = request.session.get('show_hello', True)
    # debug
    context = {'form': form, 'projects': projects, "show_hello": True} # show_hello }
    # Send message
    if request.method == "POST":
        form = FeedbackForm(request.POST or None)
        context['form'] = form
        if form.is_valid():
            # Save form into new Message object
            form.save()
            # Send email
            email = Email()
            email_subject = ""
            email_body = ""
            email_address = ""
            Email(email_subject, 'Here is the message.', 'from@example.com',
            ['to@example.com'], fail_silently=False)
            return HttpResponse("HTTP 200 OK")
        else:
            return HttpResponse("HTTP 404")
    return render_to_response('portfolio/index.html', context, context_instance=RequestContext(request))

def get_project(request, project_slug=None, project_mode=None):
    """
    Detail project page
    """
    project = get_object_or_404(Project, slug=project_slug)
    if project_mode is None:
        project = get_object_or_404(Project, slug=project_slug)
        menu = {"active": "projects"}
        context = {"project": project, "menu": menu}
        return render_to_response('portfolio/block-project-detail.html', context, context_instance=RequestContext(request))
    else:
        context = {"project": project}
        return render_to_response("%s/index.html" % project.slug, context, context_instance=RequestContext(request))
