##RFM ANALYSIS WITH SAMPLE DATA ##

import pandas as pd
import datetime as dt
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_csv("Datasets/sales_data_sample.csv")
## Checking the dataframe

def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)
    print("####################Describe ######################")
    print(df.describe().T)

check_df(df)
## Checking null
df.isnull().values.any()
df.isnull().sum()
"""
There is missing values but they are not important values and will not affect the study.
"""

##ORDERDATE Column is "Object" so I had to convert it to datetime
df["ORDERDATE"].dtypes
df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"])

df["ORDERDATE"].max()
today_date = dt.datetime(2005, 6, 2)

## Generating RFM scores and converting them to a single variable
rfm = df.groupby("CUSTOMERNAME").agg({"ORDERDATE" : lambda date: (today_date - date.max()).days,
                                     "ORDERNUMBER" : lambda num: num.nunique(),
                                     "SALES" : lambda price : price.sum()})
rfm.head(10)
rfm.shape

rfm.columns = ["Recency","Frequency","Monetary"]
rfm["Monetary"].min()

#RFM skorlarının oluşturulması ve tek bir değişkene çevrilmesi

rfm["recency_score"] = pd.qcut(rfm["Recency"] , 5, labels=[5,4,3,2,1])
rfm["frequency_score"] = pd.qcut(rfm["Frequency"].rank(method="first") , 5 ,labels=[1,2,3,4,5])
rfm["monetary_score"] = pd.qcut(rfm["Monetary"],5 , labels=[1,2,3,4,5])

rfm["RFM_Score"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))
rfm.head()

## Defining #RFM scores as segments

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm["Segment"] = rfm["RFM_Score"].replace(seg_map, regex=True)
rfm.head()

rfm.groupby("Segment").agg(["mean", "count"])

