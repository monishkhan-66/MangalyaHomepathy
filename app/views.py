from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils.timezone import now
import random
from .models import Patient, Appointment,Disease
from datetime import date
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime, time
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction






# Utility function to generate a unique Booking ID
generated_ids = set()

def generate_booking_id():
    """Generate a unique Booking ID like 'MHC-564323'"""
    while True:
        random_number = random.randint(100000, 999999)  # Generates a random 6-digit number
        booking_id = f"MHC-{random_number}"

        # Check if the generated booking ID already exists in the set
        if booking_id not in generated_ids:
            generated_ids.add(booking_id)  # Add the new ID to the set
            return booking_id  # Return the unique booking ID


# View to display the home page and diseases list
def index(request):
    disease = Disease.objects.all()
    return render(request, 'index.html', {'disease': disease})

def treatments(request):
    return render(request,"treatments.html")

def aboutus(request):
    pass


from .models import HairWellnessReport

def hhi(request):
    if request.method == "POST":
        HairWellnessReport.objects.create(
            patient_name=request.POST.get("patient_name"),
            age=request.POST.get("age") or None,
            gender=request.POST.get("gender"),
            contact=request.POST.get("contact"),

            subtotal_a=request.POST.get("subtotal_a"),
            subtotal_b=request.POST.get("subtotal_b"),
            subtotal_c=request.POST.get("subtotal_c"),
            subtotal_e=request.POST.get("subtotal_e"),

            total_score=request.POST.get("total_score"),
            status=request.POST.get("status"),
            phase=request.POST.get("phase"),
        )
        return redirect("hhi")

    reports = HairWellnessReport.objects.order_by("-created_at")[:20]

    return render(request, "hairHealthIndex.html", {
        "reports": reports
    })



def appointment_success(request, booking_id):

    appointment = Appointment.objects.get(
        booking_id=booking_id
    )

    name = f"{appointment.first_name} {appointment.last_name}"

    mobile = appointment.contact_number

    email = appointment.email

    return render(request, "appointment_success.html", {
        "booking_id": appointment.booking_id,
        "name": name,
        "mobile_number": mobile,
        "email": email,
        "appointment_date": appointment.appointment_date,
        "appointment_time": appointment.appointment_time.strftime("%I:%M %p"),
        "diseases": appointment.diseases,
        "appointment": appointment,
    })

# View to handle the booking appointment form
# def book_appointment(request):
#     today_date = date.today().isoformat()

#     if request.method == 'POST':
#         # 🔒 Prevent re-starting booking if already completed
#         if request.session.get("booking_completed"):
#             return redirect("appointment_success")

#         first_name = request.POST.get('firstName', '').strip()
#         last_name = request.POST.get('lastName', '').strip()
#         email = request.POST.get('email', '').strip()
#         contact_number = request.POST.get('contactNumber', '').strip()
#         patient_type = request.POST.get('patientType', '').strip()
#         appointment_date = request.POST.get('appointment_date', '').strip()
#         appointment_time = request.POST.get('appointment_time', '').strip()
#         diseases = request.POST.get('diseases', '').strip()

#         age = request.POST.get('age', '').strip() if patient_type == 'new' else None
#         patient_id = request.POST.get('patient_id', '').strip() if patient_type == 'existing' else None

#         if patient_type == 'existing':
#             try:
#                 patient = Patient.objects.get(patient_id=patient_id)
#                 email = patient.email
#                 contact_number = patient.contact_number
#             except Patient.DoesNotExist:
#                 return HttpResponse("Patient not found.", status=400)

#         # Generate OTP
#         otp = random.randint(100000, 999999)

#         request.session['otp'] = str(otp)
#         request.session['otp_sent_time'] = now().timestamp()
#         request.session['booking_completed'] = False

#         request.session['form_data'] = {
#             'first_name': first_name if patient_type == 'new' else patient.first_name,
#             'last_name': last_name if patient_type == 'new' else patient.last_name,
#             'email': email,
#             'contact_number': contact_number,
#             'patient_type': patient_type,
#             'appointment_date': appointment_date,
#             'appointment_time': appointment_time,
#             'diseases': diseases,
#             'age': age,
#             'patient_id': patient_id,
#         }

#         message = f"""
#                 Dear Patient,

#                 Thank you for choosing Mangalya Homeopathy.

#                 Your One-Time Password (OTP) for appointment booking is:

#                 {otp}

#                 This OTP is valid for 60 seconds and can be used only once.

