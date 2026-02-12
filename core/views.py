from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from .models import User, Flat, MaintenenceBill
from .decorators import admin_required

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user:
            if user.is_active:
                login(request, user)

                if user.role == 'ADMIN':
                    return redirect('admin_dashboard')
                elif user.role == 'OWNER':
                    return redirect('owner_dashboard')
                elif user.role == 'TENANT':
                    return redirect('tenant_dashboard')
            else:
                messages.error(request, "Account is inactive")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


from django.contrib import messages
from .models import Society , Flat , MaintenenceBill,User
import string,secrets

@admin_required
def admin_dashboard(request):

    if request.method == 'POST' and 'email' in request.POST:
        email = request.POST.get('email')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists')
        else:
            password = ''.join(
                secrets.choice(string.ascii_letters + string.digits)
                for _ in range(8)
            )

            User.objects.create_user(
                email=email,
                username=email,
                password=password,
                role='OWNER',
                is_active=True
            )

            messages.success(request, 'Owner created successfully')


    elif request.method == 'POST' and 'society_name' in request.POST:
        name = request.POST.get('society_name')
        address = request.POST.get('address')

        Society.objects.create(name=name, address=address)
        messages.success(request, 'Society created successfully')

    
    elif request.method == 'POST' and 'flat_number' in request.POST:
        flat_number = request.POST.get('flat_number')
        owner_id = request.POST.get('owner')
        society_id = request.POST.get('society')

        owner = User.objects.get(id=owner_id)
        society = Society.objects.get(id=society_id)

        Flat.objects.create(
            flat_number=flat_number,
            owner=owner,
            society=society
        )

        messages.success(request, 'Flat created successfully')

    elif request.method == 'POST' and 'month' in request.POST:
        flat_id = request.POST.get('flat')
        month = request.POST.get('month')
        amount = request.POST.get('amount')

        flat = Flat.objects.get(id=flat_id)

        MaintenenceBill.objects.create(
            flat=flat,
            month=month,
            amount=amount
        )



    owners = User.objects.filter(role='OWNER')
    societies = Society.objects.all()
    flats = Flat.objects.all()

    return render(
        request,
        'admin_dashboard.html',
        {
            'owners': owners,
            'societies': societies,
            'flats': flats
        }
    )

import secrets
import string
from django.core.mail import send_mail
from django.contrib import messages

def create_owner(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        password = ''.join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(10)
        )


        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            role='OWNER',
            is_active=True
        )

        print("Send Mail Successfully")

        send_mail(
            subject='Owner Login Credentials',
            message=f"Email: {email}\nPassword: {password}",
            from_email='gauravadmin@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, 'Owner created successfully')

    return redirect('admin_dashboard')

def create_tenant(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        flat_id = request.POST.get('flat')
        move_in_date = request.POST.get('move_in_date')

        password = ''.join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(10)
        )

        if User.objects.filter(email=email).exists():
            messages.error(request, 'User already exists')
            return redirect('admin_dashboard')

    
        tenant = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            role='TENANT',
            is_active=True
        )

        
        tenant_profile = TenantProfile.objects.create(
            user=tenant,
            move_in_date=move_in_date
        )

        
        flat = Flat.objects.get(id=flat_id)
        flat.tenant = tenant
        flat.save()

        send_mail(
            subject='Tenant Login Credentials',
            message=f"Email: {email}\nPassword: {password}",
            from_email='gauravadmin@admin.com',
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, 'Tenant created successfully')

    return redirect('admin_dashboard')



@login_required
def owner_dashboard(request):
    if request.user.role != 'OWNER':
        return redirect('login')

    flats = Flat.objects.filter(owner=request.user)
    bills = MaintenenceBill.objects.filter(flat__owner=request.user)

    return render(request, 'owner_dashboard.html', {
        'flats': flats,
        'bills': bills
    })


from .models import TenantProfile, MaintenenceBill ,Society

@login_required
def tenant_dashboard(request):

    if request.user.role != 'TENANT':
        return redirect('login')

    tenant_profile = TenantProfile.objects.filter(user=request.user).first()
    flat = Flat.objects.filter(tenant=request.user).first()
    bills = MaintenenceBill.objects.filter(flat=flat) if flat else None

    return render(request, 'tenant_dashboard.html', {
        'tenant_profile': tenant_profile,
        'flat': flat,
        'bills': bills
    })



@admin_required
def create_flat(request):
    if request.method == 'POST':
        Flat.objects.create(
            flat_number=request.POST.get('flat_number'),
            owner_id=request.POST.get('owner'),
            society_id=request.POST.get('society')
        )
        
    return redirect('admin_dashboard')



@admin_required
def create_bill(request):
    flats = Flat.objects.filter(tenant__isnull=False)
    tenants = User.objects.filter(role='TENANT')

    if request.method == 'POST':
        flat_id = request.POST.get('flat')
        month = request.POST.get('month')
        amount = request.POST.get('amount')

        if flat_id and month and amount:
            MaintenenceBill.objects.create(
                flat_id=flat_id,
                month=month,
                amount=amount,
                status='Pending'
            )
            
        else:
            messages.error(request, "Please fill all fields")

        return redirect('admin_dashboard')

    return render(request, 'create_bill.html', {'flats': flats,'tenants':tenants})





def login_redirect(user):
    if user.role == 'ADMIN':
        return 'admin_dashboard'
    elif user.role == 'OWNER':
        return 'owner_dashboard'
    elif user.role == 'TENANT':
        return 'tenant_dashboard'

def logout_view(request):
    list(messages.get_messages(request))
    logout(request)
    request.session.flush()
    return redirect ('login')



@login_required
def owner_bills(request):
    bills = MaintenenceBill.objects.filter(owner=request.user)
    return render(request, 'owner_bills.html', {'bills': bills})
