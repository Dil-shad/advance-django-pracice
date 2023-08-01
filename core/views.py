from django.shortcuts import render
from django.views.generic import TemplateView, FormView,CreateView
from django.contrib.auth.views import LoginView , LogoutView
from django.core.exceptions import ValidationError
from .forms import ContactUsForm,RegistrationForm,RegistrationFormSeller,RegistrationFormSeller2
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from .models import CustomUser,SellerAdditional
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


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
    #success_url = '/' #hardcoded url
    success_url= reverse_lazy('core:index')

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
#     success_url = reverse_lazy('core:index')

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
    #---------------OR-------------
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
    success_url = reverse_lazy('core:index')
    

class LoginViewUser(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy('core:index')


    
# class RegisterViewSeller(LoginRequiredMixin,CreateView):
#     template_name = 'registerseller2.html' 
#     form_class = RegistrationFormSeller2
#     success_url = reverse_lazy('core:index')
    
#     def form_valid(self, form):
#         user = self.request.user
#         user.type.append(user.Types.SELLER)
#         user.save()
#         form.instance.user = self.request.user
#         return super().form_valid(form)
    
     
class LogoutViewUser(LogoutView):
    success_url=reverse_lazy('core:index')
    
        
          
    
    