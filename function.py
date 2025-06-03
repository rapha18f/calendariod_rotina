def marcacao():
    from datetime import datetime
    horario = datetime.now()
    return horario.strftime("%d/%m/%Y %H:%M:%S")
import calendar
from datetime import datetime

def calendario_mes_atual(dias_com_compromisso=set()):
    hoje = datetime.now()
    cal = calendar.TextCalendar(firstweekday=0)
    texto = cal.formatmonth(hoje.year, hoje.month)

    for dia in dias_com_compromisso:
        # Substitui o dia (ex: "15") por "*15" no calendário
        texto = texto.replace(f"{dia:2d} ", f"*{dia:2d}")
    return texto
def sequencia_hde_datas_marcadas_ordenadas(arquivotxt, quantidade=30):
    import os
    from datetime import datetime, timedelta
    dias_da_semana = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
    if not os.path.exists(arquivotxt):
        return []
    with open(arquivotxt, 'r') as file:
        linhas = [linha.strip() for linha in file.readlines()]
    if len(linhas) < 2:
        return []
    compromisso = linhas[0]
    dias_escolhidos = linhas[1:]
    dias_indices = [dias_da_semana.index(dia) for dia in dias_escolhidos]
    hoje = datetime.today().date()
    datas_resultado = []
    dia_atual = hoje
    while len(datas_resultado) < quantidade:
        if dia_atual.weekday() in dias_indices:
            datas_resultado.append((dia_atual, compromisso))
        dia_atual += timedelta(days=1)
    return datas_resultado
def salvar_dados_em_txt(arquivotxt, dados):
    with open(arquivotxt, 'w') as file:
        for data, compromisso in dados:
            file.write(f"{data.strftime('%d/%m/%Y')} - {compromisso}\n")
    return True