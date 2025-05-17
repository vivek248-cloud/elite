from django.shortcuts import render, redirect,get_object_or_404
from django.core.mail import send_mail
import json
from twilio.rest import Client
from django.conf import settings
from django.contrib import messages
from .forms import QuoteRequestForm
from .models import Project
from .models import AboutVideo,Video
from .models import Review,AboutSection,AboutTitleVideo
from .models import UpcomingProject,GalleryImage,ProjectVideo,YouTubeVideo,HomeSlider,SliderVideo
from django.http import HttpResponseServerError
from django.http import HttpResponse, Http404
from django.http import JsonResponse

import os
import mimetypes
from django.templatetags.static import static
from django.core.exceptions import ImproperlyConfigured
import logging

from django.shortcuts import render, redirect
from django.http import JsonResponse


def home(request, category='residential'):
    # category = request.GET.get('category', 'residential') # Default to 'residential' if not provided
    all_projects = Project.objects.filter(category=category)[:3]
    sliders = HomeSlider.objects.all()
    return render(request, 'index/home.html',{
        'video3_url': static('videos/video3.mp4'),
        'video4_url': static('videos/video4.mp4'), 'title': 'Welcome to Elite Dream Builders',
               'projects': all_projects,
               'sliders': sliders,
    })



def category(request, category):
    # Filter projects by the provided category (case-insensitive)
    all_projects = Project.objects.filter(category=category)[:9]
    return render(request, 'index/category.html', {
        'title': f'{category} - Welcome to Elite Dream Builders',
        'projects': all_projects,
        'category': category.lower()  # Ensure consistent case
    })

def services(request):
    context = {'title': ' Services - Welcome to Elite Dream Builders'}
    return render(request, 'index/services.html')


def projects(request):
    all_projects = Project.objects.all()[:3]
    projectvideo = ProjectVideo.objects.all()[:3]
    upcoming_projects = UpcomingProject.objects.all()[:3]
    youtube_videos = YouTubeVideo.objects.all()[:3]
    videoslider = SliderVideo.objects.all()

    # Get the first project video URL securely
    if projectvideo.exists():
        first_video = projectvideo.first()
        project_video_url = first_video.video_file.build_url(resource_type='video', secure=True)
    else:
        project_video_url = ''

    context = {
        'title': 'Projects - Elite Dream Builders',
        'projects': all_projects,
        'upcoming_projects': upcoming_projects,
        'project_videos': projectvideo,  # all project videos
        'project_video_url': project_video_url,  # only the first video’s URL
        'youtube_videos': youtube_videos,
        'videoslider': videoslider,
    }
    return render(request, 'index/projects.html', context)


def load_more_projects(request):
    offset = int(request.GET.get('offset', 0))
    limit = 3
    projects = Project.objects.all()[offset:offset + limit]

    project_data = []
    for project in projects:
        project_data.append({
            'id': project.id,
            'title': project.title,
            'image_url': project.image.url,
            'budget_range': str(project.budget_range),  # <-- Convert to string
            'bhk': project.bhk,
            'description': project.description,
        })

    has_more = Project.objects.count() > offset + limit

    return JsonResponse({'projects': project_data, 'has_more': has_more})

# UpcomingProject


def load_more_upcomming_projects(request):
    offset = int(request.GET.get('offset', 0))
    limit = 3
    projects = UpcomingProject.objects.all()[offset:offset + limit]

    project_data = []
    for project in projects :
        project_data.append({
            'id': project.id,
            'title': project.title,
            'image_url': project.image.url,
            'budget_range': str(project.budget_range),  # <-- Convert to string
            'bhk': project.bhk,
            'description': project.description,
        })

    has_more = UpcomingProject.objects.count() > offset + limit

    return JsonResponse({'projects': project_data, 'has_more': has_more})

# ProjectVideo

def load_more_projects_videos(request):
    offset = int(request.GET.get('offset', 0))
    limit = 3
    projects = ProjectVideo.objects.all()[offset:offset + limit]

    project_data = []
    for project in projects:
        project_data.append({
            'id': project.id,
            'title': project.title,
            'video_file': project.video_file.url,
        })

    has_more = ProjectVideo.objects.count() > offset + limit

    return JsonResponse({'projects': project_data, 'has_more': has_more})

# youtube videos

def load_more_youtube_videos(request):
    offset = int(request.GET.get('offset', 0))
    limit = 3
    videos = YouTubeVideo.objects.all()[offset:offset + limit]

    video_data = []
    for video in videos:
        video_data.append({
            'id': video.id,
            'title': video.title,
            'youtube_link': video.youtube_link,
            'description': video.description,
        })

    has_more = YouTubeVideo.objects.count() > offset + limit

    return JsonResponse({'videos': video_data, 'has_more': has_more})


def load_more_projects_category(request):
    print("✅ load_more_projects_category view triggered")

    category = request.GET.get('category', '').strip().lower()
    offset = int(request.GET.get('offset', 0))
    limit = 3

    projects = Project.objects.filter(category__iexact=category).order_by('id')[offset:offset + limit]

    projects_data = [{
        'id': p.id,
        'title': p.title,
        'image_url': p.image.url,
        'budget_range': str(p.budget_range),  # convert to string if needed
        'bhk': p.bhk,
        'description': p.description,
        'location': p.location,
    } for p in projects]

    total_count = Project.objects.filter(category__iexact=category).count()
    has_more = offset + limit < total_count

    return JsonResponse({'projects': projects_data, 'has_more': has_more})




