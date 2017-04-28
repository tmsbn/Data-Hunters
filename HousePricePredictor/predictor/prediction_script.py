import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import _tree
from collections import Counter

PRIMARY_KEY_COL = 'no'
dummies_columns = ['land_use', 'sold_as_vacant', 'city', 'tax_district', 'neighborhood']
target_column = 'sales_price'

ranges = {
    'land_use': (3, 18),
    'sold_as_vacant': (19, 20),
    'city': (21, 30),
    'tax_district': (31, 37),
    'square_footage': (2, 2),
    'neighborhood': (38, 212),
    'land_value': (0, 0),
    'sales_price': (1, 1)
}


def get_prediction(cleaned_data, model, df):
    predict_list = []
    digit_values = []

    print(df)

    for idx, col in enumerate(ranges.keys()):

        if col == target_column:
            continue

        x, y = ranges[col]
        domain = df.columns.values[x: y + 1]
        if not type(cleaned_data[col]) is int:
            for val in domain:
                val = val.split('_')[-1]
                if val == cleaned_data[col]:
                    predict_list.append(1)
                else:
                    predict_list.append(0)
        else:
            digit_values.append(cleaned_data[col])
    predicted_values = model.predict([digit_values + predict_list])
    print(predicted_values)
    return predicted_values[0]


def get_choices():
    choices_dict = {}


def proportion_range_generator(actual, predicted):
    ranges_count = {'Excellent': 0, 'Good': 0, 'Ok': 0, 'Bad': 0}
    for i in range(len(actual)):
        proportion = actual[i] / predicted[i]
        if 1 / 1.2 < proportion < 1.2:
            ranges_count['Excellent'] += 1
        elif 1 / 1.5 < proportion < 1.5:
            ranges_count['Good'] += 1
        elif 1 / 2 < proportion < 2:
            ranges_count['Ok'] += 1
        else:
            ranges_count['Bad'] += 1

    return ranges_count


def build_model(house_data):
    # Read the data Frame -
    df = pd.DataFrame(house_data)
    # counter = Counter(df['neighborhood'].values)
    # print(counter)
    #
    # for key, value in counter.most_common():
    #     print(key, end=',')

    # Delete the primary key column
    del df[PRIMARY_KEY_COL]

    # Convert categorical variables using One Hot Shot Encoding
    df_dummies = pd.get_dummies(df, columns=dummies_columns)

    # Split data into training and testing set
    df_train, df_test = train_test_split(df_dummies, test_size=0.3)
    # print(df_test)
    # Remove the target column from the training data set
    df_target_values = df_train[target_column].values
    del df_train[target_column]
    df_input_values = df_train.values

    # Remove the target column from the testing data set
    actual_values = df_test[target_column].values
    del df_test[target_column]
    df_predict_values = df_test.values

    model = DecisionTreeRegressor(max_depth=10)
    fitted_model = model.fit(df_input_values, df_target_values)
    print('Creating Rules in Rule.txt')

    opfile = open('Rule.txt', 'w')

    tree_to_code(model.tree_, df_test.columns.values, opfile)
    print('Rules created.')

    predicted_values = fitted_model.predict(df_predict_values)

    # ranges_count = proportion_range_generator(actual_values, predicted_values)

    return fitted_model, df_dummies


def tree_to_code(tree_, feature_names, ofile):
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    ofile.write("def tree({}):".format(", ".join(feature_names)) + "\n")

    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            ofile.write("{}if {} <= {}:".format(indent, name, threshold) + "\n")
            recurse(tree_.children_left[node], depth + 1)
            ofile.write("{}else:  # if {} > {}".format(indent, name, threshold) + "\n")
            recurse(tree_.children_right[node], depth + 1)
        else:
            ofile.write("{}return {}".format(indent, tree_.value[node]) + "\n")

    recurse(0, 1)