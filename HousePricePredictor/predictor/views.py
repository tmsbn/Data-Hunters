from django.http import HttpResponse
from predictor.models import HouseData
from predictor.prediction_script import build_model
import csv
import os


# Create your views here.

def index(request):
    return HttpResponse("Hello, world!")


def show_all_data(request):
    house_data = HouseData.objects.all()
    prediction_model = build_model(house_data)
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
