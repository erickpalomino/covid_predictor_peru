from src.models.models import InfectionDay
from src.models.dto.models_dto import InfectionDayDTO
from src.predictor.predictor_middleware import get_prediction
import datetime

format_str = '%Y-%m-%d' # The format

def format_date(datestr):
  return datetime.datetime.strptime(str(datestr),format_str)

def getInfectionDay(dateq):
  date=dateq
  infectionDay=InfectionDay.objects.get(pk=format_date(date))
  return {"result":(str(infectionDay))}

def get_infection_7_days(date):
    infection_list=[]
    for i in range (7):
        date_i=(date-datetime.timedelta(7-i))
        date_i=date_i.replace(hour=0,minute=0,second=0,microsecond=0)
        print('Date query:',str(date_i))
        infection=InfectionDay.objects.get(pk=format_date(date_i.date()))
        infection_dto=InfectionDayDTO(
            date=infection.date, 
            infection_real=infection.infection_real,
            infection_smoothed=infection.infection_smoothed)
        infection_list.append(infection_dto)
    return infection_list

def get_infection_with_prediction():
    infection_list=get_infection_7_days(datetime.datetime.now())
    prediction=get_prediction()
    predicted_infection=InfectionDayDTO(date=(datetime.datetime.now()),infection_real=0,infection_smoothed=int(prediction))
    infection_list.append(predicted_infection)
    return infection_list