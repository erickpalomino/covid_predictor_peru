import os
import pandas
import numpy as np
from pandas.core.frame import DataFrame
import datetime
import statistics

import tensorflow as tf
from tensorflow import keras
from src.models.models import InfectionDay,PredictionInfo
from src.models.data_manager import *
from src.model_manager.model_manager import get_model

format_str = '%Y-%m-%d' # The format

def format_date(datestr):
  return datetime.datetime.strptime(str(datestr),format_str)


def load_model():
    file=get_model()
    print("model path: ",file.name)
    model = keras.models.load_model(file.name)
    return model

def get_prediction():
    model=load_model()
    os.environ['TZ'] = 'America/Lima'
    #prediction_input=reshape_input_database(datetime.datetime.now()-datetime.timedelta(1))
    prediction_input=reshape_input_database(datetime.datetime.now())
    prediction_info=PredictionInfo.objects.order_by('-id').first()
    prediction_input=scale_array(prediction_input,prediction_info.min,prediction_info.max)
    print(prediction_input)
    prediction=model.predict(prediction_input)
    print(prediction)
    ar_pred=inv_scale_array(prediction,prediction_info.min,prediction_info.max)
    print(ar_pred)
    ar_pred=ar_pred.reshape(-1)[0]
    return ar_pred


def predict(date):
    model=load_model()
    os.environ['TZ'] = 'America/Lima'
    prediction_input=reshape_input_database(date)
    prediction_info=PredictionInfo.objects.order_by('-id').first()
    prediction_input=scale_array(prediction_input,prediction_info.min,prediction_info.max)
    print(prediction_input)
    prediction=model.predict(prediction_input)
    print(prediction)
    ar_pred=inv_scale_array(prediction,prediction_info.min,prediction_info.max)
    print(ar_pred)
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

def reshape_input_dataset(date, dataset):
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

def reshape_input_database(date:datetime.date):
  input=[]
  for i in range (14):
    date_i=(date-datetime.timedelta(14-i))
    date_i=date_i.replace(hour=0,minute=0,second=0,microsecond=0)
    print('Date query:',str(date_i))
    input_i=InfectionDay.objects.get(pk=format_date(date_i.date()))
    input.append(input_i.infection_smoothed)
  mean=statistics.mean(input)
  std=statistics.stdev(input)
  input.append(mean)
  input.append(std)
  array=np.array(input)
  array=array.reshape(-1,16,1)
  print(array)
  return array