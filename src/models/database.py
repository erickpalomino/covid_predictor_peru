from mongoengine import connect, disconnect


def init_database():
    connect(host=(
        f'mongodb+srv://root:root@cluster0.7mevyjk.mongodb.net/covid_prediction?retryWrites=true&w=majority'
    ))
def shutdown_database():
    disconnect()