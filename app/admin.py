from django.contrib import admin
from .models import Disease, Patient, Appointment

# DiseaseAdmin class
class DiseaseAdmin(admin.ModelAdmin):
    # Specify which fields should be displayed in the list view
    list_display = ('name', 'description', 'image')

    # Add search capability for certain fields
    search_fields = ('name',)

    # Add filters on the right side of the admin page
    list_filter = ('name',)

# Registering Disease model
admin.site.register(Disease, DiseaseAdmin)

# PatientAdmin class
class PatientAdmin(admin.ModelAdmin):
    # Fields to be displayed in the list view
    list_display = ('patient_id', 'first_name', 'last_name', 'email', 'contact_number', 'age')

    # Fields to be searchable in the admin interface
    search_fields = ('patient_id', 'first_name', 'last_name', 'email', 'contact_number')

    # Filters to make it easier to navigate in the admin panel
    list_filter = ('age',)

    # ordering = ('-created_at',)

# Registering Patient model
admin.site.register(Patient, PatientAdmin)

# AppointmentAdmin class
class AppointmentAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('patient','email','contact_number','appointment_date', 'appointment_time', 'diseases', 'patient_type', 'visit_status','created_at', 'updated_at')

    # Fields to be searchable in the admin interface
    search_fields = ('patient__first_name', 'patient__last_name', 'appointment_date', 'appointment_time','visit_status')

    # Add filters to make it easier to navigate
    list_filter = ('appointment_date', 'appointment_time', 'patient_type','visit_status')

    # Inlines to handle patient details if it's a new patient
    def patient(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.patient_type == "new" else obj.patient.patient_id
    patient.admin_order_field = 'patient'  # Make this field sortable by the patient name

# Registering Appointment model
admin.site.register(Appointment, AppointmentAdmin)




from .models import SocialLanding, BookingLead
from django.utils.html import format_html

@admin.register(SocialLanding)
class SocialLandingAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'phone', 'hero_image_preview', 'created_at')
    readonly_fields = ('created_at', 'hero_image_preview', 'result_image_preview', 'video_preview')

    fieldsets = (
        ('Basic Info', {
            'fields': ('slug', 'title', 'subtitle', 'hero_image', 'hero_image_preview')
        }),
        ('Video Section', {
            'fields': ('video_title', 'video_description', 'video', 'video_preview')
        }),
        ('Results Section', {
            'fields': ('result_title', 'result_image', 'result_image_preview')
        }),
        ('Testimonials', {
            'fields': (
                'testimonial_1_review', 'testimonial_1_name',
                'testimonial_2_review', 'testimonial_2_name',
                'testimonial_3_review', 'testimonial_3_name',
            )
        }),
        ('Contact', {
            'fields': ('whatsapp_message', 'phone', 'active')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

    prepopulated_fields = {"slug": ("title",)}

    def hero_image_preview(self, obj):
        if obj.hero_image:
            return format_html('<img src="{}" style="max-height: 60px;"/>', obj.hero_image.url)
        return "-"
    hero_image_preview.short_description = "Hero Image"

    def result_image_preview(self, obj):
        if obj.result_image:
            return format_html('<img src="{}" style="max-height: 60px;"/>', obj.result_image.url)
        return "-"
    result_image_preview.short_description = "Result Image"

    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video width="250" controls>'
                '<source src="{}" type="video/mp4">'
                'Your browser does not support the video tag.'
                '</video>',
                obj.video.url
            )
        return "-"
    video_preview.short_description = "Video Preview"


@admin.register(BookingLead)
class BookingLeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'source', 'landing_slug', 'created_at', 'notified')
    readonly_fields = ('created_at',)


from .models import ClinicHoliday

@admin.register(ClinicHoliday)
class ClinicHolidayAdmin(admin.ModelAdmin):
    list_display = ('date', 'closed_slot', 'title', 'is_active')
    list_filter = ('closed_slot', 'is_active')
    search_fields = ('title',)




from .models import HairWellnessReport

@admin.register(HairWellnessReport)
class HairWellnessReportAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "total_score", "status", "phase", "created_at")
    search_fields = ("patient_name", "contact")
    list_filter = ("status", "created_at")
