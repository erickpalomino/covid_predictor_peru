from mongoengine import *
import datetime
format_str = '%Y-%m-%d' # The format

def format_date(datestr):
  return datetime.datetime.strptime(str(datestr),format_str)

class InfectionDay(Document):
    date = DateField(primary_key=True)
    infection_smoothed=IntField()
    infection_real=IntField()

    def __str__(self):
        return str({
            'date': str(format_date(self.date)),
            'infection_real': self.infection_real,
            'infection_smoothed':self.infection_smoothed
        })


class PredictedDay(Document):
    date = DateField(primary_key=True)
    infection_predicted=IntField()
    infection_smoothed=IntField()
    infection_real=IntField()


class PredictionInfo(Document):
    max= IntField()
    min= IntField()
    
class ModelInfo(Document):
    model_id=StringField(primary_key=True)
    model_name=StringField()

class ActualModel(Document):
    id=IntField(primary_key=True,default=1)
    model_id=StringField(required=True)