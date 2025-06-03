import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import function
import os
from datetime import datetime

def adicionar_ao_inicio_do_windows():
    try:
        nome_atalho = "AgendaPessoal.lnk"
        caminho_script = os.path.abspath(__file__)
        pasta_startup = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
        caminho_atalho = os.path.join(pasta_startup, nome_atalho)
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        atalho = shell.CreateShortCut(caminho_atalho)
        atalho.TargetPath = caminho_script
        atalho.WorkingDirectory = os.path.dirname(caminho_script)
        atalho.IconLocation = caminho_script
        atalho.save()
    except Exception as e:
        print(f"Erro ao adicionar ao iniciar: {e}")

def main():
    arquivo_compromissos = {"caminho": None}

    def escolher_arquivo():
        caminho = filedialog.askopenfilename(
            title="Escolha o arquivo de compromissos",
            filetypes=(("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*"))
        )
        if caminho:
            arquivo_compromissos["caminho"] = caminho
            messagebox.showinfo("Arquivo Selecionado", f"Arquivo: {caminho}")

    def marcar_falta(event):
        try:
            linha = int(float(calendario.index(f"@{event.x},{event.y}")).__floor__())
            calendario.config(state="normal")
            linha_inicio = f"{linha}.0"
            linha_fim = f"{linha}.end"
            linha_texto = calendario.get(linha_inicio, linha_fim)

            if "FALTA" not in linha_texto:
                data_hoje = datetime.now().strftime("%d/%m/%Y")
                novo_texto = f"{linha_texto}  [FALTA: {data_hoje}]"
                calendario.delete(linha_inicio, linha_fim)
                calendario.insert(linha_inicio, novo_texto)
                calendario.tag_add("falta", linha_inicio, f"{linha_inicio} lineend")
                calendario.tag_config("falta", foreground="red")
            calendario.config(state="disabled")
        except Exception as e:
            print("Erro ao marcar falta:", e)

    def adicionar_compromisso():
        arquivo = arquivo_compromissos["caminho"]
        if not arquivo:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado!")
            return
        compromisso = simpledialog.askstring("Novo compromisso", "Digite o compromisso (ex: terapia):")
        if compromisso:
            try:
                with open(arquivo, 'a', encoding='utf-8') as f:
                    f.write(f"{compromisso}\n")
                messagebox.showinfo("Sucesso", "Compromisso adicionado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")
    import calendar
    def extrair_dias_com_compromissos():
        dias = set()
        caminho = arquivo_compromissos["caminho"]
        if not caminho:
            return dias

        dias_semana = {
            "segunda": 0,
            "terça": 1,
            "terca": 1,  # caso o usuário não use acento
            "quarta": 2,
            "quinta": 3,
            "sexta": 4,
            "sábado": 5,
            "sabado": 5,
            "domingo": 6
        }

        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudo = f.read().lower()

            # Procura todos os dias da semana mencionados
                dias_encontrados = {dias_semana[palavra] for palavra in dias_semana if palavra in conteudo}

                hoje = datetime.now()
                ano, mes = hoje.year, hoje.month
                _, total_dias = calendar.monthrange(ano, mes)

                for dia in range(1, total_dias + 1):
                    data = datetime(ano, mes, dia)
                    if data.weekday() in dias_encontrados:
                        dias.add(dia)

        except Exception as e:
            print(f"Erro ao extrair dias: {e}")
            return dias
        except:
            pass
        return dias

    def atualizar_calendario():
        dias = extrair_dias_com_compromissos()
        calendario.config(state="normal")
        calendario.delete("1.0", tk.END)
        calendario.insert("1.0", function.calendario_mes_atual(dias_com_compromisso=dias))
        calendario.config(state="disabled")

    root = tk.Tk()
    root.title("Agenda Pessoal")
    root.geometry("800x600")

    titulo = tk.Label(root, text="Calendário do mês", font=("Arial", 20))
    titulo.pack(pady=10)

    data = tk.Label(root, text=f"{function.marcacao()}", font=("Arial", 20))
    data.pack(pady=10)

    calendario = tk.Text(root, font=("Courier", 12), width=30, height=30, wrap=tk.WORD)
    calendario.tag_configure("falta", foreground="red")
    calendario.insert("1.0", function.calendario_mes_atual())
    calendario.config(state="disabled")
    calendario.pack(pady=10)
    calendario.bind("<Button-3>", marcar_falta)

    botao_abrir = tk.Button(root, text="Abrir arquivo", command=escolher_arquivo)
    botao_abrir.pack(pady=5)

    botao_adicionar = tk.Button(root, text="Adicionar compromisso", command=adicionar_compromisso)
    botao_adicionar.pack(pady=5)

    botao_atualizar = tk.Button(root, text="Atualizar", command=atualizar_calendario)
    botao_atualizar.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
    adicionar_ao_inicio_do_windows()