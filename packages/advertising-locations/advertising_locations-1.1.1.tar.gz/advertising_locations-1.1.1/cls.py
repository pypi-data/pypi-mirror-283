import numpy as np
import pandas as pd
from catboost import Pool


def split_on_intervals(min_val, max_val, n) -> list[float]:
    step = (max_val - min_val) / n
    intervals = [min_val + (step * x) for x in range(n + 1)]
    return intervals


def create_groups(x_intervals, y_intervals):
    groups = {}
    x_intervals = np.concatenate([[-np.inf], x_intervals, [np.inf]])
    y_intervals = np.concatenate([[-np.inf], y_intervals, [np.inf]])

    for x_i in range(len(x_intervals) - 1):
        for y_i in range(len(y_intervals) - 1):
            groups[
                f'x : {x_intervals[x_i]} - {x_intervals[x_i + 1]} | y : {y_intervals[y_i]} - {y_intervals[y_i + 1]}'] = 0

    return groups


def sort_on_groups(x_vals, y_vals, x_intervals, y_intervals, groups, only_vals=False):
    for x, y in zip(x_vals, y_vals):
        for x_i in range(len(x_intervals) - 1):
            for y_i in range(len(y_intervals) - 1):
                if (x_intervals[x_i] <= x < x_intervals[x_i + 1]) and (y_intervals[y_i] <= y < y_intervals[y_i + 1]):
                    groups[
                        f'x : {x_intervals[x_i]} - {x_intervals[x_i + 1]} | y : {y_intervals[y_i]} - {y_intervals[y_i + 1]}'] += 1

    if only_vals:
        return list(groups.values())

    return groups


def create_dataset_one_campaign(config, geo_points):
    x_intervals = split_on_intervals(config['min_xval'], config['max_xval'], config['x_ngroups'])
    y_intervals = split_on_intervals(config['min_yval'], config['max_yval'], config['y_ngroups'])

    groups = create_groups(x_intervals, y_intervals)

    groups_values = []

    points = np.array([[float(x['lat']), float(x['lon'])] for x in geo_points])

    group_values = sort_on_groups(points[:, 0], points[:, 1], x_intervals, y_intervals, groups.copy(), only_vals=True)
    groups_values.append(group_values)

    groups_values = np.array(groups_values)

    for i in range(len(groups.keys())):
        groups[list(groups.keys())[i]] = groups_values[:, i]

    return groups


class Predictor():
    def __init__(self, models, config):
        self.models = models
        self.config = config

    def predict(self, TA, points):
        pt_df = pd.DataFrame(create_dataset_one_campaign(self.config, points))
        TA_df = pd.DataFrame(TA)
        dataset = pd.concat([pt_df, TA_df], axis=1)
        X = Pool(data=dataset, cat_features=['gender', 'ageFrom', 'ageTo', 'income'])
        preds = []
        for model in self.models:
            preds.append(model.predict(X))

        return sum(preds) / len(preds)
