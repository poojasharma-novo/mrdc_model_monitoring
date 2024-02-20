import os  
from combine_reports import combine_html
from drift_metrics import label_binary_classification, data_stability, data_drift, customizedKsMetric
import datetime
from dateutil.relativedelta import relativedelta
import warnings
warnings.filterwarnings("ignore") 

current_date = datetime.date.today()
previous_month = current_date - relativedelta(months=1)
month = previous_month.strftime("%b") 
year_of_same_month = previous_month.year
month = month + "_" + str(year_of_same_month)

def main(): 
    # try: 
        label_binary_classification(month)
        data_drift(month)
        data_stability(month)
        customizedKsMetric(month)
        combine_html()

    # except Exception as e:
    #     print('!! Error in running main.py :', e)

if __name__ == "__main__": 
    main()
