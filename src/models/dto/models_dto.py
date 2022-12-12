from pydantic import BaseModel
from datetime import date

class InfectionDayDTO(BaseModel):
    date: date
    infection_real: int
    infection_smoothed: int