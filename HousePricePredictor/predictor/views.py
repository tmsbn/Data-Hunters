from django.http import HttpResponse
from predictor.models import HouseData
from predictor.forms import HouseForm
import predictor.prediction_script as ps
from django.shortcuts import render
from django.http import HttpResponseRedirect
import csv
import os

# Create your views here.

PREDICTION_MODEL = None
DF_DUMMIES = None


def index(request):
    # if this is a POST request we need to process the form data

    global PREDICTION_MODEL
    global DF_DUMMIES

    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = HouseForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            print('got request again!')
            # process the data in form.cleaned_data as required
            predicted_value = ps.get_prediction(form.cleaned_data, PREDICTION_MODEL, DF_DUMMIES)

            # redirect to a new URL:
            return render(request, 'index.html', {'form': form, 'predicted_value': predicted_value})

    # if a GET (or any other method) we'll create a blank form
    else:

        house_data = list(HouseData.objects.all().values())
        PREDICTION_MODEL, DF_DUMMIES = ps.build_model(house_data)
        form = HouseForm()

    return render(request, 'index.html', {'form': form})


def clean_up_data(request):
    neigh_to_clean = [1113, 107, 3312, 6751, 3611, 6727, 1611, 6251, 3246, 6341, 3829, 6911, 6711, 4056, 6626, 1111,
                      3111, 6744, 6331,
                      4287, 4311, 6432, 2211, 4060, 4061, 4069]

    date_to_delete = HouseData.objects.filter(
        neighborhood__in=neigh_to_clean)

    before_len = len(HouseData.objects.all())

    date_to_delete.delete()

    after_len = len(HouseData.objects.all())

    return HttpResponse(str(before_len) + ":" + str(after_len))


def show_all_data(request):
    house_data = list(HouseData.objects.all().values())
    prediction_model = ps.build_model(house_data)
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
