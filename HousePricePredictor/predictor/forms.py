from django import forms
from predictor.models import HouseData

# Form data for web page
class HouseForm(forms.Form):
    land_use = forms.ChoiceField(label='',
                                 required=True,
                                 choices=[('', 'Land Use')] + list(
                                     HouseData.objects.values_list('land_use', 'land_use').distinct()))

    sold_as_vacant = forms.ChoiceField(label='',
                                       required=True,
                                       choices=[('', 'Sold as Vacant')] + list(
                                           HouseData.objects.values_list('sold_as_vacant',
                                                                         'sold_as_vacant').distinct()))

    city = forms.ChoiceField(label='',
                             required=True,
                             choices=[('', 'City')] + list(HouseData.objects.values_list('city', 'city').distinct()))

    square_footage = forms.IntegerField(label='',
                                        widget=forms.TextInput(attrs={'placeholder': 'square footage'}),
                                        required=True,
                                        min_value=0,
                                        max_value=1000000)

    tax_district = forms.ChoiceField(label='',
                                     required=True,
                                     choices=[('', 'Tax District')] + list(
                                         HouseData.objects.values_list('tax_district', 'tax_district').distinct()))

    neighborhood = forms.ChoiceField(label='',
                                     required=True,
                                     choices=[('', 'Neighborhood')] + list(HouseData.objects.values_list('neighborhood',
                                                                                                         'neighborhood').distinct().order_by(
                                         'neighborhood')))

    land_value = forms.IntegerField(required=True,
                                    label='',
                                    min_value=0,
                                    max_value=1000000,
                                    widget=forms.TextInput(attrs={'placeholder': 'Land value'}))

    def __init__(self, *args, **kwargs):
        super(HouseForm, self).__init__(*args, **kwargs)