#                 If you did not request this, please ignore this email.

#                 Regards,
#                 Mangalya Homeopathy Clinic
#                 Nalasopara West
#                 """
#         subject = "Mangalya Homeopathy – Appointment OTP"

#         try:
#             send_mail(
#                 subject,
#                 message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [email],
#                 fail_silently=False
#             )
#         except Exception as e:
#             print("Email failed:", e)
#             # DO NOT stop booking
#             # Do NOT return error
#             pass

#         return redirect('verify_otp')

#     return render(request, 'book_appointment.html', {'today_date': today_date})


# ========================================== without otp ===============================
from django.db import IntegrityError, transaction

def book_appointment(request):
    today_date = date.today().isoformat()

    if request.method == 'POST':

        first_name = request.POST.get('firstName', '').strip()
        last_name = request.POST.get('lastName', '').strip()
        email = request.POST.get('email', '').strip()
        contact_number = request.POST.get('contactNumber', '').strip()
        patient_type = request.POST.get('patientType', '').strip()
        appointment_date = request.POST.get('appointment_date', '').strip()
        appointment_time = request.POST.get('appointment_time', '').strip()
        diseases = request.POST.get('diseases', '').strip()

        age = request.POST.get('age', '').strip() if patient_type == 'new' else None
        patient_id = request.POST.get('patient_id', '').strip() if patient_type == 'existing' else None

        try:
            with transaction.atomic():

                if patient_type == 'new':
                    appointment = Appointment.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        contact_number=contact_number,
                        age=age,
                        appointment_date=appointment_date,
                        appointment_time=appointment_time,
                        diseases=diseases,
                        patient_type='new'
                    )
                    patient_name = f"{first_name} {last_name}"

                else:
                    appointment = Appointment.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    contact_number=contact_number,
                    age=age,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    diseases=diseases,
                    patient_type='existing')

                    patient_name = f"{first_name} {last_name}"

        except IntegrityError:
            return HttpResponse("This time slot is already booked.", status=400)

        # ✅ IMPORTANT — use DB generated booking_id
        return redirect("appointment_success", booking_id=appointment.booking_id)

    return render(request, 'book_appointment.html', {'today_date': today_date})

# View to handle OTP verification
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.core.mail import send_mail

def verify_otp(request):
    form_data = request.session.get('form_data')
    otp = request.session.get('otp')

    # 🔒 Basic guards
    if not form_data or not otp:
        return redirect('book_appointment')

    if request.session.get("booking_completed"):
        return redirect("appointment_success")

    appointment_date = form_data.get('appointment_date')

    otp_sent_time = request.session.get('otp_sent_time')
    remaining_time = max(
        0,
        60 - int(now().timestamp() - otp_sent_time)
    ) if otp_sent_time else 0

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        # ❌ Wrong OTP
        if entered_otp != otp:
            return render(request, 'verify_otp.html', {
                'otp_error': True,
                'remaining_time': remaining_time,
                'mobile_number': form_data.get('contact_number')
            })

        patient_type = form_data.get('patient_type')

        try:
            # 🔐 ATOMIC DB WRITE
            with transaction.atomic():

                if patient_type == 'new':
                    appointment = Appointment.objects.create(
                        first_name=form_data['first_name'],
                        last_name=form_data['last_name'],
                        email=form_data['email'],
                        contact_number=form_data['contact_number'],
                        age=form_data.get('age'),
                        appointment_date=appointment_date,
                        appointment_time=form_data.get('appointment_time'),
                        diseases=form_data.get('diseases'),
                        patient_type='new'
                    )
                    patient_name = f"{form_data['first_name']} {form_data['last_name']}"

                else:
                    patient = Patient.objects.get(
                        patient_id=form_data['patient_id']
                    )
                    appointment = Appointment.objects.create(
                        patient=patient,
                        appointment_date=appointment_date,
                        appointment_time=form_data.get('appointment_time'),
                        diseases=form_data.get('diseases'),
                        patient_type='existing'
                    )
                    patient_name = f"{patient.first_name} {patient.last_name}"

        except IntegrityError:
            # ⚠️ Slot already booked
            return render(request, 'verify_otp.html', {
                'slot_error': "This time slot has already been booked. Please choose another slot.",
                'remaining_time': remaining_time,
                'mobile_number': form_data.get('contact_number')
            })

        # ✅ SUCCESS — LOCK SESSION
        request.session["booking_completed"] = True
        request.session.pop("otp", None)
        request.session.pop("otp_sent_time", None)

        # Generate booking ID AFTER success
        booking_id = generate_booking_id()

        # 📧 EMAILS — NEVER BREAK FLOW
        try:
            send_mail(
                f"Appointment Confirmed - {booking_id}",
                f"Dear {patient_name}, your appointment is confirmed.\nBooking ID: {booking_id}",
                "no-reply@yourdomain.com",
                [form_data.get('email')],
                fail_silently=True
            )

            send_mail(
                f"New Appointment - {booking_id}",
                f"New appointment booked by {patient_name}.",
                "no-reply@yourdomain.com",
                ['clinic_email@yourdomain.com'],
                fail_silently=True
            )
        except Exception:
            pass  # never crash booking

        # Store success data
        request.session['success_data'] = {
            'booking_id': booking_id,
            'name': patient_name,
            'mobile_number': form_data.get('contact_number'),
            'email': form_data.get('email'),
            'appointment_date': appointment_date,
            'appointment_time': form_data.get('appointment_time'),
            'diseases': form_data.get('diseases'),
        }

        return redirect("appointment_success")

    return render(request, 'verify_otp.html', {
        'remaining_time': remaining_time,
        'mobile_number': form_data.get('contact_number')
    })



