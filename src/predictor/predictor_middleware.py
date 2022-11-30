import os
import pandas
import numpy as np
from pandas.core.frame import DataFrame
import datetime
import statistics

import tensorflow as tf
from tensorflow import keras

def load_model():
    model = keras.models.load_model('./models/model.h5')
    return model

def get_prediction():
    dataset = pandas.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv', engine='python')
    ds_filtered=dataset[dataset['location']=='Peru']
    ds_filtered=DataFrame(data={"new_cases_smoothed":ds_filtered['new_cases_smoothed'].values, "date":ds_filtered['date'].values})
    ds_filtered=ds_filtered.fillna(method='bfill').fillna(method='ffill')
    max=ds_filtered['new_cases_smoothed'].max()
    min=ds_filtered['new_cases_smoothed'].min()
    arr_scaled=scale_array(ds_filtered['new_cases_smoothed'].values,min,max)
    print(arr_scaled)
    ds_scaled=pandas.DataFrame(data={"new_cases_smoothed":arr_scaled,"date":ds_filtered['date'].values})
    print(ds_scaled.head().to_string())
    model=load_model()
    prediction=model.predict(reshape_input(datetime.datetime.now(),ds_scaled))
    print(prediction)
    ar_pred=inv_scale_array(prediction,min,max)
    ar_pred=ar_pred.reshape(-1)[0]
    return ar_pred


def min_max_scale(x,min,max):
  return (x-min)/(max-min)

def min_max_inverse(x_scaled,min,max):
  return (x_scaled*(max-min))+min

def scale_array(arr,min,max):
  res=[]
  for x in arr:
    res.append(min_max_scale(x,min,max))
  return np.asanyarray(res)

def inv_scale_array(arr,min,max):
  res=[]
  for x in arr:
    res.append(min_max_inverse(x,min,max))
  return np.asanyarray(res)

def reshape_input(date, dataset):
  input=[]
  for i in range(14):
    date_i=(date-datetime.timedelta(14-i)).strftime('%Y-%m-%d')
    print(date_i)
    query_str=f'date == "{date_i}"'
    print(query_str)
    input_i=dataset.query(query_str)['new_cases_smoothed'].values[0]
    print(input_i)
    input.append(input_i)
  mean= statistics.mean(input)
  std=statistics.stdev(input)
  input.append(mean)
  input.append(std)
  array=np.array(input)
  array=array.reshape(-1,16,1)
  print(array)
  return array