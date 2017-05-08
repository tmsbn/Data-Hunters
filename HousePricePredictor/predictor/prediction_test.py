import pandas as pd
from sklearn.tree import DecisionTreeRegressor, export_graphviz
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn import tree
from sklearn.tree import _tree
import numpy
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
import pydot


dummies_columns = ['Land Use', 'Sold As Vacant', 'City', 'Tax District', 'Neighborhood']
PRIMARY_KEY_COL = 'No'
target_col = 'Sale Price'


def tree_to_code(d_tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
        ]
    print("def tree({}):".format(", ".join(feature_names)))

    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            print("{}if {} <= {}:".format(indent, name, threshold))
            recurse(tree_.children_left[node], depth + 1)
            print("{}else:  # if {} > {}".format(indent, name, threshold))
            recurse(tree_.children_right[node], depth + 1)
        else:
            print("{}return {}".format(indent, tree_.value[node]))

    recurse(0, 1)


def visualize_tree(d_tree, feature_names):
    with open("output.dot", 'w') as f:
        export_graphviz(d_tree, out_file=f, feature_names=feature_names)

        try:
            (graph,) = pydot.graph_from_dot_file('output.dot')
            graph.write_png('output.png')
        except Exception as e:
            print(str(e))

def proportion_range_generator(actual, predicted, n):

    """
    Generate the percentage accuracy for the prediction
    :param actual:
    :param predicted:
    :param n:
    :return:
    """
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

    ranges_count['Excellent'] = ranges_count['Excellent']/ n * 100
    ranges_count['Good'] = ranges_count['Good'] / n * 100
    ranges_count['Ok'] = ranges_count['Ok'] / n * 100
    ranges_count['Bad'] = ranges_count['Bad'] / n * 100

    return ranges_count


def main():

    # Read csv and make data frame
    df = pd.read_csv('Nashville_housing_data_test.csv')
    # print(df)

    # Delete the primary key column
    del df[PRIMARY_KEY_COL]

    # Convert categorical variables using One Hot Shot Encoding
    df_dummies = pd.get_dummies(df, columns=dummies_columns)

    # Get Column names
    column_names = df_dummies.columns.values

    # Test and Training
    df_train, df_test = train_test_split(df_dummies, test_size=0.3)

    # Select Target values
    df_target_values = df_train[target_col].values
    del df_train[target_col]
    df_input_values = df_train.values

    # Predict values
    df_actual_values = df_test[target_col].values
    del df_test[target_col]
    df_test_values = df_test.values

    # print(df_train)

    dt_clf = DecisionTreeRegressor()
    rf_clf = RandomForestRegressor()
    gb_clf = GradientBoostingRegressor()

    models = [gb_clf, dt_clf, rf_clf]

    for j in range(0, 5):

        print("Iteration " + str(j + 1) + ":\n")

        for model in models:

            clf = model.fit(df_input_values, df_target_values)

            # Predict values
            predicted_values = clf.predict(df_test_values)

            print('\n' + type(clf).__name__)
            print(proportion_range_generator(df_actual_values, predicted_values, len(predicted_values)))

            if type(model) is RandomForestRegressor:
                print("Feature importance", end=':')
                importance = model.feature_importances_
                sorted_importance = sorted(importance, reverse=True)
                sorted_importance_str = []
                for idx, imp in enumerate(sorted_importance):

                    if idx < 7:
                        sorted_importance_str.append(column_names.tolist()[importance.tolist().index(imp)] + ": " + str(round(imp , 2) * 100.0))

                print(','.join(sorted_importance_str))

        print("\n")

        if type(model) is DecisionTreeRegressor:
            visualize_tree(clf, column_names)


if __name__ == "__main__":
    main()
