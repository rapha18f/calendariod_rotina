def marcacao():
    from datetime import datetime
    horario = str(datetime.datetime.now())[:14]
    return horario.strftime("%d/%m/%Y %H:%M:%S")
def calendario():
    from calendar import Calendar
print(marcacao)