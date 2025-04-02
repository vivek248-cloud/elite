from django.shortcuts import render, redirect,get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import QuoteRequestForm
from .models import Project
from .models import AboutVideo
from .models import Review,AboutSection
from .models import UpcomingProject,GalleryImage
from django.http import HttpResponseServerError
from django.http import HttpResponse, Http404
import os
import mimetypes
from django.templatetags.static import static


def home(request):

    context = {'title': 'Welcome to Elite Dream Builders',}
    return render(request, 'index/home.html',{
        'video3_url': static('videos/video3.mp4'),
        'video4_url': static('videos/video4.mp4')
    })

def services(request):
    context = {'title': ' Services - Welcome to Elite Dream Builders'}
    return render(request, 'index/services.html')


def projects(request):
    all_projects = Project.objects.all()
    upcoming_projects = UpcomingProject.objects.all()
    context = {
        'title': 'Projects - Elite Dream Builders',
        'projects': all_projects,
        'upcoming_projects':upcoming_projects,
    }
    return render(request, 'index/projects.html', context)

def contact(request):
    images = GalleryImage.objects.all()
    about_sections = AboutSection.objects.all()
    context = {'title': 'Contact Us - Elite Dream Builders'
               ,'images':images,'about_sections':about_sections}
    return render(request, 'index/contact.html',context)

def project_details(request,project_id):
    project = get_object_or_404(Project ,id = project_id)
    context = {'title': 'Project Details - Elite Dream Builders',
               'project':project,}
    return render(request,'index/project details.html', context)



def get_quote(request):
    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote = form.save()
            
            # **User's Email**
            user_subject = "Quote Request Received"
            user_message = f"""
            Dear {quote.name},

            Thank you for requesting a quote. We have received your request and will get back to you soon.

            Details:
            - Name: {quote.name}
            - Email: {quote.email}
            - Phone: {quote.phone}
            - Service Type: {quote.service_type}
            - Budget Range: {quote.budget_range}

            Best Regards,
            Elite Dream Builders
            """
            send_mail(
                user_subject,
                user_message,
                settings.EMAIL_HOST_USER,  # Your email
                [quote.email],  # Send to user
                fail_silently=False,
            )


            # Success message for the user
            messages.success(request, "Your request has been submitted successfully! 👏")

            # Email to construction company
            admin_email = "kuttyvivek248@gmail.com"  # Replace with actual admin email
            subject = "New Quote Request"
            message = f"""
            Name: {quote.name}
            Email: {quote.email}
            phone: {quote.phone}
            Service Type: {quote.service_type}
            Budget Range: {quote.budget_range.name}
            """
            send_mail(subject, message, "kuttyvivek248@gmail.com", [admin_email])

            return redirect('get_quote')

    else:
        form = QuoteRequestForm()
    context = {'title': 'Get-Quote - Elite Dream Builders','form':form,}
    return render(request, 'index/get_quote.html',context)


def about(request):
    about_data = AboutVideo.objects.order_by('-id').first()
    context = {
        'title': 'About Us - Elite Dream Builders',
        'about': about_data  # Pass None if no records exist
    }
    return render(request, 'index/about.html', context)



def testimonals(request):
    reviews = Review.objects.all().order_by('-created_at')
    context = {'title': 'Testimonals - Elite Dream Builders','reviews':reviews}
    return render(request,'index/testimonals.html',context)

def terms(request):
    context = {'title': 'Testimonals - Elite Dream Builders'}
    return render(request,'index/terms.html',context)

# custom 404 error

def custom_404(request,exception):
    return render(request, 'index/404.html', status=404)

def custom_500(request):
    return render(request, 'index/500.html', status=500)


def serve_media(request, path):
    """ Serve media files securely """
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if not os.path.exists(file_path):
        raise Http404("File not found")

    content_type, _ = mimetypes.guess_type(file_path)
    content_type = content_type or "application/octet-stream"

    with open(file_path, 'rb') as f:
        return HttpResponse(f.read(), content_type=content_type)