from django import forms
from inventory.models import AssetCategory, Asset, AssetUnit, Inventory
from manager.models import Customer


class AssetCategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=32,
        label='Loại Vật tư Thiết-bị:',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Loại Vật-tư'})
    )

    class Meta:
        model = AssetCategory
        fields = '__all__'


class AssetUnitForm(forms.ModelForm):
    name = forms.CharField(
        max_length=32,
        label='Đơn vị tính (Vật-tư Thiết-bị):',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ĐVT Vật-tư'})
    )

    class Meta:
        model = AssetUnit
        fields = '__all__'


class AssetForm(forms.ModelForm):
    code = forms.CharField(
        max_length=32,
        label='Mã số [*]:',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mã số'})
    )
    name = forms.CharField(
        max_length=80,
        label='Vật-tư Thiết-bị [*]:',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vật-tư Thiết-bị'})
    )
    customer = forms.ModelChoiceField(
        Customer.objects.all(),
        label='Người sử dụng:',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        AssetCategory.objects.all(),
        label='Phân loại:',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    thumb = forms.ImageField(
        required=False,
        label='Hình ảnh:',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Asset
        fields = ('code', 'name', 'category', 'customer', 'thumb')


class AssetFilterForm(forms.Form):
    category: forms.CharField()


"""
class InventoryForm(forms.ModelForm):
    supplier = forms.ModelChoiceField(
        Supplier.objects.all(),
        label='Nhà cung cấp:',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    asset = forms.ModelChoiceField(
        Asset.objects.all(),
        label='Vật-tư Thiết-bị:',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantityIO = forms.IntegerField(
        label='Số lượng:',
        widget=forms.NumberInput()
    )

    class Meta:
        model = Purchase
        fields = ('supplier',)


class DeliverForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        Customer.objects.all(),
        label='Khách hàng:',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    asset = forms.ModelChoiceField(
        # Asset.objects.all(),
        Asset.objects.filter(inventory__quantityIO__gt=0).order_by('name').distinct(),
        label='Vật-tư Thiết-bị:',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantityIO = forms.IntegerField(
        label='Số lượng:',
        widget=forms.NumberInput()
    )

    class Meta:
        model = Deliver
        fields = ('customer',)


class DeliverFilterForm(forms.Form):
    category: forms.CharField()
"""