# Resend OTP functionality
def resend_otp(request):
    if not request.session.get('form_data'):
        return redirect('book_appointment')

    otp = random.randint(100000, 999999)
    request.session['otp'] = str(otp)
    request.session['otp_sent_time'] = now().timestamp()

    email = request.session['form_data'].get('email')

    send_mail(
        "Your New OTP",
        f"Your new OTP is {otp}.",
        "no-reply@yourdomain.com",
        [email]
    )

    return redirect('verify_otp')


from django.shortcuts import render
from django.utils.timezone import now
from .models import Appointment
from django.db.models import Q
from datetime import datetime
import calendar

@login_required(login_url="/login/")
def dashboard_appointments(request):
    today = now().date()

    filter_date = request.GET.get('date', '')
    filter_month = request.GET.get('month', '')
    filter_year = request.GET.get('year', str(today.year))
    search_query = request.GET.get('search', '').strip()
    time_filters = request.GET.getlist('time')

    appointments = Appointment.objects.all()

    # DEFAULT → TODAY
    if not filter_date and not filter_month:
        appointments = appointments.filter(appointment_date=today)
        filter_month = str(today.month)

    # DATE FILTER
    if filter_date:
        try:
            appointments = appointments.filter(
                appointment_date=datetime.strptime(filter_date, "%Y-%m-%d").date()
            )
        except ValueError:
            pass

    # MONTH FILTER
    elif filter_month:
        appointments = appointments.filter(
            appointment_date__month=int(filter_month),
            appointment_date__year=int(filter_year)
        )

    # SEARCH
    if search_query:
        appointments = appointments.filter(
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query)
        )

    # TIME SLOT FILTER
    if time_filters:
        q = Q()

        if 'morning' in time_filters:
            q |= Q(
                appointment_time__gte=time(6, 0),
                appointment_time__lt=time(12, 0)
            )

        if 'afternoon' in time_filters:
            q |= Q(
                appointment_time__gte=time(12, 0),
                appointment_time__lt=time(17, 0)
            )

        if 'evening' in time_filters:
            q |= Q(
                appointment_time__gte=time(17, 0),
                appointment_time__lt=time(22, 0)
            )

        appointments = appointments.filter(q)

    appointments = appointments.order_by('appointment_time')

    # KPI CALCULATIONS
    kpi_month = int(filter_month) if filter_month else today.month
    kpi_year = int(filter_year)
    selected_date = filter_date if filter_date else today.strftime("%Y-%m-%d")


    context = {
        "appointments": appointments,
        "today": today,
        "months": [(i, calendar.month_abbr[i]) for i in range(1, 13)],
        "years": range(today.year, today.year - 5, -1),
        "selected_month": str(kpi_month),
        "selected_year": str(kpi_year),

        "today_count": Appointment.objects.filter(
            appointment_date=today
        ).count(),

        "month_count": Appointment.objects.filter(
            appointment_date__month=kpi_month,
            appointment_date__year=kpi_year
        ).count(),

        "year_count": Appointment.objects.filter(
            appointment_date__year=kpi_year
        ).count(),

        "selected_month_name": calendar.month_name[kpi_month],
        "time_filters": time_filters,   # ✅ for template checkboxes
        "selected_date": selected_date,

    }

    return render(request, "appointments.html", context)


