from django.db import models
import random
# =========================================
from django.db import models
import random
import string


def test_generate_patient_id():

    while True:

        random_part = ''.join(
            random.choices(
                string.digits,
                k=6
            )
        )

        patient_id = f"MHC-{random_part}"

        if not TestPatient.objects.filter(
            patient_id=patient_id
        ).exists():

            return patient_id


class TestPatient(models.Model):

    patient_id = models.CharField(
        max_length=20,
        primary_key=True,
        unique=True,
        editable=False,
        default=test_generate_patient_id
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    dob = models.DateField()

    gender = models.CharField(
        max_length=20
    )

    contact_number = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return (
            f"{self.patient_id} - "
            f"{self.first_name}"
        )


from django.db import models
import uuid


class TestAppointment(models.Model):

    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('checked_in', 'Checked In'),
        ('cancelled', 'Cancelled'),
    ]

    appointment_id = models.CharField(
        max_length=20,
        primary_key=True,
        editable=False
    )

    patient = models.ForeignKey(
        TestPatient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    disease = models.CharField(
        max_length=255
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    visit_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='booked'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.appointment_id:

            self.appointment_id = (
                f"APT-{uuid.uuid4().hex[:6].upper()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.patient.patient_id} - "
            f"{self.appointment_date}"
        )







# ==========================











class HairWellnessReport(models.Model):
    patient_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)

    subtotal_a = models.IntegerField()
    subtotal_b = models.IntegerField()
    subtotal_c = models.IntegerField()
    subtotal_e = models.IntegerField()

    total_score = models.IntegerField()
    status = models.CharField(max_length=50)
    phase = models.CharField(max_length=150)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.total_score}"


class Disease(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='diseases/', null=True, blank=True)

    def __str__(self):
        return self.name

class Patient(models.Model):
    patient_id = models.CharField(max_length=9, unique=True, primary_key=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    contact_number = models.CharField(max_length=15)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def generate_patient_id(self):
        """Generate a unique patient ID like 'PT-123456'."""
        while True:
            random_number = random.randint(100000, 999999)  # Generates a random 6-digit number
            patient_id = f"PT-{random_number}"
            if not Patient.objects.filter(patient_id=patient_id).exists():
                return patient_id

    def save(self, *args, **kwargs):
        """Override save to generate patient_id before saving."""
        if not self.patient_id:
            self.patient_id = self.generate_patient_id()
        super(Patient, self).save(*args, **kwargs)



from django.db import models
import uuid

class Appointment(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    booking_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True   # IMPORTANT for existing 1000 records
    )
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    diseases = models.TextField()

    patient_type = models.CharField(
        max_length=10,
        choices=[('new', 'New Patient'), ('existing', 'Follow-up')]
    )

    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('visited', 'Visited'),
        ('cancelled', 'Cancelled'),
        ('unvisited', 'Unvisited'),
    ]

    visit_status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='booked'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ✅ DATABASE-LEVEL DUPLICATE PROTECTION (THIS IS THE KEY)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['appointment_date', 'appointment_time'],
                name='unique_time_slot'
            )
        ]
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):

        name = f"{self.first_name} {self.last_name}"

        return f"{name} | {self.appointment_date} {self.appointment_time}"

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = f"MHC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

# yourapp/models.py
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

try:
    # Django 3.1+ supports JSONField on all DBs
    from django.db.models import JSONField
except ImportError:
    # For older versions, fallback to TextField (store JSON string)
    JSONField = None

class SocialLanding(models.Model):
    slug = models.SlugField(max_length=120, unique=True)
    title = models.CharField(max_length=220)
    subtitle = models.CharField(max_length=300, blank=True)
    hero_image = models.ImageField(upload_to='landing_images/', blank=True, null=True)

    video_title =  models.CharField(max_length=300, blank=True)
    video_description = models.TextField(blank=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)

    result_title = models.CharField(max_length=300, blank=True)
    result_image = models.ImageField(upload_to='landing_images/', blank=True, null=True)

    testimonial_1_review = models.TextField(blank=True)
    testimonial_1_name = models.CharField(max_length=300, blank=True)

    testimonial_2_review = models.TextField(blank=True)
    testimonial_2_name = models.CharField(max_length=300, blank=True)


    testimonial_3_review = models.TextField(blank=True)
    testimonial_3_name = models.CharField(max_length=300, blank=True)


    whatsapp_message = models.CharField(max_length=350, blank=True)
    phone = models.CharField(max_length=30, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('social_landing_slug', args=[self.slug])

    def image_url_absolute(self, request):
        if self.hero_image:
            return request.build_absolute_uri(self.hero_image.url)
        from django.templatetags.static import static
        return request.build_absolute_uri(static('images/default-hero.jpg'))


    def __str__(self):
        return self.title


class BookingLead(models.Model):
    SOURCE_CHOICES = [
        ('landing', 'Landing Page'),
        ('site', 'Website'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    preferred_date = models.CharField(max_length=50, blank=True)
    message = models.TextField(blank=True)
    source = models.CharField(max_length=30, choices=SOURCE_CHOICES, default='landing')
    landing_slug = models.CharField(max_length=120, blank=True)
    utm = JSONField(blank=True, null=True) if JSONField else models.TextField(blank=True, null=True, help_text='JSON string if DB does not support JSONField')
    created_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} — {self.phone} ({self.created_at:%Y-%m-%d %H:%M})"


from django.db import models

class ClinicHoliday(models.Model):

    SLOT_CHOICES = [
        ('full', 'Full Day Closed'),
        ('morning', 'Morning Closed'),
        ('evening', 'Evening Closed'),
    ]

    date = models.DateField()
    closed_slot = models.CharField(
        max_length=10,
        choices=SLOT_CHOICES,
        default='full'
    )
    title = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('date', 'closed_slot')
        ordering = ['date']

    def __str__(self):
        return f"{self.date} - {self.closed_slot}"