def contact(request):
    images = GalleryImage.objects.all()
    about_sections = AboutSection.objects.all()
    videoslider = SliderVideo.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        # Send email
        try:
            send_mail(
                subject,
                full_message,
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],
                fail_silently=False
            )
        except Exception as e:
            print(f"EMAIL ERROR: {e}")
            messages.error(request, "Failed to send email. Please try again.")

        # Send WhatsApp message via Twilio
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                from_='whatsapp:' + settings.TWILIO_WHATSAPP_NUMBER,
                to='whatsapp:' + settings.ADMIN_WHATSAPP_NUMBER,
                content_sid=settings.TWILIO_TEMPLATE_SID,  # Your template SID
                content_variables=json.dumps({
                    "1": name,
                    "2": email,
                    "3": message
                })
            )
            messages.success(request, "Thank you for contacting us! We'll reach out soon.")
        except Exception as e:
            print(f"WHATSAPP ERROR: {e}")
            messages.error(request, "Failed to send WhatsApp message.")

        return redirect('contact')
    context = {
        'title': 'Contact Us - Elite Dream Builders',
        'images': images,
        'about_sections': about_sections,
        'videoslider': videoslider,
    }
    return render(request, 'index/contact.html', context)



def project_details(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        project_type = 'project'
    except Project.DoesNotExist:
        try:
            project = UpcomingProject.objects.get(id=project_id)
            project_type = 'upcoming'
        except UpcomingProject.DoesNotExist:
            raise Http404("No matching project found.")

    context = {
        'title': 'Project Details - Elite Dream Builders',
        'project': project,
        'project_type': project_type,
    }
    return render(request, 'index/project details.html', context)



from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from twilio.rest import Client
import json
from .forms import QuoteRequestForm




from twilio.rest import Client
import json

def send_whatsapp_to_admin(quote):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            from_='whatsapp:' + settings.TWILIO_WHATSAPP_NUMBER,
            to='whatsapp:' + settings.ADMIN_WHATSAPP_NUMBER,
            content_sid=settings.TWILIO_TEMPLATE_SID_TWO,
            content_variables=json.dumps({
                "1": quote.name,
                "2": quote.email,
                "3": quote.phone,
                "4": quote.service_type,
                "5": quote.budget_range.name if quote.budget_range else "N/A",
            })
        )
        print("✅ WhatsApp message sent successfully.")
        return True
    except Exception as e:
        print(f"[Twilio Error] WhatsApp not sent: {e}")
        return False



# clite messages

from twilio.rest import Client
import json

def send_whatsapp_template(name, email, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        from_='whatsapp:' + settings.TWILIO_WHATSAPP_NUMBER,
        to='whatsapp:' + settings.ADMIN_WHATSAPP_NUMBER,  # Best practice
        content_sid=settings.TWILIO_TEMPLATE_SID,  # Use the settings variable
        content_variables=json.dumps({
            "1": name,
            "2": email,
            "3": message
        })
    )


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import QuoteRequestForm
from .models import BudgetRange


def get_quote(request):
    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)

            # Get budget_range from custom HTML select
            budget_range_id = request.POST.get("budget_range")
            if budget_range_id:
                try:
                    quote.budget_range = BudgetRange.objects.get(id=budget_range_id)
                except BudgetRange.DoesNotExist:
                    quote.budget_range = None

            quote.save()

            # ✅ Email to User
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
                settings.EMAIL_HOST_USER,  # sender
                [quote.email],
                fail_silently=False,
            )

            # ✅ Email to Admin
            admin_subject = "New Quote Request"
            admin_message = f"""
Name: {quote.name}
Email: {quote.email}
Phone: {quote.phone}
Service Type: {quote.service_type}
Budget Range: {quote.budget_range.name if quote.budget_range else 'N/A'}
"""
            send_mail(
                admin_subject,
                admin_message,
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            # ✅ WhatsApp to Admin
            if send_whatsapp_to_admin(quote):
                messages.success(request, "Your request has been submitted successfully! 👏")
            else:
                messages.warning(request, "Submitted, but WhatsApp message failed.")

            return redirect('get_quote')

    else:
        form = QuoteRequestForm()

    context = {
        'title': 'Get-Quote - Elite Dream Builders',
        'form': form,
    }
    return render(request, 'index/get_quote.html', context)


def about(request):
    about_data = AboutVideo.objects.order_by('-id').first()
    Abouttitlevideo = AboutTitleVideo.objects.order_by('-id').first()
    if Abouttitlevideo:
        video_url = Abouttitlevideo.video_file.build_url(resource_type='video', secure=True)
    else:
        video_url = ''
    if about_data:
        about_url = about_data.video_file.build_url(resource_type='video', secure=True)
    else:
        about_url =''
    context = {
        'title': 'About Us - Elite Dream Builders',
        'about': about_data,  # Pass None if no records exist
        'about_title_video': Abouttitlevideo,  # Pass None if no records exist
        'video_url': video_url,
        'about_url':about_url,
        
    }
    return render(request, 'index/about.html', context)
    



def testimonals(request):
    videos = Video.objects.all()
    reviews = Review.objects.all().order_by('-created_at')
    
    if videos.exists():
        first_video = videos.first()
        video_url = first_video.video_file.build_url(resource_type='video', secure=True)
    else:
        video_url = ''

    context = {
        'title': 'Testimonals - Elite Dream Builders',
        'reviews': reviews,
        'videos': videos,
        'video_url': video_url
    }
    return render(request, 'index/testimonals.html', context)


def terms(request):
    context = {'title': 'Terms & Conditions - Elite Dream Builders'}
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




