from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# class User(AbstractUser):
#     USER_TYPE_CHOICES = [
#         ('freelancer', 'Freelancer'),
#         ('client', 'Client'),
#     ]

#     email = models.EmailField(unique=True)
#     profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
#     user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='freelancer')  # Valeur par défaut ajoutée

#     # Champs communs optionnels
#     skills = models.TextField(blank=True, null=True)
#     experience = models.TextField(blank=True, null=True)
#     portfolio_url = models.URLField(blank=True, null=True)
#     cv_file = models.FileField(upload_to='cv_files/', blank=True, null=True)
#     location = models.CharField(max_length=255, blank=True, null=True)

#     # Champs spécifiques client
#     company_name = models.CharField(max_length=255, blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     website = models.URLField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.username} ({self.get_user_type_display()})"



class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('freelancer', 'Freelancer'),
        ('client', 'Client'),
    ]

    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='freelancer')

    # Champs communs
    skills = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    cv_file = models.FileField(upload_to='cv_files/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    # Champs client
    company_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.get_user_type_display()})"


class JobOffer(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'client'})
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    is_remote = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()

    def clean(self):
        if self.client.user_type != 'client':
            raise ValidationError("Only users with user_type 'client' can post job offers.")

    def __str__(self):
        return self.title


class Application(models.Model):
    job = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'freelancer'})
    cover_letter = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=[('sent', 'Sent'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='sent'
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.freelancer.user_type != 'freelancer':
            raise ValidationError("Only users with user_type 'freelancer' can apply for jobs.")

    def __str__(self):
        return f"{self.freelancer.username} applied for {self.job.title}"


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


class Resource(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    file = models.FileField(upload_to='resource_files/', null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    reviewer = models.ForeignKey(User, related_name='given_reviews', on_delete=models.CASCADE)
    reviewed = models.ForeignKey(User, related_name='received_reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewed.username}"


class Comment(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.resource.title}"