def my_appointments(request):
    if request.method == "POST":
        value = request.POST.get("value")

        otp = random.randint(100000, 999999)

        request.session["my_appt_otp"] = str(otp)
        request.session["my_appt_value"] = value
        request.session["my_appt_time"] = now().timestamp()

        send_mail(
            "OTP to view your appointments",
            f"Your OTP is {otp}",
            "no-reply@yourdomain.com",
            [value] if "@" in value else []
        )

        return redirect("my_appointments_verify")

    return render(request, "my_appointments_start.html")


def my_appointments_verify(request):
    otp = request.session.get("my_appt_otp")
    value = request.session.get("my_appt_value")

    if not otp or not value:
        return redirect("my_appointments")

    if request.method == "POST":
        if request.POST.get("otp") != otp:
            return render(request, "my_appointments_verify.html", {"error": True})

        appointments = Appointment.objects.filter(
            Q(email=value) | Q(contact_number=value)
        ).order_by("-appointment_date")

        request.session.flush()

        return render(request, "my_appointments_list.html", {
            "appointments": appointments
        })

    return render(request, "my_appointments_verify.html")



from django.shortcuts import render, get_object_or_404
from .models import Appointment

def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'appointment_detail.html', {'appointment': appointment})

from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        body = f"""
New Contact Request

Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}
"""

        # Email to clinic
        send_mail(
            subject=f"Contact Form - {name}",
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["mangalyahomeopathy@gmail.com"],
            fail_silently=True,
        )

        # ✅ Auto reply to patient
        send_mail(
            subject="Thanks for contacting Mangalya Homeopathy",
            message=(
                f"Dear {name},\n\n"
                "Thanks for contacting Mangalya Homeopathy.\n"
                "We have received your message and our team will contact you shortly.\n\n"
                "Regards,\n"
                "Mangalya Homeopathy Clinic\n"
                "Nalasopara West"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

        messages.success(request, "Message sent successfully!")
        return redirect("contact")

    return render(request, "contact.html")


def homeopathic(request):
    return render(request, 'homeopathic.html')


def patient_login(request):
    if request.method == 'POST':
        username = request.POST.get('email_or_mobile')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Fetch all appointments (you can filter by patient if needed)
            appointments = Appointment.objects.filter(patient=user)
            return render(request, 'appointments.html', {'appointments': appointments})
        else:
            messages.error(request, "You are not registered or password is incorrect!")
            return render(request, 'patient_login.html')

    return render(request, 'patient_login.html')


from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages

def careers(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message_body = request.POST.get('message', '')
        resume = request.FILES.get('resume')

        subject = f"Job Application from {name}"
        message = f"""Name: {name}
Email: {email}
Phone: {phone}
Message: {message_body}
"""

        # Use main Gmail account (career@ forwards to mangalyahomeopathy@gmail.com)
        email_msg = EmailMessage(
            subject,
            message,
            'mangalyahomeopathy@gmail.com',  # From
            ['mangalyahomeopathy@gmail.com'],  # Recipient
        )

        # Attach resume if uploaded
        if resume:
            email_msg.attach(resume.name, resume.read(), resume.content_type)

        # Send email safely
        try:
            email_msg.send()
            messages.success(request, "Your application has been submitted successfully!")
        except Exception as e:
            messages.error(request, f"Failed to send email: {e}")
            return redirect('careers')

        return redirect('careers')  # Or a thank-you page

    return render(request, 'career.html')




# yourapp/views.py
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from .models import SocialLanding, BookingLead

def social_landing_slug(request, slug):
    landing = get_object_or_404(SocialLanding, slug=slug)
    image_url = landing.image_url_absolute(request)
    context = {
        'landing': landing,
        'image_url': image_url,
        'clinic_address': 'Mangalya Homeopathy - Nalasopara West',
    }
    return render(request, 'landing/social_media_landing.html', context)


@require_POST
@csrf_protect
def create_booking_lead(request):
    # Accept JSON body or form POST
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body.decode('utf-8') or '{}')
        except Exception:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    else:
        data = request.POST

    name = (data.get('name') or '').strip()
    phone = (data.get('phone') or '').strip()
    email = (data.get('email') or '').strip()
    preferred_date = (data.get('preferred_date') or '').strip()
    message = (data.get('message') or '').strip()
    landing_slug = (data.get('landing_slug') or '').strip()
    utm = data.get('utm') or {}

    if not name or not phone:
        return JsonResponse({'success': False, 'error': 'Name and phone are required.'}, status=400)

    # Save lead
    lead = BookingLead.objects.create(
        name=name,
        phone=phone,
        email=email or None,
        preferred_date=preferred_date,
        message=message,
        landing_slug=landing_slug,
        utm=utm if isinstance(utm, dict) else (json.loads(utm) if utm else {}),
        source='landing' if landing_slug else 'site',
    )

    # Send email notification (best to enqueue in background)
    try:
        from django.core.mail import send_mail
        subject = f"New Booking Lead — {lead.name}"
        body = f"""
New booking lead:

Name: {lead.name}
Phone: {lead.phone}
Email: {lead.email or '-'}
Preferred: {lead.preferred_date or '-'}
Message: {lead.message or '-'}
Landing: {lead.landing_slug or '-'}
Time: {lead.created_at.isoformat()}
UTM: {json.dumps(lead.utm or {})}
"""
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)],
            fail_silently=True,
        )
        lead.notified = True
        lead.save(update_fields=['notified'])
    except Exception:
        # log error in production
        pass

    return JsonResponse({'success': True, 'message': 'Thanks — we received your request.'})

