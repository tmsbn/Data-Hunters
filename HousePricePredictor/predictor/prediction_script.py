import pandas as pd
from sklearn.model_selection import train_test_split
from collections import Counter
from collections import OrderedDict
from sklearn.tree import DecisionTreeRegressor
from predictor.models import HouseData
from django_pandas.io import read_frame

PRIMARY_KEY_COL = 'no'
dummies_columns = ['land_use', 'sold_as_vacant', 'city', 'tax_district']
target_columns = 'sales_price'


def proportion_range_generator(actual, predicted):
    ranges_count = {'Excellent': 0, 'Good': 0, 'Ok': 0, 'Bad': 0}
    for i in range(len(actual)):
        proportion = actual[i] / predicted[i]
        if 1/1.2 < proportion < 1.2:
            ranges_count['Excellent'] += 1
        elif 1/1.5 < proportion < 1.5:
            ranges_count['Good'] += 1
        elif 1/2 < proportion < 2:
            ranges_count['Ok'] += 1
        else:
            ranges_count['Bad'] += 1

    return ranges_count


def build_model(house_data):

    # Read the data Frame - this is a Django-Pandas method for convenience
    df = read_frame(house_data)

    # Delete the primary key column
    del df[PRIMARY_KEY_COL]

    # Convert categorical variables using One Hot Shot Encoding
    df_dummies = pd.get_dummies(df, columns=dummies_columns)

    # Split data into training and testing set
    df_train, df_test = train_test_split(df_dummies, test_size=0.3)

    # Remove the target column from the training data set
    df_target_values = df_train[target_columns].values
    del df_train[target_columns]
    df_input_values = df_train.values

    # Remove the target column from the testing data set
    actual_values = df_test[target_columns].values
    del df_test[target_columns]
    df_predict_values = df_test.values

    model = DecisionTreeRegressor()
    clf = model.fit(df_input_values, df_target_values)

    predicted_values = clf.predict(df_predict_values)
    ranges_count = proportion_range_generator(actual_values, predicted_values)

    return ranges_count.items()
