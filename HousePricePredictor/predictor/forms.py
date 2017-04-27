from django import forms
from predictor.models import HouseData


class HouseForm(forms.Form):
    land_use = forms.ChoiceField(label='land use',
                                 required=True,
                                 choices=list(HouseData.objects.values_list('land_use', 'land_use').distinct()))

    sold_as_vacant = forms.ChoiceField(label='sold as vacant',
                                       required=True,
                                       choices=list(HouseData.objects.values_list('sold_as_vacant', 'sold_as_vacant').distinct()))

    city = forms.ChoiceField(label='City',
                             required=True,
                             choices=list(HouseData.objects.values_list('city', 'city').distinct()))

    square_footage = forms.IntegerField(label='square footage', required=True, min_value=0, max_value=100000)

    tax_district = forms.ChoiceField(label='tax district',
                                     required=True,
                                     choices=list(HouseData.objects.values_list('tax_district', 'tax_district').distinct()))

    neighborhood = forms.ChoiceField(label='neighborhood',
                                     required=True,
                                     choices=list(HouseData.objects.values_list('neighborhood', 'neighborhood').distinct()))

    land_value = forms.IntegerField(required=True, label='land value', min_value=0, max_value=100000)

    def __init__(self, *args, **kwargs):

        super(HouseForm, self).__init__(*args, **kwargs)