def skin_treatments(request):
    return render( request,"landing/skin-treatments.html")


from django.http import JsonResponse
from datetime import datetime
from .models import Appointment

def get_booked_slots(request):
    date_str = request.GET.get('date')

    if not date_str:
        return JsonResponse({'slots': []})

    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({'slots': []})

    booked_slots = Appointment.objects.filter(
        appointment_date=selected_date
    ).values_list('appointment_time', flat=True)

    # Convert time objects → "HH:MM"
    booked_times = [t.strftime("%H:%M") for t in booked_slots]

    return JsonResponse({'slots': booked_times})




from .models import ClinicHoliday

def get_holidays(request):
    holidays = ClinicHoliday.objects.filter(is_active=True)

    data = {}
    for h in holidays:
        date_str = h.date.strftime("%Y-%m-%d")

        if date_str not in data:
            data[date_str] = []

        data[date_str].append({
            "slot": h.closed_slot,
            "title": h.title
        })

    return JsonResponse({"holidays": data})




from django.http import HttpResponse


@login_required
def dashboard_home(request):
    today = now().date()

    context = {
        "booked_count": Appointment.objects.filter(
            visit_status="booked"
        ).count(),

        "visited_count": Appointment.objects.filter(
            visit_status="visited"
        ).count(),

        "unvisited_count": Appointment.objects.filter(
            visit_status="unvisited"
        ).count(),

        "cancelled_count": Appointment.objects.filter(
            visit_status="cancelled"
        ).count(),

        "today_appointments": Appointment.objects.filter(
            appointment_date=today
        ).count(),

        "total_patients": Patient.objects.count(),
    }

    return render(request, "dashboard.html", context)


from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Appointment

@require_POST
def update_visit_status(request):
    appointment_id = request.POST.get("id")
    status = request.POST.get("status")

    try:
        appt = Appointment.objects.get(id=appointment_id)
        appt.visit_status = status
        appt.save()

        return JsonResponse({"success": True})
    except Appointment.DoesNotExist:
        return JsonResponse({"success": False})


@login_required
def doctor_dashboard(request):
    today = now().date()

    appointments = Appointment.objects.filter(
        appointment_date=today
    ).order_by("appointment_time")

    context = {
        "appointments": appointments,
        "today_total": appointments.count(),
        "visited_today": appointments.filter(
            visit_status="visited"
        ).count(),
        "waiting_today": appointments.filter(
            visit_status="booked"
        ).count(),
        "cancelled_today": appointments.filter(
            visit_status="cancelled"
        ).count(),
    }

    return render(request, "doctor/dashboard.html", context)



# ========================================   PDF ================================
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from .models import Appointment


