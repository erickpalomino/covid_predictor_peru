
from math import trunc
from src.models.models import InfectionDay,PredictionInfo
import pandas
from pandas.core.frame import DataFrame


def update_database():
    dataset = pandas.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv', engine='python')
    ds_filtered=filter_country_fill_data(dataset,'Peru')
    max=ds_filtered['new_cases_smoothed'].max()
    min=ds_filtered['new_cases_smoothed'].min()
    info=PredictionInfo(min=min,max=max)
    info.save()
    for index,row in ds_filtered.iterrows():
      infection_day=InfectionDay(
        date=index,
        infection_smoothed=int(row['new_cases_smoothed']),
        infection_real=int(row['new_cases'])
      )
      infection_day.save()
    print("DB ready")
    return {"message":"DB ready"}



def filter_country_fill_data(dataset,country):
  ds_filtered=dataset[dataset['location']==country]
  ds_filtered=DataFrame(
      data={
      "new_cases":ds_filtered['new_cases'].values,
      "new_cases_smoothed": ds_filtered['new_cases_smoothed'].values
      },
      index=ds_filtered['date'].values)
  ds_filtered=ds_filtered.fillna(method='bfill').fillna(method='ffill')
  return ds_filtered

  