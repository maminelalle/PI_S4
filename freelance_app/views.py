from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, JobOffer, Application, Message, Resource, Review, Comment
from .forms import JobOfferForm, ApplicationForm, MessageForm, ResourceForm, ReviewForm, CommentForm
from django.contrib.auth import authenticate, login
# from .forms import LoginForm, FreelancerRegistrationForm, ClientRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q , Count , Exists, OuterRef
from datetime import date

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Vous êtes bien enregistré.")
            form = RegistrationForm()  # formulaire vide après succès
            return render(request, 'register.html', {'form': form, 'redirect_to_login': True})
        else:
            # Ne pas afficher les erreurs détaillées du formulaire dans le template,
            # juste un message d'erreur global précisant que c'est le formulaire d'inscription.
            messages.error(request, "Erreur dans le formulaire d'inscription. Veuillez vérifier vos données.")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        print("Tentative de connexion reçue.")
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            print("Formulaire valide.")
            try:
                user = form.get_user()
                print(f"Utilisateur récupéré depuis la base de données : {user}")

                login(request, user)
                print(f"Utilisateur connecté : {user.email} (type: {user.user_type})")

                # Redirection basée sur le type d'utilisateur
                if user.user_type == 'client':
                    return redirect('dashboard_client')
                elif user.user_type == 'freelancer':
                    return redirect('dashboard')
                else:
                    print("Type d'utilisateur non reconnu.")
                    messages.error(request, "Type d'utilisateur non reconnu.")
                    return redirect('login')

            except Exception as e:
                print("❌ Erreur lors de la récupération ou connexion de l'utilisateur :", e)
                messages.error(request, "Erreur interne. Veuillez réessayer plus tard.")
                return redirect('login')
        else:
            print("❌ Formulaire invalide. Données reçues :", request.POST)
            print("Erreurs du formulaire :", form.errors)
            messages.error(request, "Email ou mot de passe invalide.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('login')   


# Dashboard principal
# @login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# ========================
#   SECTION CLIENT
# ========================

@login_required
def client_dashboard(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    return render(request, 'dashboard_client.html')

 

@login_required
def client_create_job(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = JobOfferForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user
            job.save()
            messages.success(request, 'Votre offre a été publiée avec succès!')
            return redirect('client_job_list')
    else:
        form = JobOfferForm()
    
    return render(request, 'client/client_create_job.html', {'form': form})

@login_required
def client_job_list(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    
    jobs = JobOffer.objects.filter(client=request.user).annotate(
        application_count=Count('applications')
    ).order_by('-date_posted')
    
    # Status counts for the cards
    status_counts = {
        'all': jobs.count(),
        'open': jobs.filter(status='open').count(),
        'in_progress': jobs.filter(status='in_progress').count(),
        'in_review': jobs.filter(status='in_review').count(),
        'completed': jobs.filter(status='completed').count(),
        'cancelled': jobs.filter(status='cancelled').count(),
    }
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter and status_filter != 'all':
        jobs = jobs.filter(status=status_filter)
    
    return render(request, 'client/client_job_list.html', {
        'jobs': jobs,
        'status_counts': status_counts,
    })

@login_required
def client_messages(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')

    # Annotate freelancers with unread message count
    freelancers = User.objects.filter(
        Q(received_messages__sender=request.user) |
        Q(sent_messages__receiver=request.user),
        user_type='freelancer'
    ).distinct().annotate(
        unread_count=Count('sent_messages', 
                         filter=Q(sent_messages__receiver=request.user,
                                sent_messages__is_read=False))
    )

    # Get selected freelancer
    selected_freelancer_id = request.GET.get('freelancer')
    if selected_freelancer_id:
        selected_freelancer = get_object_or_404(User, id=selected_freelancer_id, user_type='freelancer')
    elif freelancers.exists():
        selected_freelancer = freelancers.first()
    else:
        selected_freelancer = None

    # Get conversation messages
    messages_list = []
    if selected_freelancer:
        messages_list = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=selected_freelancer)) |
            (Q(sender=selected_freelancer) & Q(receiver=request.user))
        ).order_by('sent_at')

        # Mark received messages as read
        Message.objects.filter(
            receiver=request.user,
            sender=selected_freelancer,
            is_read=False
        ).update(is_read=True)

    # Handle message form
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid() and selected_freelancer:
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = selected_freelancer
            message.save()
            return redirect(f"{request.path}?freelancer={selected_freelancer.id}")
    else:
        form = MessageForm()

    return render(request, 'client/client_messages.html', {
        'freelancers': freelancers,
        'selected_freelancer': selected_freelancer,
        'messages': messages_list,
        'form': form,
        'today': date.today()
    })
@login_required
def get_messages(request):
    if request.method == 'GET' and request.is_ajax():
        freelancer_id = request.GET.get('freelancer_id')
        freelancer = get_object_or_404(User, id=freelancer_id)
        
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=freelancer)) |
            (Q(sender=freelancer) & Q(receiver=request.user))
        ).order_by('sent_at')
        
        messages_data = []
        for msg in messages:
            messages_data.append({
                'sender': msg.sender.email,
                'content': msg.content,
                'sent_at': msg.sent_at.strftime("%H:%M %d/%m/%Y"),
                'is_sender': msg.sender == request.user,
                'file_url': msg.file.url if msg.file else None,
                'file_name': msg.file.name.split('/')[-1] if msg.file else None,
            })
        
        return JsonResponse({'messages': messages_data})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def client_payments(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    return render(request, 'client/client_payments.html')

@login_required
def client_profile(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    return render(request, 'client/client_profile.html')

@login_required
def client_resources(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    resources = Resource.objects.filter(author=request.user)
    return render(request, 'client/client_resources.html', {'resources': resources})


@login_required
def client_reviews(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    reviews = Review.objects.filter(reviewed=request.user)
    return render(request, 'client/client_reviews.html', {'reviews': reviews})



@login_required
def client_settings(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    return render(request, 'client/client_settings.html')


@login_required
def client_view_applications(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    # job = get_object_or_404(JobOffer, pk=pk, client=request.user)
    # applications = Application.objects.filter(job=job)
    return render(request, 'client/client_view_applications.html')
 











# @login_required
# def client_accept_application(request, pk):
#     if request.user.user_type != 'client':
#         return redirect('dashboard')
    
#     application = get_object_or_404(Application, pk=pk, job__client=request.user)
#     application.status = 'accepted'
#     application.save()
    
#     # Rejeter automatiquement les autres candidatures
#     Application.objects.filter(job=application.job).exclude(pk=pk).update(status='rejected')
    
#     messages.success(request, "Candidature acceptée avec succès")
#     return redirect('client_view_applications', pk=application.job.pk)

# @login_required
# def client_reject_application(request, pk):
#     if request.user.user_type != 'client':
#         return redirect('dashboard')
    
#     application = get_object_or_404(Application, pk=pk, job__client=request.user)
#     application.status = 'rejected'
#     application.save()
    
#     messages.success(request, "Candidature rejetée")
#     return redirect('client_view_applications', pk=application.job.pk)