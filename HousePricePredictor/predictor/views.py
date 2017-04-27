from django.http import HttpResponse
from predictor.models import HouseData
from predictor.forms import HouseForm
import predictor.prediction_script as p
from django.shortcuts import render
from django.http import HttpResponseRedirect
import csv
import os


# Create your views here.


def index(request):
    # if this is a POST request we need to process the form data

    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = HouseForm(request.POST)
        print(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            # redirect to a new URL:
            return render(request, 'index.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        house_data = HouseData.objects.all()
        p.build_model(house_data)
        fields = HouseData._meta.get_fields()
        form = HouseForm()

    return render(request, 'index.html', {'form': form})


def show_all_data(request):
    house_data = list(HouseData.objects.all().values())
    prediction_model = p.build_model(house_data)
    return HttpResponse(prediction_model)


def delete_data(request):
    is_deleted = HouseData.objects.all().delete()
    return HttpResponse(is_deleted)


def load_data(request):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(base_dir, 'Nashville_housing_data.csv')

    with open(path) as f:
        reader = csv.reader(f)

        added, updated = 0, 0
        for idx, row in enumerate(reader):
            if idx > 0:
                _, created = HouseData.objects.get_or_create(
                    no=int(row[0]),
                    land_use=row[1],
                    sold_as_vacant=row[2],
                    city=row[3],
                    square_footage=row[4],
                    tax_district=row[5],
                    neighborhood=int(row[6]),
                    land_value=int(row[7]),
                    sales_price=int(row[8])
                )
                if not created:
                    updated += 1
                else:
                    added += 1

    return HttpResponse(str(added) + ':' + str(updated))
