import csv
import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Sum
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.edit import FormMixin

from EqpMS.utils import render_to_pdf
# from action.models import TreatmentAsset, Treatment
from inventory.forms import AssetCategoryForm, AssetForm, AssetUnitForm, AssetFilterForm
from inventory.models import AssetCategory, Asset, AssetUnit, Inventory
from manager.models import Customer


# Create your views here.

# AssetCategory views
class AssetCategoryAll(LoginRequiredMixin, ListView):
    template_name = 'inventory/assetcategory/index.html'
    login_url = 'manager:login'
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assetcategories'] = AssetCategory.objects.order_by('id')
        return context


class AssetCategoryNew(LoginRequiredMixin, CreateView):
    model = AssetCategory
    template_name = 'inventory/assetcategory/create.html'
    form_class = AssetCategoryForm
    login_url = 'manager:login'
    success_url = reverse_lazy('inventory:ass_cat_all')


class AssetCategoryUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'inventory/assetcategory/edit.html'
    form_class = AssetCategoryForm
    login_url = 'manager:login'
    model = AssetCategory
    success_url = reverse_lazy('inventory:ass_cat_all')


# AssetUnit views
class AssetUnitAll(LoginRequiredMixin, ListView):
    template_name = 'inventory/assetunit/index.html'
    login_url = 'manager:login'
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assetunits'] = AssetUnit.objects.order_by('name')
        return context


class AssetUnitNew(LoginRequiredMixin, CreateView):
    model = AssetCategory
    template_name = 'inventory/assetunit/create.html'
    form_class = AssetUnitForm
    login_url = 'manager:login'
    success_url = reverse_lazy('inventory:ass_unt_all')


class AssetUnitUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'inventory/assetunit/edit.html'
    form_class = AssetUnitForm
    login_url = 'manager:login'
    model = AssetUnit
    success_url = reverse_lazy('inventory:ass_unt_all')


# Asset views
class AssetAll(LoginRequiredMixin, ListView):
    template_name = 'inventory/asset/overview.html'
    login_url = 'manager:login'
    model = Asset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = AssetCategory.objects.order_by('id')
        context['assets'] = Asset.objects.order_by('name')
        context['asset_total'] = Asset.objects.all().count()
        return context


class AssetNew(LoginRequiredMixin, CreateView):
    model = Asset
    template_name = 'inventory/asset/create.html'
    form_class = AssetForm
    login_url = 'manager:login'
    success_url = reverse_lazy('inventory:asset_all')


class AssetUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'inventory/asset/edit.html'
    form_class = AssetForm
    login_url = 'manager:login'
    model = Asset
    success_url = reverse_lazy('inventory:asset_all')


class AssetView(LoginRequiredMixin, DetailView):
    queryset = Asset.objects.select_related('category')
    template_name = 'inventory/asset/single.html'
    context_object_name = 'asset'
    login_url = 'manager:login'


def inventory_overview(request):
    category = request.GET.get('category')
    asset_name = request.GET.get('asset_name')

    assets = Asset.objects.all().order_by('category_id')
    if category:
        if category != "0":
            assets = assets.filter(category_id=category)
    if asset_name:
        assets = assets.filter(name__contains=asset_name)

    # InventoryTmp.objects.all().delete()

    context = {
        # 'customers': Customer.objects.all(),
        'categories': AssetCategory.objects.order_by('id'),
        # 'inventories': InventoryTmp.objects.all(),
    }

    return render(request, 'inventory/inv/overview.html', context)


def inventory_view_pdf(request):
    data = {
        # 'inventories': InventoryTmp.objects.all(),
    }
    pdf = render_to_pdf('PDFs/overview.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def inventory_view_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    fn = "inventory_" + datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".csv"
    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Disposition":
                'attachment; filename=' + fn
        },
    )

    writer = csv.writer(response)
    # for inv in InventoryTmp.objects.all():
    #     writer.writerow([
    #         inv.category_name,
    #         inv.asset_name,
    #         inv.timeI,
    #         inv.input,
    #         inv.timeO,
    #         inv.output,
    #         inv.stock
    #     ])
        # writer.writerow(["First row", "Foo", "Bar", "Baz"])
        # writer.writerow(["Second row", "A", "B", "C", '"Testing"', "Here's a quote"])

    return response


