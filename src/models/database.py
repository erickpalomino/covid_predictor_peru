from mongoengine import connect, disconnect
from ..settings import settings


def init_database():
    connect(host=(
        f'mongodb+srv://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}?retryWrites=true&w=majority'
    ))
def shutdown_database():
    disconnect()