def download_appointment_pdf(request, booking_id):
    try:
        appointment = Appointment.objects.get(booking_id=booking_id)
    except Appointment.DoesNotExist:
        return HttpResponse("Invalid Booking ID", status=404)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("<b>Mangalya Homeopathy Clinic</b>", styles['Title']))
    elements.append(Spacer(1, 0.4 * inch))

    # Patient Name Handling
    if appointment.patient_type == 'new':
        patient_name = f"{appointment.first_name} {appointment.last_name}"
        mobile = appointment.contact_number
        email = appointment.email
    else:
        patient_name = f"{appointment.patient.first_name} {appointment.patient.last_name}"
        mobile = appointment.patient.contact_number
        email = appointment.patient.email

    # Table Data
    table_data = [
        ["Booking ID", appointment.booking_id],
        ["Patient Name", patient_name],
        ["Mobile Number", mobile],
        ["Email", email],
        ["Appointment Date", str(appointment.appointment_date)],
        ["Appointment Time", appointment.appointment_time.strftime("%I:%M %p")],
        ["Disease(s)", appointment.diseases],
        ["Status", appointment.visit_status.title()],
    ]

    table = Table(table_data, colWidths=[2.5 * inch, 3.5 * inch])

    table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(Paragraph("Thank you for choosing Mangalya Homeopathy.", styles['Normal']))

    doc.build(elements)

    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="Appointment_{appointment.booking_id}.pdf"'

    return response


# ===============================================
def pcodTreatment(request):
    return render(request,"pcod-treatment.html")









    # ===================================
from .models import (
    TestPatient,
    TestAppointment
)


def test_booking(request):

    if request.method == "POST":

        contact_number = request.POST.get(
            'contact_number'
        )

        first_name = request.POST.get(
            'first_name'
        )

        last_name = request.POST.get(
            'last_name'
        )

        dob = request.POST.get(
            'dob'
        )

        gender = request.POST.get(
            'gender'
        )

        email = request.POST.get(
            'email'
        )

        disease = request.POST.get(
            'disease'
        )

        appointment_date = request.POST.get(
            'appointment_date'
        )

        appointment_time = request.POST.get(
            'appointment_time'
        )

        patient = TestPatient.objects.create(

            first_name=first_name,

            last_name=last_name,

            dob=dob,

            gender=gender,

            contact_number=contact_number,

            email=email

        )

        TestAppointment.objects.create(

            patient=patient,

            disease=disease,

            appointment_date=appointment_date,

            appointment_time=appointment_time

        )

    return render(
        request,
        'test_booking.html'
    )

def test_login(request):

    if request.method == "POST":

        contact_number = request.POST.get(
            'contact_number'
        )

        otp = random.randint(1000, 9999)

        request.session['test_otp'] = str(otp)

        request.session[
            'test_contact_number'
        ] = contact_number

        print("TEST OTP:", otp)

        return redirect(
            'test_verify_otp'
        )

    return render(
        request,
        'test_login.html'
    )


def test_verify_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get(
            'otp'
        )

        saved_otp = request.session.get(
            'test_otp'
        )

        if entered_otp == saved_otp:

            contact_number = request.session.get(
                'test_contact_number'
            )

            patients = TestPatient.objects.filter(
                contact_number=contact_number
            )

            # ================= if patient exists =================

            if patients.exists():

                return render(
                    request,
                    'test_patient_cards.html',
                    {
                        'patients': patients
                    }
                )

            # ================= no patient =================

            else:

                return redirect(
                    'test_add_patient'
                )

    return render(
        request,
        'test_verify_otp.html'
    )

def test_patient_cards(request):

    contact_number = request.session.get(
        'test_contact_number'
    )

    patients = TestPatient.objects.filter(
        contact_number=contact_number
    )

    return render(
        request,
        'test_patient_cards.html',
        {
            'patients': patients
        }
    )

def test_add_patient(request):

    contact_number = request.session.get(
        'test_contact_number'
    )

    if request.method == "POST":

        # ================= patient details =================

        first_name = request.POST.get(
            'first_name'
        )

        last_name = request.POST.get(
            'last_name'
        )

        dob = request.POST.get(
            'dob'
        )

        gender = request.POST.get(
            'gender'
        )

        email = request.POST.get(
            'email'
        )

        # ================= appointment details =================

        disease = request.POST.get(
            'disease'
        )

        appointment_date = request.POST.get(
            'appointment_date'
        )

        appointment_time = request.POST.get(
            'appointment_time'
        )

        # ================= create patient =================

        patient = TestPatient.objects.create(

            first_name=first_name,

            last_name=last_name,

            dob=dob,

            gender=gender,

            contact_number=contact_number,

            email=email

        )

        # ================= create appointment =================

        TestAppointment.objects.create(

            patient=patient,

            disease=disease,

            appointment_date=appointment_date,

            appointment_time=appointment_time

        )

        return redirect(
            'test_patient_cards'
        )

    return render(
        request,
        'test_add_patient.html'
    )





