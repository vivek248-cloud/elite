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
    all_projects =  Project.objects.filter(status='completed').order_by('id')[:6]
    upcoming_projects = Project.objects.filter(status='ongoing').order_by('id')[:6]
    youtube_videos = YouTubeVideo.objects.all().order_by('id')[:3]


    context = {
        'title': 'Projects - Elite Dream Builders',
        'projects': all_projects,
        'upcoming_projects': upcoming_projects,

        'youtube_videos': youtube_videos,
        
    }

    return render(request, 'index/projects.html', context)




def load_more_projects(request):
    offset = int(request.GET.get('offset', 0))
    limit = 6

    # Only fetch completed projects to match the main view
    completed_projects = Project.objects.filter(status='completed').order_by('id')[offset:offset + limit]

    project_data = []
    for project in completed_projects:
        project_data.append({
            'slug': project.slug,
            'title': project.title,
            'image_url': project.image.url,
            'budget_range': str(project.budget_range),
            'bhk': project.bhk,
            'description': project.description,
        })

    has_more = Project.objects.filter(status='completed').count() > offset + limit

    return JsonResponse({'projects': project_data, 'has_more': has_more})

def load_more_upcomming_projects(request):
    offset = int(request.GET.get('offset', 0))
    limit = 6

    # Only fetch projects with status 'ongoing'
    ongoing_projects = Project.objects.filter(status='ongoing').order_by('id')
    upcoming_projects = ongoing_projects[offset:offset + limit]

    project_data = []
    for project in upcoming_projects:
        project_data.append({
            'slug': project.slug,
            'title': project.title,
            'image_url': project.image.url,
            'budget_range': str(project.budget_range),
            'bhk': project.bhk,
            'description': project.description,
        })

    # Use the same filtered queryset for counting
    has_more = ongoing_projects.count() > offset + limit

    return JsonResponse({'upcoming_projects': project_data, 'has_more': has_more})

# ProjectVideo

def load_more_projects_videos(request):
    offset = int(request.GET.get('offset', 0))
    limit = 3
    projects = ProjectVideo.objects.all().order_by('id')[offset:offset + limit]

    project_data = []
    for project in projects:
        try:
            secure_url = project.video_file.build_url(resource_type='video', secure=True)
        except Exception as e:
            print(f"Error generating secure URL for video {project.id}: {e}")
            secure_url = ''
        project_data.append({
            'id': project.id,
            'title': project.title,
            'video_file': secure_url,
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

    # Get first video from slider
    if videoslider.exists():
        first_video = videoslider.first()
        video_url = first_video.video_file.build_url(resource_type='video', secure=True)
    else:
        video_url = ''

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
                content_sid=settings.TWILIO_TEMPLATE_SID,
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
        'video_url': video_url,
    }
    return render(request, 'index/contact.html', context)




def project_details(request, slug):
    try:
        project = Project.objects.get(slug=slug)
        project_type = 'project'
    except Project.DoesNotExist:
        try:
            project = UpcomingProject.objects.get(slug=slug)
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

# def send_whatsapp_to_admin(quote):
#     try:
#         client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#         message = client.messages.create(
#             from_='whatsapp:' + settings.TWILIO_WHATSAPP_NUMBER,
#             to='whatsapp:' + settings.ADMIN_WHATSAPP_NUMBER,
#             content_sid=settings.TWILIO_TEMPLATE_SID_TWO,
#             content_variables=json.dumps({
#                 "1": quote.name,
#                 "2": quote.email,
#                 "3": quote.phone,
#                 "4": quote.service_type,
#                 "5": quote.budget_range.name if quote.budget_range else "N/A",
#             })
#         )
#         print("✅ WhatsApp message sent successfully.")
#         return True
#     except Exception as e:
#         print(f"[Twilio Error] WhatsApp not sent: {e}")
#         return False

import requests

def send_whatsapp_to_admin(quote):
    try:
        url = f"https://graph.facebook.com/v19.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        data = {
            "messaging_product": "whatsapp",
            "to": settings.ADMIN_WHATSAPP_NUMBER,  # e.g., '919XXXXXXXXX'
            "type": "template",
            "template": {
                "name": "admin_quote_notify",  # Template name from WhatsApp Manager
                "language": {
                    "code": "en"
                },
                "components": [
                  {
                    "type": "body",
                    "parameters": [
                      {"type": "text", "text": quote.name},
                      {"type": "text", "text": quote.email},
                      {"type": "text", "text": quote.service_type},
                      {"type": "text", "text": quote.budget_range.name if quote.budget_range else "N/A"},
                    ]
                  }
                ]

            }
        }

        response = requests.post(url, headers=headers, json=data)
        print("📤 WhatsApp Response:", response.json())
        return response.status_code == 200

    except Exception as e:
        print(f"[Meta API Error] WhatsApp not sent: {e}")
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
    about_title_video = AboutTitleVideo.objects.order_by('-id').first()

   
    context = {
        'title': 'About Us - Elite Dream Builders',
        'about': about_data,
        'about_title_video': about_title_video,
        
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


from .forms import QuoteRequestForm,CareerEmailForm

from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render
from .forms import CareerEmailForm
import logging

def careers(request):
    success = False
    error = False

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        resume = request.FILES.get('resume')

        try:
            email_message = EmailMessage(
                subject=f"New Career Application from {name}",
                body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=settings.EMAIL_HOST_USER,
                to=['elitedreambuilders.in@gmail.com'],
            )

            if resume:
                email_message.attach(resume.name, resume.read(), resume.content_type)

            email_message.send()
            success = True
        except Exception as e:
            print(f"Error sending email: {e}")
            error = True

    return render(request, 'main/about.html', {'success': success, 'error': error})


def row_villa_view(request):
    return render(request, 'index/row-villa.html')