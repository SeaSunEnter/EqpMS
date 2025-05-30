import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, resolve_url, reverse
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, logout
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView

from inventory.models import Asset
from manager.forms import RegistrationForm, UserUpdateForm, LoginForm, SetPasswordForm
from manager.forms import EmployeeForm, DepartmentForm, CustomerForm, CustomerFilterForm
from manager.models import LoginLogs, Employee, Department, Customer


# Create your views here.

class Index(TemplateView):
    template_name = 'manager/home/home.html'


# Authentication
class Register(CreateView):
    model = get_user_model()
    form_class = RegistrationForm
    template_name = 'manager/registrations/register.html'
    success_url = reverse_lazy('manager:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = LoginLogs.objects.all()
        return context


class LoginViewer(LoginView):
    model = get_user_model()
    form_class = LoginForm
    template_name = 'manager/registrations/login.html'

    def get_success_url(self):
        if self.request.user.is_authenticated:
            cur_user = self.request.user
            LoginLogs.objects.create(user=cur_user)

        url = resolve_url('manager:dashboard')
        return url


class LogoutView(View):

    def get(self, request):
        logout(self.request)
        return redirect('manager:login', permanent=True)


class UserUpdate(UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'manager/registrations/user_update.html'

    def get_success_url(self):
        url = resolve_url('manager:dashboard')
        return url


@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('manager:login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'manager/registrations/user_pass_change.html', {'form': form})


# Main Board
class Dashboard(LoginRequiredMixin, ListView):
    template_name = 'manager/dashboard/index.html'
    model = get_user_model()
    login_url = 'manager:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_total'] = Employee.objects.all().count()
        context['department_total'] = Department.objects.all().count()
        context['departments'] = Department.objects.all()
        context['admin_count'] = get_user_model().objects.all().count()
        context['customers'] = Customer.objects.order_by('-id')[:5]
        context['customer_total'] = Customer.objects.filter(deleted=False).count()
        context['assets'] = Asset.objects.order_by('-id')[:5]
        context['assets_total'] = Asset.objects.all().count()
        context['workers'] = Employee.objects.order_by('id')

        return context


# Employee's Controller
class EmployeeNew(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'manager/employee/create.html'
    login_url = 'manager:login'
    redirect_field_name = 'redirect:'


class EmployeeAll(LoginRequiredMixin, ListView):
    template_name = 'manager/employee/overview.html'
    model = Employee
    login_url = 'manager:login'
    context_object_name = 'employees'
    paginate_by = 5


class EmployeeView(LoginRequiredMixin, DetailView):
    queryset = Employee.objects.select_related('department')
    template_name = 'manager/employee/single.html'
    context_object_name = 'employee'
    login_url = 'manager:login'


"""
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    try:
      query = Kin.objects.get(employee=self.object.pk)
      context["kin"] = query
      return context
    except ObjectDoesNotExist:
      return context
"""


class EmployeeUpdate(LoginRequiredMixin, UpdateView):
    model = Employee
    template_name = 'manager/employee/edit.html'
    form_class = EmployeeForm
    login_url = 'manager:login'

    # success_url = reverse_lazy('manager:employee_all')
    def get_success_url(self):
        return reverse('manager:employee_view', kwargs={'pk': self.kwargs['pk']})


class EmployeeDelete(LoginRequiredMixin, DeleteView):
    pass

# Department views

class DepartmentAll(LoginRequiredMixin, ListView):
    template_name = 'manager/department/index.html'
    login_url = 'manager:login'
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_count'] = get_user_model().objects.all().count()
        context['departments'] = Department.objects.order_by('id')
        return context


"""
  def get_queryset(self):
    queryset = Employee.objects.filter(department=self.kwargs['pk'])
    return queryset
"""


class DepartmentNew(LoginRequiredMixin, CreateView):
    template_name = 'manager/department/create.html'
    model = Department
    form_class = DepartmentForm
    login_url = 'manager:login'
    success_url = reverse_lazy('manager:dept_all')


class DepartmentUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'manager/department/edit.html'
    model = Department
    form_class = DepartmentForm
    login_url = 'manager:login'
    success_url = reverse_lazy('manager:dept_all')


# Customer's Controller
def customer_overview(request):
    mobile = request.GET.get('mobile')
    fname = request.GET.get('fname')
    customers = Customer.objects.filter(deleted=False)
    if mobile:
        customers = customers.filter(mobile__contains=mobile)
    if fname:
        customers = customers.filter(fullname__contains=fname)
    context = {
        'cust_total': Customer.objects.filter(deleted=False).count(),
        'cust_lookup': customers.count(),
        'form': CustomerFilterForm(),
        'customers': customers.filter(deleted=False).order_by('-id'),
        # 'operating': Operating.objects.all().distinct()
    }

    return render(request, 'manager/customer/overview.html', context)


class CustomerAll(LoginRequiredMixin, ListView):
    template_name = 'manager/customer/index.html'
    model = Customer
    login_url = 'manager:login'

    # context_object_name = 'customers'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.filter(deleted=False)
        # context['treatments'] = Treatment.objects.all().distinct()
        return context

    paginate_by = 10


class CustomerNew(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'manager/customer/create.html'
    login_url = 'manager:login'
    redirect_field_name = 'redirect:'

    success_url = reverse_lazy('manager:customer_overview')


class CustomerView(LoginRequiredMixin, DetailView):
    queryset = Customer.objects.select_related('department')
    template_name = 'manager/customer/single.html'
    context_object_name = 'customer'
    login_url = 'manager:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_pk = self.kwargs['pk']
        context['assets'] = Asset.objects.filter(customer_id=customer_pk)

        # cur_inv = None
        # for inv in Invoice.objects.all():
        #     if inv.customer_id == customer_pk:
        #         cur_inv = inv.id
        #         break
        # context['invoice_id'] = cur_inv

        return context


class CustomerUpdate(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'manager/customer/edit.html'
    form_class = CustomerForm
    login_url = 'manager:login'

    def get_success_url(self):
        return reverse('manager:customer_view', kwargs={'pk': self.kwargs['pk']})


class CustomerDelete(LoginRequiredMixin, DeleteView):
    pass


