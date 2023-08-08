from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView,ListView,DeleteView,UpdateView,DeleteView,DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from .forms import ContactUsForm, RegistrationForm, RegistrationFormSeller, RegistrationFormSeller2,CartForm
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from .models import CustomUser, SellerAdditional, Product
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
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

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import JsonResponse,HttpResponse


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

    request.session.set_expiry(1)
    request.session['test'] = 'testing'
    request.session['test2'] = 'testing2'
    return render(request, 'sessiontesting.html')


def example_view(request):
    context = {
        'user_name': 'John',  
    }
    return render(request, 'example_template.html', context)
# ----------------------------------------------------------------#


class ProductListView(ListView):
    model = Product
    template_name = "listproducts.html"
    context_object_name='product'
    paginate_by = 2
    



def listProducts(request):
    ordering = request.GET.get('ordering', "")
    search = request.GET.get('search', "")
    price = request.GET.get('price', "")
    product_per_page = request.GET.get('itemsPer')
    if not product_per_page:
        product_per_page = 4

    if search:
        product = Product.objects.filter(Q(product_name__icontains=search) | Q(brand__icontains=search))
    else:
        product = Product.objects.all()

    if ordering:
        product = product.order_by(ordering)

    if price:
        product = product.filter(price__lte=price)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(product, product_per_page)
    try:
        product_subset = paginator.page(page)
    except EmptyPage:
        product_subset = paginator.page(paginator.num_pages)

    context = {
        "product": product_subset,
        'page_obj': product_subset,
        'is_paginated': product_subset.has_other_pages(),
        'paginator': paginator
    }

    return render(request, "listproducts.html", context)


def suggestionApi(request):
    if 'term' in request.GET:
        search = request.GET.get('term')
        qs = Product.objects.filter(Q(product_name__icontains=search))[0:10]
        # print(list(qs.values()))
        # print(json.dumps(list(qs.values()), cls = DjangoJSONEncoder))
        titles = [product.product_name for product in qs]
        #print(titles)
        if len(qs)<10:
            remaining_count = 10 - len(qs)
            qs2 = Product.objects.filter(Q(brand__icontains=search))[0:remaining_count]
            titles.extend(product.brand for product in qs2)
        return JsonResponse(titles, safe=False)      # [1,2,3,4] ---> "[1,2,3,4]"   queryset ---> serialize into list or dict format ---> json format using json.dumps with a DjangoJSONEncoder(encoder to handle datetime like objects)



def listProductsApi(request):
    # print(Product.objects.all())
    # print(Product.objects.values())
    #result = json.dumps(list(Product.objects.values()), sort_keys=False, indent=0, cls=DjangoJSONEncoder)   # will return error if you have a datetime object as it is not jsonserializable  so thats why use DjangoJSONEncoder, indent to beautify and sort_keys to sort keys
    #print(type(result))    #str type  
    #print(result)
    result = list(Product.objects.values())          # will work like passing queryset as a context data if used by a template
    #print(result)
    #return render(request, "firstapp/listproducts.html", {"product":result})
    return JsonResponse(result, safe=False) 
    
    
    
    
    
class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = "productdetail.html"



@login_required
def addToCart(request, id):
    try:
        cart = Cart.objects.get(user = request.user)
        try:
            product = Product.objects.get(product_id = id)
            try:
                productincart = ProductInCart.objects.get(cart = cart, product = product)
                productincart.quantity = productincart.quantity + 1
                productincart.save()
                messages.success(request, "Successfully added to cart")
                return redirect(reverse_lazy("displaycart"))
            except:
                productincart = ProductInCart.objects.create(cart = cart, product = product, quantity=1)
                messages.success(request, "Successfully added to cart")
                return redirect(reverse_lazy("displaycart"))
        except:
            messages.error(request, "Product can not be found")
            return redirect(reverse_lazy('listproducts'))
    except:
        
        cart = Cart.objects.create(user = request.user)
        try:
            product = Product.objects.get(product_id = id)
            productincart = ProductInCart.objects.create(cart = cart, product = product, quantity = 1)
            messages.success(request, "Successfully added to cart")
            return redirect(reverse_lazy("displaycart"))
        except:
            messages.error(request, "Error in adding to cart. Please try again")
            return redirect(reverse_lazy('listproducts'))
        
        
class DisplayCart(LoginRequiredMixin, ListView):
    model = ProductInCart
    template_name = "displaycart.html"
    context_object_name = "cart"

    def get_queryset(self):
        queryset = ProductInCart.objects.filter(cart = self.request.user.cart)
        return queryset
    
    
class UpdateCart(LoginRequiredMixin, UpdateView):
    model = ProductInCart
    form_class = CartForm
    success_url = reverse_lazy("displaycart")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 302:
            if int(request.POST.get("quantity")) == 0:
                productincart = self.get_object()
                productincart.delete()
            return response
        else:
            messages.error(request, "error in quantity")
            return redirect(reverse_lazy("displaycart"))

class DeleteFromCart(LoginRequiredMixin, DeleteView):
    model = ProductInCart
    success_url = reverse_lazy("displaycart")  
 