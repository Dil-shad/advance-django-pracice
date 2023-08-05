from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from .forms import ContactUsForm, RegistrationForm, RegistrationFormSeller, RegistrationFormSeller2
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from .models import CustomUser, SellerAdditional
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

from django.core.mail import EmailMessage, send_mail
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from Ecommerceprojct import settings

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages


# def index(request):
#     return render(request, 'index.html')


class Index(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        age = 10
        context_old = super().get_context_data(**kwargs)
        print(context_old)
        context = {'age': age}
        return context
    def get(self, request):
        request.session['test'] = 'testing'
        return super().get(request)

def Contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST['phone']
        if len(phone) < 10 or len(phone) > 10:
            raise ValidationError("Phone number length is not right")
        query = request.POST['query']
        print(name + " " + email + " " + phone + " " + query)
    return render(request, 'contactus.html')


def contactus2(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            if len(query) <= 10:
                form.add_error(
                    'query', 'Query length should be more than 10 characters.')
                return render(request, 'contactus2.html', {'form': form})
            form.save()
            return HttpResponse("Thank You")
        else:
            query = form.cleaned_data.get('query')
            if len(query) <= 10:
                form.add_error(
                    '__all__', 'Query length should be more than 10 characters.')
            return render(request, 'contactus2.html', {'form': form})
    else:
        form = ContactUsForm()
    return render(request, 'contactus2.html', {'form': form})


class ContactUs(FormView):
    form_class = ContactUsForm
    template_name = 'contactus2.html'
    # success_url = '/' #hardcoded url
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        query = form.cleaned_data.get('query')
        if len(query) <= 10:
            form.add_error(
                'query', 'Query length should be more than 10 characters.')
            return render(self.request, 'contactus2.html', {'form': form})
        form.save()
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        query = form.cleaned_data.get('query')
        if len(query) <= 10:
            form.add_error(
                '__all__', 'Query length should be more than 10 characters.')
        response = super().form_invalid(form)
        return response


# class RegisterViewSeller(CreateView):
#     template_name = 'registerseller.html'
#     form_class = RegistrationFormSeller
#     success_url = reverse_lazy('index')

    # def post(self, request, *args, **kwargs):
    #     response = super().post(request, *args, **kwargs)
    #     if response.status_code == 302:
    #         gst = request.POST.get('gst')
    #         warehouse_location = request.POST.get('warehouse_location')
    #         user = CustomUser.objects.get(email = request.POST.get('email'))
    #         s_add = SellerAdditional.objects.create(user = user, gst = gst, warehouse_location = warehouse_location)
    #         return response
    #     else:
    #         return response
    # ---------------OR-------------
    # def form_valid(self, form):
    #     # Call the parent form_valid method to save the form data
    #     response = super().form_valid(form)

    #     # Extract form data from cleaned_data
    #     gst = form.cleaned_data['gst']
    #     warehouse_location = form.cleaned_data['warehouse_location']
    #     email = form.cleaned_data['email']

    #     # Retrieve or create the CustomUser instance based on the email
    #     user, _ = CustomUser.objects.get_or_create(email=email)

    #     # Create the SellerAdditional object and associate it with the user
    #     s_add = SellerAdditional.objects.create(user=user, gst=gst, warehouse_location=warehouse_location)

    #     # Return the response
    #     return response


class RegisterView(CreateView):
    template_name = 'registerbasicuser.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        # form = RegistrationForm(request.POST)
        user_email = request.POST.get('email')
        try:
            existing_user = CustomUser.objects.get(email=user_email)
            if (existing_user.is_active == False):
                existing_user.delete()
        except:
            pass
        response = super().post(request, *args, **kwargs)
        if response.status_code == 302:
            # 302 is http response sttus code
            user = CustomUser.objects.get(email=user_email)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)  # www.wondershop.in:8000
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            print(message)
            to_email = user_email
            # form = RegistrationForm(request.POST)   # here we are again calling all its validations
            form = self.get_form()
            try:
                send_mail(
                    subject=mail_subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[to_email],
                    # if it fails due to some error or email id then it get silenced without affecting others
                    fail_silently=False,
                )
                messages.success(
                    request, "link has been sent to your email id. please check your inbox and if its not there check your spam as well.")
                return self.render_to_response({'form': form})
            except:
                form.add_error('', 'Error Occured In Sending Mail, Try Again')
                messages.error(
                    request, "Error Occured In Sending Mail, Try Again")
                return self.render_to_response({'form': form})
        else:
            return response


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Successfully Logged In")
        return redirect(reverse_lazy('index'))
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid or your account is already Verified! Try To Login')


class LoginViewUser(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy('index')


class LogoutViewUser(LogoutView):
    # Override the success_url attribute
    success_url = reverse_lazy('index')


def testsession(request):
    if request.session.get('test', False):
        print(request.session['test'])

    request.session.set_expiry(60)
    request.session['test'] = 'testing'
    request.session['test2'] = 'testing2'
    return render(request, 'sessiontesting.html')


def example_view(request):
    context = {
        'user_name': 'John',  # Replace this with the actual user's name
    }
    return render(request, 'example_template.html', context)
