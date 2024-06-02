import tkinter as tk
import requests
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import json
from tkinter import ttk, messagebox, BooleanVar
from PIL import ImageTk
import platform
import ctypes

class WeatherApp:
    #função para iniciar a pagina inicial
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Application")
        self.root.geometry("800x600")

        self.data_window = None
        self.graph_window = None
        self.alert_window = None
        self.hist_window = None

        self.load_theme()

        #carregar o tema "azure"
        self.style = ttk.Style()
        self.style.theme_use('azure-dark')
        self.configure_styles()

        #icon da janela
        icon_path = r'weather-2019-02-07.ico'
        self.set_app_icon(icon_path)

        #booleano para o butão switch
        self.theme_var = BooleanVar(value=False)

        self.create_main_interface()
        self.enviar()

    def load_theme(self): #função para carregar o tema e inicia-lo em "dark"
        try:
            self.root.tk.call('source', 'azure/azure.tcl')
            self.root.tk.call('set_theme', 'dark')
        except tk.TclError:
            pass

    def set_app_icon(self, icon_path): #função para carregar o icon dependendo do sistema operativo

        if platform.system() == 'Windows':
            self.root.iconbitmap(icon_path)

            app_id = 'myweatherapp'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        else:
            icon = ImageTk.PhotoImage(file=icon_path.replace('.ico', '.png'))
            self.root.iconphoto(True, icon)


    def create_main_interface(self): #função com os botões e labels da pagina principal
        self.limpar_pagina()

        # Title Label centered at the top
        self.title_label = ttk.Label(self.root, text="WeatherApp", font=('Courier New', 80, "italic", "bold"))
        self.title_label.pack(pady=30)

        # Buttons centered below the title
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        self.weather_button = ttk.Button(button_frame, text="Forecast", command=self.show_weather_options,
                                         style="Large.TButton")
        self.weather_button.pack(pady=10)

        self.theme_button = ttk.Button(button_frame, text="Histórico", command=self.historico, style="Large.TButton")
        self.theme_button.pack(pady=10)

        self.botao_conta = ttk.Button(button_frame, text="Conta", command=self.acessar_conta, style="Large.TButton")
        self.botao_conta.pack(pady=10)

        switch_frame = tk.Frame(self.root)
        switch_frame.place(relx=1.0, rely=0.0, anchor='ne', x=-20, y=20)  # Posição a alterar

        inner_frame = tk.Frame(switch_frame)
        inner_frame.pack()

        self.moon_label = ttk.Label(inner_frame, text="🌙")
        self.moon_label.pack(side=tk.LEFT, padx=5)

        self.theme_switch = ttk.Checkbutton(inner_frame, style='Switch.TCheckbutton', variable=self.theme_var,
                                            command=self.toggle_theme)
        self.theme_switch.pack(side=tk.LEFT)

        self.sun_label = ttk.Label(inner_frame, text="☀️")
        self.sun_label.pack(side=tk.LEFT, padx=5)

    def configure_styles(self): # configuração e estilo dos botões
        button_font = ('Helvetica', 24)  # tamanho da fonte
        self.style.configure("Large.TButton", font=button_font, padding=20)
        self.style.configure('TLabel', font=('Helvetica', 12))

        self.style.configure("Switch.TCheckbutton", font=('Helvetica', 10))
        self.style.configure("Switch.TLabel", font=('Helvetica', 10, 'bold'))

    def apply_theme(self): #escolha do tema para usar no botão switch
        if self.theme_var.get():
            self.root.tk.call("set_theme", "light")
            self.style.theme_use('azure-light')
        else:
            self.root.tk.call("set_theme", "dark")
            self.style.theme_use('azure-dark')

    def toggle_theme(self): #função para o toggle do tema
        self.apply_theme()
        self.configure_styles()

    # ----------------

    def acessar_conta(self):
        # Limpar a página
        self.limpar_pagina()

        # Verificar se existem dados do usuário no arquivo JSON
        if os.path.exists("dados_usuario.json"):
            with open("dados_usuario.json", "r") as f:
                dados_usuario = json.load(f)
            # Exibir os dados do usuário
            self.exibir_informacoes(dados_usuario)
        else:
            # Exibir campos para inserir informações da conta
            self.label_nome = tk.Label(self.root, text="Nome:")
            self.label_nome.pack(pady=5)
            self.entry_nome = tk.Entry(self.root)
            self.entry_nome.pack(pady=5)

            self.label_morada = tk.Label(self.root, text="Cidade:")
            self.label_morada.pack(pady=5)
            self.entry_morada = tk.Entry(self.root)
            self.entry_morada.pack(pady=5)

            self.label_email = tk.Label(self.root, text="Email:")
            self.label_email.pack(pady=5)
            self.entry_email = tk.Entry(self.root)
            self.entry_email.pack(pady=5)

            self.botao_guardar = tk.Button(self.root, text="Guardar", command=self.guardar_informacoes)
            self.botao_guardar.pack(pady=10)

    def limpar_pagina(self):
        # Limpa todos os widgets da página
        for widget in self.root.winfo_children():
            widget.destroy()

    def guardar_informacoes(self):
        # Função para guardar as informações da conta do usuário em um arquivo JSON
        nome = self.entry_nome.get()
        morada = self.entry_morada.get()
        email = self.entry_email.get()

        # Criar dicionário com as informações do usuário
        dados_usuario = {
            "Nome": nome,
            "Morada": morada,
            "Email": email
        }

        # Salvar os dados em um arquivo JSON
        with open("dados_usuario.json", "w") as f:
            json.dump(dados_usuario, f)
        print("Informações da conta salvas com sucesso.")
        # Após salvar as informações, exibir na tela
        self.exibir_informacoes(dados_usuario)

    def exibir_informacoes(self, dados_usuario):
        # Limpar a página
        self.limpar_pagina()

        # Exibir informações da conta
        self.label_nome = tk.Label(self.root, text="Nome: " + dados_usuario["Nome"])
        self.label_nome.pack(pady=5)

        self.label_morada = tk.Label(self.root, text="Cidade " + dados_usuario["Morada"])
        self.label_morada.pack(pady=5)

        self.label_email = tk.Label(self.root, text="Email: " + dados_usuario["Email"])
        self.label_email.pack(pady=5)

        # Botão Atualizar
        self.botao_atualizar = tk.Button(self.root, text="Atualizar", command=self.atualizar_conta)
        self.botao_atualizar.pack(pady=10)

        # Botão voltar
        self.botao_voltar = tk.Button(self.root, text="Voltar", command=self.voltar_pagina_inicial)
        self.botao_voltar.pack(pady=10)

    def atualizar_conta(self):
        # Limpar a página
        self.limpar_pagina()

        # Exibir campos para inserir informações da conta
        self.label_nome = tk.Label(self.root, text="Nome:")
        self.label_nome.pack(pady=5)
        self.entry_nome = tk.Entry(self.root)
        self.entry_nome.pack(pady=5)

        self.label_morada = tk.Label(self.root, text="Cidade:")
        self.label_morada.pack(pady=5)
        self.entry_morada = tk.Entry(self.root)
        self.entry_morada.pack(pady=5)

        self.label_email = tk.Label(self.root, text="Email:")
        self.label_email.pack(pady=5)
        self.entry_email = tk.Entry(self.root)
        self.entry_email.pack(pady=5)

        self.botao_guardar = tk.Button(self.root, text="Guardar", command=self.guardar_informacoes)
        self.botao_guardar.pack(pady=10)

        # Botão cancelar
        self.botao_cancelar = tk.Button(self.root, text="Cancelar", command=self.acessar_conta)
        self.botao_cancelar.pack(pady=10)

    def voltar_pagina_inicial(self):
        # Limpar a página
        self.limpar_pagina()

        # Voltar para a página inicial
        self.__init__(self.root)

    # ----------

    def show_weather_options(self):
        self.limpar_pagina()

        self.city_select_label = ttk.Label(self.root, text="Enter city for weather forecast:")
        self.city_select_label.pack(pady=5)
        self.city_select_entry = ttk.Entry(self.root)
        self.city_select_entry.pack(pady=5)

        # Buttons to show data, graphs, and alerts
        self.show_data_button = ttk.Button(self.root, text="Show Data", command=self.mostrar_dados_meteo)
        self.show_data_button.pack(pady=5)

        self.show_graph_button = ttk.Button(self.root, text="Show Graph", command=self.plotar_graficos_tempo)
        self.show_graph_button.pack(pady=5)

        self.show_alert_button = ttk.Button(self.root, text="Show Alerts", command=self.show_alert)
        self.show_alert_button.pack(pady=5)

        self.back_button = ttk.Button(self.root, text="Back", command=self.create_main_interface)
        self.back_button.pack(pady=20)

    def obter_coordenadas(self, cidade):
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={cidade}&limit=1&appid=7341cc3239672fcc5a85b0084b0095c8"
        resposta = requests.get(url)
        dados = resposta.json()
        if resposta.status_code == 200:
            return dados[0]['lat'], dados[0]['lon']
        else:
            return None, None

    def obter_dados_meteo(self, latitude, longitude):
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True,
            "hourly": "temperature_2m,relative_humidity_2m,dew_point_2m,"
                      "precipitation_probability,precipitation,rain,snowfall",
            "forecast_days": 1
        }
        response = requests.get(url, params=params)
        return response.json()

    def mostrar_dados_meteo(self):
        cidade = self.city_select_entry.get()
        latitude, longitude = self.obter_coordenadas(cidade)
        if latitude is None or longitude is None:
            messagebox.showerror("Error", "City coordinates could not be found.")
        else:
            response = self.obter_dados_meteo(latitude, longitude)
            hourly = response.get('hourly', {})
            hora_atual = datetime.now(tz=timezone.utc)
            indice_momento_atual = int(
                (hora_atual - hora_atual.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds() / 3600)

            temperatura_atual = hourly['temperature_2m'][indice_momento_atual]
            umidade_atual = hourly['relative_humidity_2m'][indice_momento_atual]
            ponto_orvalho_atual = hourly['dew_point_2m'][indice_momento_atual]
            probabilidade_precipitacao_atual = hourly['precipitation_probability'][indice_momento_atual]
            precipitacao_atual = hourly['precipitation'][indice_momento_atual]
            chuva_atual = hourly['rain'][indice_momento_atual]
            neve_atual = hourly['snowfall'][indice_momento_atual]

            self.mostrar_interface_dados_meteo(temperatura_atual, umidade_atual, ponto_orvalho_atual,
                                               probabilidade_precipitacao_atual, precipitacao_atual, chuva_atual,
                                               neve_atual)

    def mostrar_interface_dados_meteo(self, temperatura, umidade, ponto_orvalho, probabilidade_precipitacao,
                                      precipitacao, chuva, neve):
        if self.data_window:
            self.data_window.destroy()

        self.data_window = tk.Toplevel(self.root)
        self.data_window.title("Dados Meteorológicos")

        label_temperatura = tk.Label(self.data_window, text=f"Temperatura: {temperatura:.2f} °C")
        label_temperatura.pack(pady=5)

        label_umidade = tk.Label(self.data_window, text=f"Umidade: {umidade:.2f} %")
        label_umidade.pack(pady=5)

        label_ponto_orvalho = tk.Label(self.data_window, text=f"Ponto de Orvalho: {ponto_orvalho:.2f} °C")
        label_ponto_orvalho.pack(pady=5)

        label_probabilidade_precipitacao = tk.Label(self.data_window,
                                                    text=f"Probabilidade de Precipitação: "
                                                         f"{probabilidade_precipitacao:.2f} %")
        label_probabilidade_precipitacao.pack(pady=5)

        label_precipitacao = tk.Label(self.data_window, text=f"Precipitação: {precipitacao:.2f} mm")
        label_precipitacao.pack(pady=5)

        label_chuva = tk.Label(self.data_window, text=f"Chuva: {chuva:.2f} mm")
        label_chuva.pack(pady=5)

        label_neve = tk.Label(self.data_window, text=f"Neve: {neve:.2f} cm")
        label_neve.pack(pady=5)

    def plotar_graficos_tempo(self):
        cidade = self.city_select_entry.get()
        latitude, longitude = self.obter_coordenadas(cidade)
        if latitude is None or longitude is None:
            messagebox.showerror("Error", "City coordinates could not be found.")
        else:
            response = self.obter_dados_meteo(latitude, longitude)
            hourly = response.get('hourly', {})
            horas = pd.date_range(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), periods=24,
                                  freq='H').strftime('%H:%M')
            temperaturas = hourly['temperature_2m']
            umidades = hourly['relative_humidity_2m']
            pontos_orvalho = hourly['dew_point_2m']
            probabilidades_precipitacao = hourly['precipitation_probability']
            precipitacoes = hourly['precipitation']
            chuvas = hourly['rain']
            neves = hourly['snowfall']

            if self.graph_window:
                plt.close(self.graph_window)

            self.graph_window = plt.figure(figsize=(10, 8))

            plt.subplot(3, 1, 1)
            plt.plot(horas, temperaturas, label='Temperatura (°C)')
            plt.plot(horas, pontos_orvalho, label='Ponto de Orvalho (°C)')
            plt.xlabel('Hora')
            plt.ylabel('Temperatura / Ponto de Orvalho')
            plt.legend()

            plt.subplot(3, 1, 2)
            plt.plot(horas, umidades, label='Umidade (%)')
            plt.xlabel('Hora')
            plt.ylabel('Umidade')
            plt.legend()

            plt.subplot(3, 1, 3)
            plt.plot(horas, probabilidades_precipitacao, label='Probabilidade de Precipitação (%)')
            plt.plot(horas, precipitacoes, label='Precipitação (mm)')
            plt.plot(horas, chuvas, label='Chuva (mm)')
            plt.plot(horas, neves, label='Neve (cm)')
            plt.xlabel('Hora')
            plt.ylabel('Precipitação')
            plt.legend()

            plt.tight_layout()
            plt.show()

    # -----

    def obter_sigla(self, cidade):
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={cidade}&limit=1&appid=7341cc3239672fcc5a85b0084b0095c8"
        resposta = requests.get(url)
        dados = resposta.json()
        if dados:
            return dados[0]['country']
        else:
            return None

    def verificar_continente(self, sigla):
        paises_europa_siglas = [
            "AL", "AD", "AT", "BY", "BE", "BA", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE",
            "GR", "HU", "IS", "IE", "IT", "LV", "LI", "LT", "LU", "MK", "MT", "MD", "MC", "ME", "NL",
            "NO", "PL", "PT", "RO", "SM", "RS", "SK", "SI", "ES", "SE", "CH", "TR", "UA", "GB", "VA"
        ]

        paises_asia_siglas = [
            "AF", "AM", "AZ", "BH", "BD", "BT", "BN", "KH", "CN", "CY", "GE", "IN", "ID", "IR", "IQ",
            "IL", "JP", "JO", "KZ", "KW", "KG", "LA", "LB", "MY", "MV", "MN", "MM", "NP", "KP", "OM",
            "RU", "PK", "PS", "PH", "QA", "SA", "SG", "KR", "LK", "SY", "TW", "TJ", "TH", "TR", "TM",
            "AE", "UZ", "VN", "YE"
        ]

        paises_africa_siglas = [
            "DZ", "AO", "BJ", "BW", "BF", "BI", "CV", "CM", "CF", "TD", "KM", "CG", "CD", "DJ", "EG",
            "GQ", "ER", "ET", "SZ", "GA", "GM", "GH", "GN", "GW", "CI", "KE", "LS", "LR", "LY", "MG",
            "MW", "ML", "MR", "MU", "MA", "MZ", "NA", "NE", "NG", "RW", "ST", "SN", "SC", "SL", "SO",
            "ZA", "SS", "SD", "TZ", "TG", "TN", "UG", "EH", "ZM", "ZW"
        ]

        paises_america_sul_siglas = [
            "AR", "BO", "BR", "CL", "CO", "EC", "GY", "PE", "PY", "SR", "UY", "VE"
        ]

        paises_america_norte_siglas = [
            "CA", "US", "MX", "GT", "CU", "HT", "DO", "HN", "NI", "CR", "PA", "BS", "JM", "BZ", "SV",
            "TT", "VC", "AG", "BB", "GD", "DM", "KN", "LC"
        ]

        paises_america_central_siglas = [
            "BZ", "CR", "SV", "GT", "HN", "NI", "PA", "BS", "CU", "HT", "DO", "TT", "VC", "AG", "BB",
            "GD", "DM", "KN", "LC"
        ]

        if sigla in paises_europa_siglas:
            return "Europa"
        elif sigla in paises_asia_siglas:
            return "Ásia"
        elif sigla in paises_africa_siglas:
            return "África"
        elif sigla in paises_america_sul_siglas:
            return "América do Sul"
        elif sigla in paises_america_norte_siglas:
            return "América do Norte"
        elif sigla in paises_america_central_siglas:
            return "América Central"
        else:
            return "Sigla não encontrada em nenhuma lista de países."

    def verificar_continente_pelo_nome_da_cidade(self, cidade):
        sigla = self.obter_sigla(cidade)
        if sigla:
            return self.verificar_continente(sigla)
        else:
            return "Cidade não encontrada ou sigla do país não disponível."

    def show_alert(self):
        cidade = self.city_select_entry.get()
        latitude, longitude = self.obter_coordenadas(cidade)
        regiao = self.verificar_continente_pelo_nome_da_cidade(cidade)
        if latitude is None or longitude is None:
            messagebox.showerror("Error", "City coordinates could not be found.")
            return
        else:
            response = self.obter_dados_meteo(latitude, longitude)
            hourly = response.get('hourly', {})
            hora_atual = datetime.now(tz=timezone.utc)
            indice_momento_atual = int(
                (hora_atual - hora_atual.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds() / 3600)

            temperatura = hourly['temperature_2m'][indice_momento_atual]
            humidade = hourly['relative_humidity_2m'][indice_momento_atual]

            if self.alert_window:
                self.alert_window.destroy()

            self.alert_window = tk.Toplevel(self.root)
            self.alert_window.title("Alertas")

            alertas = []

            if regiao in ["Europa", "Ásia", "África", "América do Sul", "América do Norte", "América Central",
                          "Austrália"]:
                if temperatura >= 26 and humidade >= 60:
                    alertas.append(f"Condições para tempestades são atendidas em {cidade}.")
                if temperatura >= 20 and humidade >= 50:
                    alertas.append(f"Condições para tornados são atendidas em {cidade}.")
                if 25 <= temperatura <= 35 and humidade >= 70:
                    alertas.append(f"Condições para inundações são atendidas em {cidade}.")
                if (regiao == "Europa" and 25 <= temperatura <= 40 and humidade < 30) or \
                        (regiao == "Ásia" and 35 <= temperatura <= 50 and humidade < 20) or \
                        ((regiao in ["África", "América do Sul", "América do Norte", "América Central",
                                     "Austrália"]) and 30 <= temperatura <= 45 and humidade < 30):
                    alertas.append(f"Condições para secas são atendidas em {cidade}.")
                if not alertas:
                    alertas.append(f"Nenhuma condição meteorológica extrema é atendida em {cidade}.")
            else:
                alertas.append("Região não identificada.")

            for alerta in alertas:
                label_alerta = tk.Label(self.alert_window, text=alerta)
                label_alerta.pack(pady=5)

    # ----
    def email(self):
        if os.path.exists("dados_usuario.json"):
            with open("dados_usuario.json", "r") as f:
                dados_usuario = json.load(f)

            assunto = "Alerta de Catástofre"
            cidade = dados_usuario.get("Morada")
            email = dados_usuario.get("Email")
            latitude, longitude = self.obter_coordenadas(cidade)
            regiao = self.verificar_continente_pelo_nome_da_cidade(cidade)
            if latitude is None or longitude is None:
                messagebox.showerror("Error", "City coordinates could not be found.")
            else:
                response = self.obter_dados_meteo(latitude, longitude)
                hourly = response.get('hourly', {})
                hora_atual = datetime.now(tz=timezone.utc)
                indice_momento_atual = int(
                    (hora_atual - hora_atual.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds() / 3600)

                temperatura = hourly['temperature_2m'][indice_momento_atual]
                humidade = hourly['relative_humidity_2m'][indice_momento_atual]

                alertas = []

                if regiao in ["Europa", "Ásia", "África", "América do Sul", "América do Norte", "América Central",
                              "Austrália"]:
                    if temperatura >= 26 and humidade >= 60:
                        alertas.append(f"Condições para tempestades são atendidas em {cidade}.")
                    if temperatura >= 20 and humidade >= 50:
                        alertas.append(f"Condições para tornados são atendidas em {cidade}.")
                    if 25 <= temperatura <= 35 and humidade >= 70:
                        alertas.append(f"Condições para inundações são atendidas em {cidade}.")
                    if (regiao == "Europa" and 25 <= temperatura <= 40 and humidade < 30) or \
                            (regiao == "Ásia" and 35 <= temperatura <= 50 and humidade < 20) or \
                            ((regiao in ["África", "América do Sul", "América do Norte", "América Central",
                                         "Austrália"]) and 30 <= temperatura <= 45 and humidade < 30):
                        alertas.append(f"Condições para secas são atendidas em {cidade}.")

                if len(alertas) != 0:
                    remetente = 'melhor.grupo.lab.prog@gmail.com'
                    senha = 'dwdv royk tsbe wbyi'
                    mensagem = ""
                    for alerta in alertas:
                        if alerta != alertas[-1]:
                            mensagem = mensagem + alerta + "\n"
                        else:
                            mensagem = mensagem + alerta

                    # Configurando a mensagem
                    msg = MIMEMultipart()
                    msg['From'] = remetente
                    msg['To'] = email
                    msg['Subject'] = assunto
                    msg.attach(MIMEText(mensagem, 'plain'))

                    try:
                        # Conectando ao servidor SMTP do Gmail
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(remetente, senha)
                        texto = msg.as_string()
                        server.sendmail(remetente, email, texto)
                        server.quit()
                        print(f"Email enviado com sucesso para {email}")
                    except Exception as e:
                        print(f"Falha ao enviar o email. Erro: {e}")

    def enviar(self):
        if os.path.exists("dados_usuario.json"):
            with open("dados_usuario.json", "r") as f:
                dados_usuario = json.load(f)

            morada = dados_usuario["Morada"]

            lat, lon = self.obter_coordenadas(morada)
            if lat is None or lon is None:
                print("Cidade não encontrada. Por favor, verifique o nome da cidade e tente novamente.")
                return
            else:
                self.email()

    # -----

    def historico(self):
        self.hist_window = tk.Toplevel(self.root)
        self.hist_window.title("Historico")

        frame = tk.Frame(self.hist_window)
        frame.pack(pady=10, padx=10)

        tk.Label(frame, text="City:").grid(row=0, column=0, pady=5)
        self.entry_city = tk.Entry(frame)
        self.entry_city.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Start Date (DD-MM-YYYY):").grid(row=1, column=0, pady=5)
        self.entry_start_date = tk.Entry(frame)
        self.entry_start_date.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="End Date (DD-MM-YYYY):").grid(row=2, column=0, pady=5)
        self.entry_end_date = tk.Entry(frame)
        self.entry_end_date.grid(row=2, column=1, pady=5)

        button = tk.Button(frame, text="Get Weather", command=self.show_weather)
        button.grid(row=3, columnspan=2, pady=10)

        tree_frame = tk.Frame(self.hist_window)
        tree_frame.pack(pady=10, padx=10)

        columns = ('data', 'temperaturamax', 'temperaturamin', 'precipitação', 'ph')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        # Define headings
        self.tree.heading('data', text='Data')
        self.tree.heading('temperaturamax', text='Temperatura(MAX)')
        self.tree.heading('temperaturamin', text='Temperatura(MIN)')
        self.tree.heading('precipitação', text='Precipitação')
        self.tree.heading('ph', text='Precipitação(Horas)')

        # Define column widths
        self.tree.column('data', width=200)
        self.tree.column('temperaturamax', width=200)
        self.tree.column('temperaturamin', width=200)
        self.tree.column('precipitação', width=200)
        self.tree.column('ph', width=200)

        self.tree.pack()

    @staticmethod
    def is_valid_date(date_str):
        try:
            date = datetime.strptime(date_str, '%d-%m-%Y')
        except ValueError:
            return False, "Date format should be DD-MM-YYYY."

        if date.year < 1940:
            return False, "Year must be 1940 or later."

        if date.month < 1 or date.month > 12:
            return False, "Month must be between 1 and 12."

        if date.day < 1 or date.day > 31:
            return False, "Day must be between 1 and 31."

        if date.month in [4, 6, 9, 11] and date.day > 30:
            return False, "Day must be between 1 and 30 for the selected month."

        if date.month == 2:
            if date.year % 4 == 0 and (date.year % 100 != 0 or date.year % 400 == 0):
                if date.day > 29:
                    return False, "Day must be between 1 and 29 for February in a leap year."
            else:
                if date.day > 28:
                    return False, "Day must be between 1 and 28 for February."

        return True, ""

    @staticmethod
    def arredondar_dados(df):
        return df.round(2)  # Round all values to two decimal places

    def get_weather_data(self, latitude, longitude, start_date, end_date):
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "precipitation_hours"],
            "timezone": "Europe/Berlin"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()['daily']

            daily_data = {
                "date": pd.date_range(
                    start=start_date,
                    end=end_date,
                    freq='D'
                ),
                "temperature_2m_max": data['temperature_2m_max'],
                "temperature_2m_min": data['temperature_2m_min'],
                "precipitation_sum": data['precipitation_sum'],
                "precipitation_hours": data['precipitation_hours']
            }

            df = pd.DataFrame(data=daily_data)
            return self.arredondar_dados(df)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None

    def show_weather(self):
        city = self.entry_city.get()
        start_date_str = self.entry_start_date.get()
        end_date_str = self.entry_end_date.get()

        is_valid, error_msg = self.is_valid_date(start_date_str)
        if not is_valid:
            messagebox.showerror("Start Date Error", error_msg)
            return

        is_valid, error_msg = self.is_valid_date(end_date_str)
        if not is_valid:
            messagebox.showerror("End Date Error", error_msg)
            return

        try:
            start_date = datetime.strptime(start_date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Date conversion error.")
            return

        latitude, longitude = self.obter_coordenadas(city)

        if latitude is None or longitude is None:
            messagebox.showerror("Error", "City not found. Please enter a valid city name.")
            return

        df = self.get_weather_data(latitude, longitude, start_date, end_date)

        if df is not None:
            for i in self.tree.get_children():
                self.tree.delete(i)

            for index, row in df.iterrows():
                self.tree.insert("", "end", values=list(row))


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
