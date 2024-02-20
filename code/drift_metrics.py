import pandas as pd
from evidently import ColumnMapping
from evidently.report import Report
from evidently.tests import * 
from evidently.metric_preset import DataDriftPreset
from evidently.test_suite import TestSuite
from evidently.test_preset import BinaryClassificationTestPreset, DataStabilityTestPreset
from evidently.options import ColorOptions
from ks_metric import ksMetric
from data_preprocess import model_drift, data_drift, reference_data, preprocess_ref
import warnings
warnings.filterwarnings("ignore") 

path1 = "/Users/pooja/Desktop/GitHub/mrdc_model_monitoring/data/"
path2 = "/Users/pooja/Desktop/GitHub/mrdc_model_monitoring/reports/"

color_scheme = ColorOptions(
    primary_color = "#5a86ad",
    fill_color = "#fff4f2",
    zero_line_color = "#016795",
    current_data_color = "#c292a1",
    reference_data_color = "#017b92"
)

model_cur = model_drift()
model_ref = preprocess_ref()
data_cur = data_drift()
data_ref =  reference_data()

column_mapping = ColumnMapping()
column_mapping.target = 'actual_return'
column_mapping.prediction = 'probability'
column_mapping.numerical_features = None


def label_binary_classification(month):
    label_binary_classification_performance = TestSuite(tests=[
            BinaryClassificationTestPreset(stattest='psi'),
        ],options=[color_scheme])

    label_binary_classification_performance.run(reference_data = model_ref, current_data=model_cur, column_mapping = column_mapping)
    # label_binary_classification_performance.save_html(path2 + "mrdc_model_drift/model_performance_" + month + ".html")
    return label_binary_classification_performance


# data stability report 
def data_stability(month): 
    data_stability= TestSuite(tests=[
        DataStabilityTestPreset(),
    ],options=[color_scheme])
    data_stability.run(current_data=data_cur, reference_data=data_ref, column_mapping=None)
    data_stability.save_html(path2 + "mrdc_data_drift/data_stability_" + month + ".html")
    return data_stability


# data drift report 
def data_drift(month): 
    data_drift_report = Report(metrics=[
                # DataDriftPreset(stattest="ks", stattest_threshold=0.35),  
                DataDriftPreset(stattest="psi", stattest_threshold=0.25),],options=[color_scheme])
    data_drift_report.run(current_data=data_cur, reference_data = data_ref, column_mapping=None)
    data_drift_report.save_html(path2 + "mrdc_data_drift/data_drift_" + month + ".html")
    return data_drift_report

def customizedKsMetric(month): 
    ksMetric_report = Report(metrics = [
        ksMetric()
    ])
    ksMetric_report.run(reference_data= model_ref[['actual_return','probability']], current_data= model_cur[['actual_return','probability']] , column_mapping=column_mapping)
    ksMetric_report.save_html(path2 + "mrdc_model_drift/kstable/kstable_" + month+ ".html")
    return ksMetric_report