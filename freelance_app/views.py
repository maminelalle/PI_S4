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
            return redirect('client_job_list')
    else:
        form = JobOfferForm()
    return render(request, 'client_create_job.html', {'form': form})


@login_required
def client_job_list(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    jobs = JobOffer.objects.filter(client=request.user)
    return render(request, 'client_job_list.html', {'jobs': jobs})


@login_required
def client_view_applications(request, pk):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    job = get_object_or_404(JobOffer, pk=pk, client=request.user)
    applications = Application.objects.filter(job=job)
    return render(request, 'client_view_applications.html', {
        'applications': applications,
        'job': job
    })

@login_required
def client_messages(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    messages = Message.objects.filter(receiver=request.user)
    return render(request, 'client_messages.html', {'messages': messages})


@login_required
def client_profile(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    return render(request, 'client_profile.html')


@login_required
def client_reviews(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    reviews = Review.objects.filter(reviewed=request.user)
    return render(request, 'client_reviews.html', {'reviews': reviews})


@login_required
def client_resources(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    resources = Resource.objects.filter(author=request.user)
    return render(request, 'client_resources.html', {'resources': resources})


@login_required
def client_payments(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    return render(request, 'client_payments.html')


@login_required
def client_settings(request):
    if request.user.user_type != 'client':
        return redirect('dashboard')
    return render(request, 'client_settings.html')
