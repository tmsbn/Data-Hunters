import pandas as pd
from sklearn.model_selection import train_test_split
from collections import Counter
from collections import OrderedDict
from sklearn.tree import DecisionTreeRegressor

RANGE_DICT = OrderedDict({
 'Land Use': (4, 19),
 'Sold As Vacant': (20, 21),
 'City': (22, 31),
 'Square Footage': (0, 0),
 'Tax District': (32, 38),
 'Neighborhood': (1, 1),
 'Land Value': (2, 2),
 'Sale Price': (3, 3)
})


def print_count(df, dummies_columns):
    for i in dummies_columns:
        df_land_use = Counter(df[i].values)
        print(len(df_land_use), df_land_use)


def proportion_range_generator(actual, predicted):
    ranges_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for i in range(len(actual)):
        proportion = actual[i] / predicted[i]
        if proportion >= 1:
            if proportion < 1.1:
                ranges_count['A'] += 1
            elif proportion < 1.2:
                ranges_count['B'] += 1
            elif proportion < 2:
                ranges_count['C'] += 1
            else:
                ranges_count['D'] += 1
        else:
            if proportion > 1 / 1.2:
                ranges_count['A'] += 1
            elif proportion > 1 / 1.5:
                ranges_count['B'] += 1
            elif proportion > 1 / 2:
                ranges_count['C'] += 1
            else:
                ranges_count['D'] += 1
    return ranges_count


def print_accuracy(actual_values, predicted_values):
    count = 0
    for i in range(len(actual_values)):
        if predicted_values[i] == actual_values[i]:
            count += 1
        print(predicted_values[i], actual_values[i], ' = ', predicted_values[i]/ actual_values[i])
    print(count / len(actual_values) * 100)


def convert_prediction(df, input_data):
    """
    Takes in the input variables from the user as a comma separated list and returns a list that is compatable with the
    decision tree.
    :param df: The data set's decision tree compatible list.
    :param range_info: The dictionary of range info.
    :param string_columns: A list of the names of the attribute's whose domain is string.
    :return: The list.
    """
    predict_list = []
    digit_values = []
    for idx, col in enumerate(RANGE_DICT.keys()):
        if col == 'Sale Price':
            continue
        x, y = RANGE_DICT[col]
        domain = df.columns.values[x: y + 1]
        # print(df.columns.values)
        # print(idx, col)
        if not input_data[idx].isdigit():
            for val in domain:
                # print(val, input_data[idx])
                val = val.split('_')[1]
                if val == input_data[idx]:
                    predict_list.append(1)
                else:
                    predict_list.append(0)
        else:
            digit_values.append(input_data[idx])
    return digit_values + predict_list


def find_dummy_columns(df_dummies):
    d = df_dummies.columns.values
    range_list = []
    x = ''
    for i in range(len(d)):
        # print(i, ':', d[i])
        if d[i].strip().split('_')[0] == x:
            continue
        else:
            if len(range_list) >= 1:
                range_list[-1].append(i - 1)
            x = d[i].strip().split('_')[0]
            range_list.append([x, i])
    range_list[-1].append(i)
    range_dict = ()
    print('RANGE_DICT = {')
    for i in range_list:
        if i == len(range_list) - 1:
            print(' \'' + str(i[0]) + '\' : (' + str(i[1]) + ', ' + str(i[2]) + ')')
        else:
            print(' \'' + str(i[0]) + '\' : (' + str(i[1]) + ', ' + str(i[2]) + '),')
    print('}')
    # [['Square Footage', 0, 0], ['Neighborhood', 1, 1], ['Land Value', 2, 2], ['Sale Price', 3, 3],
    #  ['Land Use_CHURCH', 4, 19], ['Sold As Vacant_No', 20, 21], ['City_ANTIOCH', 22, 31],
    #  ['Tax District_CITY OF BELLE MEADE', 32, 38]]
    print(range_list)


def main():
    df = pd.read_csv("Nashville_housing_data.csv")# Reads the csv file as a pandas object.

    dummies_columns = ['Land Use', 'Sold As Vacant', 'City', 'Tax District']
    target_columns = 'Sale Price'

    line = ['Are you Ready!!!']

    # df.loc[-1] = line + [0]

    # df_predict_values = df.iloc[-1].values
    # print(df_predict_values)

    df_dummies = pd.get_dummies(df, columns=dummies_columns)
    # df_dummies_temp = df_dummies.iloc[: -1, :].values
    # df_predict_values = df_dummies.iloc[-1, :-1].values
    # print(df_predict_values)

    df_train, df_test = train_test_split(df_dummies, test_size=0.3)

    # print(df_train.iloc[0].values)
    df_target_values = df_train[target_columns].values
    del df_train[target_columns]
    df_input_values = df_train.values
    # print(df_input_values[0], df_target_values[0])

    actual_values = df_test[target_columns].values
    del df_test[target_columns]
    df_predict_values = df_test.values

    model = DecisionTreeRegressor()
    clf = model.fit(df_input_values, df_target_values)


    while line[0] != 'q':
        line = input().strip().split(',')
        input_to_predict = convert_prediction(df_dummies, line)
        # print(input_to_predict)
        # print(df_dummies.iloc[0].values)
        predicted_values = clf.predict([input_to_predict])
        print(int(predicted_values[0]))
        # ranges_count = proportion_range_generator(actual_values, predicted_values)
        # for key, value in ranges_count.items():
        #     print(key, ':', value)
        # print_accuracy(actual_values, predicted_values)

        #take_input(line, clf, df)


if __name__ == '__main__':
    main()