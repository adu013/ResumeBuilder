import io

from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, UserProfileForm, EditProfileForm, UserJobExperienceFormSet
from .models import UserProfile, UserJobExperience
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm


def index(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'resume/index.html')
    else:
        all_profiles = UserProfile.objects.all().filter(user=request.user)
        all_exp = UserJobExperience.objects.all().filter(user=request.user)
        context = {'all_profiles': all_profiles, 'all_exp': all_exp}
        return render(request, 'resume/index.html', context=context)
    return render(request, 'resume/index.html')


'''
def index(request):
    all_profiles = UserProfile.objects.all().filter()
    all_exp = UserJobExperience.objects.all()
    context = {'all_profiles': all_profiles, 'all_exp': all_exp}
    return render(request, 'resume/index.html', context=context)
'''

'''
class IndexView(View):
    template_name = 'resume/index.html'

    def get(self, request):
        form = UserProfileForm
        profile = UserProfile.objects.all()
        return render(request, self.template_name, {'profile': profile})
'''


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('resume:index')
            else:
                return render(request, 'resume/login.html', {'error_message': 'Your account has been deactivated'})
        else:
            return render(request, 'resume/login', {'error_message': 'Either your username or password is wrong'})
    return render(request, 'resume/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {"form": form}
    return render(request, 'resume/login.html', context)


class UserFormView(View):
    form_class = UserForm
    template_name = 'resume/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # Cleaned normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    # request.user.username
                    return redirect('resume:index')

        return render(request, self.template_name, {'form': form})


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'resume/profile.html')
    else:
        all_profiles = UserProfile.objects.all().filter(user=request.user)
        all_exp = UserJobExperience.objects.all().filter(user=request.user)
        context = {'all_profiles': all_profiles, 'all_exp': all_exp}
        return render(request, 'resume/profile.html', context=context)
    return render(request, 'resume/profile.html')


'''
def profile(request):
    args = {'user': request.user}
    return render(request, 'resume/profile.html', args)
'''


def edit_profile(request):
    print(request.user)

    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        form2 = UserProfileForm(request.POST, instance=profile)
        formset = UserJobExperienceFormSet(request.POST, request.user)
        
        if form.is_valid() and form2.is_valid() and formset.is_valid():
            form.save()
            form2.save()
            # Saving multiple data in Job Experience Section
            for fset in formset:
                # Extract items from each forms
                company_name = fset.cleaned_data.get('company_name')
                duration = fset.cleaned_data.get('duration')
                designation = fset.cleaned_data.get('designation')
                contribution = fset.cleaned_data.get('contribution')

                # Saving
                UserJobExperience(
                    user=request.user,
                    company_name=company_name,
                    duration=duration,
                    designation=designation,
                    contribution=contribution
                ).save()

            return redirect('/resume/profile')
    else:
        form = EditProfileForm(instance=request.user)
        form2 = UserProfileForm(instance=profile)
        formset = UserJobExperienceFormSet()
        formset.user = request.user
        context = {'form': form, 'form2': form2, 'formset': formset}
        return render(request, 'resume/edit_profile.html', context)


'''
def edit_profile(request):
    print(request.user)

    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        form2 = UserProfileForm(request.POST, instance=profile)

        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect('/resume/profile')
    else:
        form = EditProfileForm(instance=request.user)
        form2 = UserProfileForm(instance=profile)

        context = {'form': form, 'form2': form2}
        return render(request, 'resume/edit_profile.html', context)
'''


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('resume/profile')
        else:
            return redirect('resume/change-password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return redirect(request, 'resume/profile', args)


# Views to export data to pdf
def create_resume(request):
    all_profiles = UserProfile.objects.all().filter(user=request.user)
    all_exp = UserJobExperience.objects.all().filter(user=request.user)
    context = {'all_profiles': all_profiles, 'all_exp': all_exp}

    pdf_name = "resume/static/resume/files/resume.pdf"
    c = canvas.Canvas(pdf_name, pagesize=letter)
    # canvas.setLineWidth(.3)
    # canvas.setFont('Helvetica', 12)

    c.drawString(20, 750, "Resume")
    c.drawString(20, 700, "Name: " + request.user.first_name + " " + request.user.last_name)
    c.drawString(20, 685, "Email: " + request.user.email)

    '''
    for pro in all_profiles:
        summary = pro.summary
        phone = pro.phone
        alt_phone = pro.alt_phone
        alt_email = pro.alt_email
        experience = pro.experience
        current_ctc = pro.current_ctc
        expected_ctc = pro.expected_ctc

        c.drawString(20, 670, summary)
        c.drawString(20, 655, phone)
        c.drawString(20, 640, alt_phone)
        c.drawString(20, 625, alt_email)
        c.drawString(20, 610, experience)
        c.drawString(20, 595, current_ctc)
        c.drawString(20, 580, expected_ctc)
    '''
    c.save()

    return render(request, 'resume/download.html', {'context': context})


def view_resume(request):
    return render(request, 'files/resume.pdf')
