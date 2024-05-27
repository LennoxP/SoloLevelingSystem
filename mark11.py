import json
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Estudante:
    def __init__(self, nome):
        self.nome = nome 
        self.nivel = 1
        self.experiencia = 0
        self.tarefas_completas = 0
        self.total_tarefas = 0
        self.total_experiencia = 0
        self.carregar_progresso()

    def completar_tarefa(self, pontos_experiencia, linguagem, topico):
        self.experiencia += pontos_experiencia
        self.tarefas_completas += 1
        self.total_tarefas += 1
        self.total_experiencia += pontos_experiencia
        if self.experiencia >= 100:
            self.subir_de_nivel()
        self.salvar_progresso()
        # Exibir o popup informando a conclusão da missão
        self.mostrar_popup_missao(linguagem, topico)

    def mostrar_popup_missao(self, linguagem, topico):
        popup = tk.Toplevel(self.root)
        popup.title("Missão Concluída")
        popup.geometry("400x200+400+200")
        mensagem = f"Você completou a missão!\nSua nova habilidade é: {topico} em {linguagem}."
        label = tk.Label(popup, text=mensagem, padx=20, pady=20)
        label.pack(expand=True)


    def completar_tarefa(self, pontos_experiencia):
        self.experiencia += pontos_experiencia
        self.tarefas_completas += 1
        self.total_tarefas += 1
        self.total_experiencia += pontos_experiencia
        if self.experiencia >= 100:
            self.subir_de_nivel()
        self.salvar_progresso()

    def subir_de_nivel(self):
        self.nivel += 1
        self.experiencia = 0
        self.tarefas_completas = 0
        self.mostrar_popup_nivel()
        self.salvar_progresso()

    def mostrar_popup_nivel(self):
        popup = tk.Toplevel()
        popup.overrideredirect(True)
        popup.configure(bg='black')

        # Gera coordenadas aleatórias para a posição da janela
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = random.randint(0, screen_width - 400)  # Ajuste o valor conforme necessário
        y = random.randint(0, screen_height - 200)  # Ajuste o valor conforme necessário
        popup.geometry(f"800x200+{x}+{y}")

        title_bar = tk.Frame(popup, bg='black', relief='raised', bd=0)
        title_bar.pack(fill=tk.X)

        close_button = tk.Button(title_bar, text='X', command=popup.destroy, bg='black', fg='white', bd=0)
        close_button.pack(side=tk.RIGHT)

        label = tk.Label(popup, text=f"Parabéns, {self.nome}! Você subiu para o nível {self.nivel}!",
                         bg='black', fg='#FFD700', font=('Bebas Neue', 18, 'bold'))
        label.pack(expand=True)
        popup.wm_iconbitmap('')  # Remove o ícone da janela pop-up

        close_button = tk.Button(popup, text='Fechar', command=popup.destroy, bg='black', fg='#FFD700', font=('Bebas Neue', 14, 'bold'))
        close_button.pack(pady=10)


    def mostrar_status(self):
        return f"Nome: {self.nome}, Nível: {self.nivel}, Experiência: {self.experiencia}, Tarefas Completas: {self.tarefas_completas}"

    def mostrar_status_completo(self):
        return [
            f"Nome: {self.nome}",
            f"Nível (Atual): {self.nivel}",
            f"Experiência (Atual): {self.experiencia}",
            f"Tarefas Concluídas (Atual): {self.tarefas_completas}",
            f"Tarefas Concluídas (Total): {self.total_tarefas}",
            f"Experiência (Total): {self.total_experiencia}"
        ]

    def salvar_progresso(self):
        progresso = {
            "nome": self.nome,
            "nivel": self.nivel,
            "experiencia": self.experiencia,
            "tarefas_completas": self.tarefas_completas,
            "total_tarefas": self.total_tarefas,
            "total_experiencia": self.total_experiencia
        }
        with open("progresso.json", "w") as arquivo:
            json.dump(progresso, arquivo)

    def carregar_progresso(self):
        if os.path.exists("progresso.json"):
            with open("progresso.json", "r") as arquivo:
                progresso = json.load(arquivo)
                self.nivel = progresso.get("nivel", 1)
                self.experiencia = progresso.get("experiencia", 0)
                self.tarefas_completas = progresso.get("tarefas_completas", 0)
                self.total_tarefas = progresso.get("total_tarefas", 0)
                self.total_experiencia = progresso.get("total_experiencia", 0)

    def resetar_progresso(self):
        self.nivel = 1
        self.experiencia = 0
        self.tarefas_completas = 0
        self.total_tarefas = 0
        self.total_experiencia = 0
        self.salvar_progresso()


    def move_window(self, event, window):
        x = window.winfo_pointerx() - window.offset_x
        y = window.winfo_pointery() - window.offset_y
        window.geometry(f"+{x}+{y}")

    def start_move(self, event, window):
        window.offset_x = event.x
        window.offset_y = event.y

    def center_window(self, window, width=800, height=200, offset=0):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2) + offset
        y = (screen_height // 2) - (height // 2) + offset
        window.geometry(f"{width}x{height}+{x}+{y}")

class GUI:
    def __init__(self, root, sistema_estudo):
        self.root = root
        self.sistema_estudo = sistema_estudo

        # Remove a barra de título
        self.root.overrideredirect(True)
        self.root.configure(bg='black')
        self.root.wm_attributes('-alpha', 0.9)  # Define transparência
        self.center_window(self.root, width=1114, height=580)

        # Adiciona uma barra personalizada
        self.title_bar = tk.Frame(root, bg='black', relief='raised', bd=0)
        self.title_bar.pack(fill=tk.X)

        # Remove o texto "Solo Leveling" do canto superior esquerdo
        self.close_button = tk.Button(self.title_bar, text='X', command=self.root.quit, bg='black', fg='white', bd=0)
        self.close_button.pack(side=tk.RIGHT)

        self.title_bar.bind("<B1-Motion>", lambda event: self.move_window(event, self.root))
        self.title_bar.bind("<Button-1>", lambda event: self.start_move(event, self.root))
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='black', foreground='white', font=('Bebas Neue', 30, 'bold'))
        style.configure('TButton', background='black', foreground='purple', font=('Bebas Neue', 19, 'bold'), borderwidth=0)
        style.map('TButton', background=[('active', 'black')], foreground=[('active', '#BA55D3')], cursor=[('!disabled', 'hand2')])
        self.lbl_nome = ttk.Label(root, text=f"Solo Leveling", foreground='white', font=('Solo Level Demo', 80,))
        self.lbl_nome.pack(pady=10)

        self.btn_gerar_tarefas = ttk.Button(root, text="Gerar Tarefas Diárias", command=self.gerar_tarefas)
        self.btn_gerar_tarefas.pack(pady=10)

        self.tarefas_frame = tk.Frame(root, bg='black')
        self.tarefas_frame.pack(pady=10)

        self.btn_resetar = ttk.Button(root, text="Resetar", command=self.confirmar_resetar_progresso)
        self.btn_resetar.pack(side=tk.LEFT, anchor=tk.SW, padx=10, pady=10)

        self.btn_status = ttk.Button(root, text="Status", command=self.mostrar_status_janela)
        self.btn_status.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)

        self.tarefas_labels = []

    def move_window(self, event, window):
        x = window.winfo_pointerx() - window.offset_x
        y = window.winfo_pointery() - window.offset_y
        window.geometry(f"+{x}+{y}")

    def atualizar_cores(self):
        cor_principal = '#000080' if self.sistema_estudo.estudante.nivel < 50 else '#800080'
        cor_texto_status = 'blue' if self.sistema_estudo.estudante.nivel < 50 else '#800080'

        self.root.configure(bg=cor_principal)
        self.title_bar.configure(bg=cor_principal)
        self.lbl_nome.configure(foreground=cor_principal)
        self.lbl_nome.configure(foreground=cor_texto_status)
        self.btn_resetar.configure(foreground=cor_texto_status)

    def start_move(self, event, window):
        window.offset_x = event.x
        window.offset_y = event.y

    def center_window(self, window, width=800, height=200, offset=0):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2) + offset
        y = (screen_height // 2) - (height // 2) + offset
        window.geometry(f"{width}x{height}+{x}+{y}")

    def gerar_tarefas(self):
        self.sistema_estudo.gerar_tarefas_diarias()
        self.atualizar_tarefas()

    def atualizar_tarefas(self):
        for widget in self.tarefas_frame.winfo_children():
            widget.destroy()

        self.tarefas_labels.clear()

        for linguagem, topico in self.sistema_estudo.obter_tarefas_diarias():
            frame = tk.Frame(self.tarefas_frame, bg='black')
            frame.pack(pady=5, padx=5)

            lbl_linguagem = ttk.Label(frame, text=linguagem, foreground='#DC143C', font=('Bebas Neue', 27, 'bold'))
            lbl_linguagem.pack(side=tk.LEFT, padx=5)

            lbl_topico = ttk.Label(frame, text=topico, foreground='white', font=('Bebas Neue', 20))
            lbl_topico.pack(side=tk.LEFT, padx=5)

            btn_concluir = ttk.Button(frame, text="Concluir", command=lambda l=linguagem, t=topico, f=frame: self.concluir_tarefa(l, t, f))
            btn_concluir.pack(side=tk.RIGHT, padx=5)

            self.tarefas_labels.append((lbl_linguagem, lbl_topico, btn_concluir))

    def concluir_tarefa(self, linguagem, topico, frame):
        self.sistema_estudo.estudante.completar_tarefa(25)
        frame.pack_forget()  # Remove o frame da tarefa

        # Exibir um pop-up ao concluir uma missão
        popup = tk.Toplevel()
        popup.overrideredirect(True)  # Remove a borda da janela
        popup.configure(bg='black')

        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = random.randint(1, screen_width - 400)  # Ajuste o valor conforme necessário
        y = random.randint(1, screen_height - 800)  # Ajuste o valor conforme necessário
        popup.geometry(f"800x200+{x}+{y}")

        label = tk.Label(popup, text=f"Você completou a missão!\nSua nova habilidade é: {topico}", bg='black', fg='#FFD700', font=('Bebas Neue', 18, 'bold'))
        label.pack(expand=True)

        close_button = tk.Button(popup, text='Fechar', command=popup.destroy, bg='black', fg='#FFD700', font=('Bebas Neue', 14, 'bold'))
        close_button.pack(pady=10)

        popup.focus_set()
        popup.grab_set()
        popup.wait_window()


    def mostrar_popup_missao(self, linguagem, topico):
        popup = tk.Toplevel()
        self.center_window(popup, offset=50)
        popup.overrideredirect(True)
        popup.configure(bg='black')

        title_bar = tk.Frame(popup, bg='black', relief='raised', bd=0)
        title_bar.pack(fill=tk.X)

        close_button = tk.Button(title_bar, text='X', command=popup.destroy, bg='black', fg='white', bd=0)
        close_button.pack(side=tk.RIGHT)

        title_bar.bind("<B1-Motion>", lambda event: self.move_window(event, popup))
        title_bar.bind("<Button-1>", lambda event: self.start_move(event, popup))

        label = tk.Label(popup, text=f"Você completou a missão! Sua nova habilidade é: {topico}", bg='black', fg='#FFD700', font=('Bebas Neue', 18, 'bold'))
        label.pack(expand=True)


    def confirmar_resetar_progresso(self):
        popup = tk.Toplevel()
        self.center_window(popup, offset=50)
        popup.overrideredirect(True)
        popup.configure(bg='black')

        title_bar = tk.Frame(popup, bg='black', relief='raised', bd=0)
        title_bar.pack(fill=tk.X)

        close_button = tk.Button(title_bar, text='X', command=popup.destroy, bg='black', fg='white', bd=0)
        close_button.pack(side=tk.RIGHT)

        title_bar.bind("<B1-Motion>", lambda event: self.move_window(event, popup))
        title_bar.bind("<Button-1>", lambda event: self.start_move(event, popup))

        label = tk.Label(popup, text="Você tem certeza que deseja resetar seu progresso?",
                        bg='black', fg='#FFD700', font=('Bebas Neue', 18, 'bold'))
        label.pack(pady=20)

        frame = tk.Frame(popup, bg='black')
        frame.pack(pady=10)

        btn_sim = ttk.Button(frame, text="Sim", command=lambda: [self.sistema_estudo.estudante.resetar_progresso(), popup.destroy()])
        btn_sim.pack(side=tk.LEFT, padx=10)

        btn_nao = ttk.Button(frame, text="Não", command=popup.destroy)
        btn_nao.pack(side=tk.RIGHT, padx=10)

    def mostrar_status_janela(self):
        popup = tk.Toplevel()
        self.center_window(popup, width=700, height=500, offset=50)
        popup.overrideredirect(True)
        popup.configure(bg='black')

        title_bar = tk.Frame(popup, bg='black', relief='raised', bd=0)
        title_bar.pack(fill=tk.X)

        close_button = tk.Button(title_bar, text='X', command=popup.destroy, bg='black', fg='white', bd=0)
        close_button.pack(side=tk.RIGHT)

        title_bar.bind("<B1-Motion>", lambda event: self.move_window(event, popup))
        title_bar.bind("<Button-1>", lambda event: self.start_move(event, popup))

        status_text = "\n".join(self.sistema_estudo.estudante.mostrar_status_completo())
        color = '#000080' if self.sistema_estudo.estudante.nivel < 50 else '#800080'
        label = tk.Label(popup, text=status_text, bg='black', fg=color, font=('Pixellari', 20, 'bold'))
        label.pack(expand=True, padx=20, pady=20)

import random

class SistemaEstudo:
    def __init__(self, estudante):
        self.estudante = estudante
        self.linguagens = {
            "Python": {
                "iniciante": [
"Hello World",
"Operações matemáticas básicas","Concatenar strings","Conversão de tipos de dados","Uso de variáveis",
"Entrada do usuário",
"Condicionais (if, elif, else)",
"Loops (for, while)",
"Listas",
"Tuplas",
"Conjuntos (sets)",
"Dicionários",
"Funções",
"Compreensão de listas",
"Manipulação de strings",
"Formatação de strings (f-strings)",
"Métodos de listas",
"Métodos de dicionários",
"Operadores lógicos",
"Operadores de comparação",
"Manipulação de arquivos (leitura/escrita)",
"Tratamento de exceções",
"Módulos e pacotes",
"Uso do módulo math",
"Uso do módulo datetime",
"Uso do módulo os",
"Uso do módulo sys",
"Uso do módulo random"
                ],
                "avancado": [
"Classes e objetos",
"Herança",
"Polimorfismo",
"Encapsulamento",
"Métodos estáticos e de classe",
"Sobrecarga de operadores",
"Geradores",
"Iteradores",
"Expressões lambda",
"Funções de alta ordem (map, filter, reduce)",
"Decoração de funções (decorators)",
"Programação assíncrona (asyncio)",
"Uso de bibliotecas externas (ex: requests)",
"Criação de pacotes instaláveis",
"Documentação de código (docstrings)",
"Testes unitários (unittest)",
"Testes com pytest",
"Testes de desempenho",
"Manipulação de JSON",
"Manipulação de CSV",
"Uso do SQLite",
"Uso do SQLAlchemy",
"Scraping de sites (BeautifulSoup, Scrapy)",
"Automação de tarefas (ex: com Selenium)",
"Criação de APIs REST (ex: Flask, FastAPI)",
"Criação de interfaces gráficas (ex: Tkinter, PyQt)",
"Trabalhando com dataframes (pandas)",
"Visualização de dados (matplotlib, seaborn)",
"Análise de dados",
"Machine Learning (scikit-learn)",
"Deep Learning (TensorFlow, PyTorch)",
"Processamento de imagem (OpenCV)",
"Processamento de linguagem natural (NLTK, spaCy)",
"Jogos 2D (Pygame)",
"Uso de ambientes virtuais (venv, virtualenv)",
"Controle de versão com Git",
"Automação de builds (ex: Makefile, tox)",
"Desenvolvimento orientado a testes (TDD)",
"Design patterns (Padrões de projeto)",
"Práticas de Clean Code",
"Refatoração de código",
"Benchmarking",
"Profiling",
"Otimização de código",
"Uso de logs",
"Serialização de objetos (pickle)",
"Segurança em aplicações Python",
"Trabalhando com sockets",
"Programação de rede",
"Conexões com APIs externas",
"Uso de Websockets",
"Threading e multiprocessing",
"Análise estática de código (pylint, flake8)",
"Programação funcional",
"Design de bancos de dados",
"ORMs (Object-Relational Mapping)",
"Deploy de aplicações Python",
"Uso de Docker com Python",
"Automação de deploy (ex: Ansible, Jenkins)",
"Criação de bots (ex: Discord, Telegram)",
"Criação de CLI (Command Line Interface)",
"Desenvolvimento de plugins",
"Customização do interpretador Python",
"Uso de ctypes e CFFI",
"Binding de C/C++ com Python (ex: SWIG, pybind11)",
"Interoperabilidade com outras linguagens",
"Análise de logs",
"Programação orientada a aspectos",
"Criação de testes de integração",
"Criação de dashboards",
"Manipulação de dados geoespaciais (ex: GeoPandas)",
"Análise de séries temporais",
"Uso de Jupyter Notebooks",
"Criação de extensões para Jupyter",
"APIs GraphQL com Python",
"Aplicações serverless (ex: AWS Lambda)",
"Criação de pacotes PyPI",
"Gerenciamento de dependências (pip, pipenv)",
"Criação de serviços de backend",
"Microserviços com Python",
"Desenvolvimento full-stack com Python",
"Boas práticas de desenvolvimento",
"Automação de testes",
"Testes end-to-end",
"Versionamento semântico",
"Continuous Integration/Continuous Deployment (CI/CD)",
"Monitoramento de aplicações",
"Logging e monitoramento",
"Trabalho com arquivos binários",
"Manipulação de XML",
"Autenticação e autorização",
"OAuth com Python",
"Trabalhando com queues (RabbitMQ, Kafka)",
"Trabalhando com streams",
"Desenvolvimento de middlewares",
"Criação de pipelines de dados",
"Big Data com Python",
"Trabalho com NoSQL (ex: MongoDB)",
"Desenvolvimento de chatbots",
"Reconhecimento de fala",
"Síntese de fala",
"Trabalho com RFID/NFC",
"Automação industrial com Python",
"Desenvolvimento de firmware",
"Programação de sistemas embarcados",
"Uso de Arduino com Python",
"Desenvolvimento de aplicações mobile (ex: Kivy, BeeWare)",
"Criação de scripts para automação diária",
"Criação de ferramentas de linha de comando",
"Internacionalização e localização",
"Debugging avançado",
"Análise de desempenho",
"Uso de ferramentas de qualidade de código",
"Programação defensiva",
"Análise forense de dados",
"Criptografia e segurança de dados",
"Trabalhando com blockchain",
"Desenvolvimento de smart contracts",
"Aplicações em fintech",
"Simulação de sistemas",
"Trabalho com redes neurais artificiais",
"Criação de assistentes virtuais",
"Reconhecimento de padrões",
"Classificação de dados",
"Regressão linear e logística",
"Análise de clusters",
"Redes Bayesianas",
"Aprendizado por reforço",
"Processamento paralelo e distribuído",
"Programação concorrente",
"Trabalho com GPUs (ex: CUDA)",
"Criação de gráficos interativos",
"Programação orientada a eventos",
"Análise de risco",
"Análise preditiva",
"Construção de modelos preditivos",
"Modelagem estatística",
"Automação de planilhas"
                ]
            },
            "JavaScript": {
                "iniciante": [
"Hello World",
"Variáveis e tipos de dados",
"Operadores aritméticos",
"Operadores de atribuição",
"Operadores de comparação",
"Operadores lógicos",
"Condicionais (if, else, else if)",
"Loops (for, while)",
"Arrays",
"Objetos (JSON)",
"Funções",
"Escopo de variáveis",
"Manipulação de strings",
"Manipulação de arrays (push, pop, splice, etc.)",
"Template literals",
"Arrow functions",
"Callback functions",
"Promises (Promise, then, catch)",
"Fetch API (GET, POST, PUT, DELETE)",
"Manipulação do DOM (document.getElementById, etc.)",
"Eventos do DOM (click, input, submit, etc.)",
"SetInterval e setTimeout",
"LocalStorage e SessionStorage",
"Formulários (validação, envio, etc.)",
"Tratamento de erros (try, catch, finally)",
"Closures",
"Operador spread",
"Destructuring",
"Classes e herança",
"Módulos (import/export)",
"Async/Await",
"Map, filter, reduce",
"Expressões regulares (RegExp)",
"Date e manipulação de datas",
"Operações assíncronas com callbacks",
"Manipulação de JSON",
"Requisições AJAX"
                ],
                "avancado": [
"EventEmitter",
"Streams",
"WebSockets",
"WebRTC",
"Service Workers",
"Web Workers",
"Progressive Web Apps (PWA)",
"Testing (Jest, Mocha, Jasmine)",
"Node.js (FS, HTTP, etc.)",
"Frameworks frontend (React, Vue, Angular)",
"Frameworks backend (Express, Koa, NestJS)",
"GraphQL",
"RESTful APIs",
"WebSockets em tempo real",
"Autenticação e autorização (JWT)",
"Segurança de aplicações web",
"Testes de integração",
"Testes end-to-end",
"Testes de unidade",
"CI/CD (Jenkins, Travis CI)",
"Desenvolvimento de plugins",
"Design patterns",
"Deploy de aplicações",
"Microserviços",
"Arquitetura de software",
"WebAssembly",
"Serverless",
"Big Data (Hadoop, Spark)",
"Machine Learning (TensorFlow, Keras)",
"Reconhecimento de voz",
"Processamento de linguagem natural",
"Blockchain (Ethereum, Solidity)",
"Realidade virtual (VR)",
"Realidade aumentada (AR)",
"Desenvolvimento de jogos",
"Programação gráfica 3D (Three.js, WebGL)",
"IoT (Internet das Coisas)",
"Integração com APIs externas",
"Controle de versionamento (Git)",
"Desenvolvimento mobile (React Native, NativeScript)",
"Desenvolvimento desktop (Electron)",
"Web scraping",
"Automatização de tarefas",
"Gerenciamento de projetos (Scrum, Kanban)",
"Design de interfaces",
"Animações (CSS, JS)",
"SEO (Search Engine Optimization)",
"Marketing digital",
"Analytics e métricas",
"UX/UI Design",
"Análise de dados",
"Visualização de dados (D3.js, Chart.js)",
"Game design",
"Design responsivo",
"Compatibilidade cross-browser",
"Localização e internacionalização",
"Testes de usabilidade",
"Prototipação",
"Design Thinking",
"Arquitetura de informação",
"Empreendedorismo",
"Negócios digitais",
"Monetização de projetos",
"Pitching de projetos",
"Networking",
"Gestão de equipe"
                ]
            },
            "Java": {
                "iniciante": [
"Hello World",
"Variáveis e tipos de dados",
"Operadores aritméticos",
"Operadores de atribuição",
"Operadores de comparação",
"Operadores lógicos",
"Estruturas condicionais (if, else if, else)",
"Estruturas de repetição (for, while, do-while)",
"Arrays unidimensionais",
"Arrays multidimensionais",
"Manipulação de strings",
"Funções (métodos)",
"Passagem de parâmetros",
"Escopo de variáveis",
"Conversão de tipos de dados",
"Operador ternário",
"Switch-case",
"Construtores",
"Métodos getters e setters",
                ],
                "avancado": [
"Herança",
"Polimorfismo",
"Encapsulamento",
"Interfaces",
"Classes abstratas",
"Modificadores de acesso (public, private, protected)",
"Coleções (ArrayList, LinkedList, etc.)",
"Manipulação de coleções (add, remove, etc.)",
"Mapas (HashMap, TreeMap, etc.)",
"Tratamento de exceções (try-catch)",
"Exceções personalizadas",
"Leitura e escrita de arquivos",
"Serialização e desserialização de objetos",
"Enumerações",
"Data e hora (Date, Calendar)",
"Expressões regulares (Regex)",
"Operações com datas (LocalDate, LocalDateTime, etc.)",
"Threads (Runnable, Thread, etc.)",
"Sincronização de threads",
"Concorrência em Java",
"Streams (InputStream, OutputStream)",
"Leitura e escrita em arquivos",
"Entrada e saída de dados (Scanner, Console)",
"Operações de entrada e saída de bytes",
"Manipulação de diretórios e arquivos",
"JavaFX (Interface Gráfica)",
"Eventos de interface",
"Layouts em JavaFX",
"Controles em JavaFX (Button, TextField, etc.)",
"Listeners em JavaFX",
"Threads em JavaFX",
"Trabalhando com tabelas (TableView)",
"Persistência de dados em JavaFX",
"Gráficos em JavaFX",
"Animações em JavaFX",
"Desenvolvimento Web (Servlets, JSP, etc.)",
"Conexão com banco de dados (JDBC)",
"Frameworks MVC (Spring, Hibernate, etc.)",
"Desenvolvimento de aplicações desktop (Swing, AWT)",
"Desenvolvimento de applets",
"Desenvolvimento de aplicações mobile (Android Studio)",
"Desenvolvimento de jogos em Java",
"Testes unitários (JUnit)",
"Documentação de código (Javadoc)",
"Manipulação de JSON em Java",
"Consumo de APIs REST em Java",
"Autenticação em Java",
"Autorização em Java",
"Segurança em Java",
"Gerenciamento de sessões e cookies",
"Trabalhando com protocolos de rede (TCP/IP, UDP)",
"Comunicação cliente-servidor em Java",
"Desenvolvimento de sistemas distribuídos",
"Desenvolvimento de sistemas concorrentes",
"Padrões de projeto em Java",
"Refatoração de código",
"Depuração de código (debugging)",
"Desenvolvimento orientado a testes (TDD)",
"Desenvolvimento ágil (Scrum, Kanban)",
"Controle de versão (Git, SVN)",
"Integração contínua (Jenkins, Maven, etc.)",
"Desenvolvimento de APIs (RESTful, SOAP)",
"Desenvolvimento de microserviços",
"Arquitetura de software em Java",
"Design Patterns em Java",
"Modelagem de dados",
"Modelagem de banco de dados (ER, UML)",
"Gerenciamento de banco de dados (MySQL, PostgreSQL, etc.)",
"ORM (Object-Relational Mapping)",
"Análise e otimização de desempenho",
"Segurança de aplicações Java",
"Desenvolvimento de aplicações web responsivas",
"Desenvolvimento de aplicações escaláveis",
"Desenvolvimento de aplicações multiplataforma",
"Desenvolvimento de sistemas embarcados",
"Desenvolvimento de IoT (Internet of Things)",
"Inteligência artificial em Java",
"Aprendizado de máquina (Machine Learning)",
"Redes neurais em Java",
"Processamento de linguagem natural (NLP)",
"Análise de dados em tempo real",
"Visualização de dados em Java",
"Big Data em Java",
"Computação em nuvem com Java",
"Desenvolvimento de sistemas financeiros",
"Desenvolvimento de sistemas de saúde",
"Desenvolvimento de sistemas educacionais",
"Desenvolvimento de sistemas de e-commerce",
"Desenvolvimento de sistemas de gerenciamento",
"Desenvolvimento de sistemas de logística",
"Desenvolvimento de sistemas de entretenimento",
"Desenvolvimento de sistemas de segurança",
"Desenvolvimento de sistemas de telecomunicações",
"Desenvolvimento de sistemas de viagens",
"Desenvolvimento de sistemas de transporte",
"Desenvolvimento de sistemas de energia",
"Desenvolvimento de sistemas de automação",
"Desenvolvimento de sistemas de robótica",
"Desenvolvimento de sistemas de análise de dados",
"Desenvolvimento de sistemas de IoT industrial",
"Desenvolvimento de sistemas de jogos",
"Desenvolvimento de sistemas de realidade virtual",
"Desenvolvimento de sistemas de realidade aumentada",
"Desenvolvimento de sistemas de inteligência artificial"
                ]
            },
            "C#": {
                "iniciante": [
"Hello World",
"Variáveis e tipos de dados",
"Operadores aritméticos",
"Operadores de atribuição",
"Operadores de comparação",
"Operadores lógicos",
"Estruturas condicionais (if, else if, else)",
"Estruturas de repetição (for, while, do-while)",
"Arrays unidimensionais",
"Arrays multidimensionais",
"Manipulação de strings",
"Funções (métodos)",
"Passagem de parâmetros",
"Escopo de variáveis",
"Conversão de tipos de dados",
"Operador ternário",
"Switch-case",
"Construtores",
"Métodos getters e setters"
                ],
                "avancado": [
"Herança",
"Polimorfismo",
"Encapsulamento",
"Interfaces",
"Classes abstratas",
"Modificadores de acesso (public, private, protected)",
"Coleções (List, Dictionary, etc.)",
"Manipulação de coleções (Add, Remove, etc.)",
"Tratamento de exceções (try-catch)",
"Exceções personalizadas",
"Leitura e escrita de arquivos",
"Serialização e desserialização de objetos",
"Enumerações",
"Data e hora (DateTime, TimeSpan, etc.)",
"Expressões regulares (Regex)",
"Operações com datas (DateTime.Parse, etc.)",
"Threads (Thread, Task, etc.)",
"Sincronização de threads",
"Concorrência em C#",
"Streams"
                ]
            },
            "Machine Learning": {
                "iniciante": [
"Introdução ao Machine Learning",
"Entendimento dos dados (Exploratory Data Analysis)",
"Pré-processamento de dados (limpeza, normalização, etc.)",
"Treinamento de modelos simples (Regressão Linear, Regressão Logística)",
"Avaliação de modelos de Machine Learning",
"Validação cruzada (Cross-Validation)",
"Feature Engineering básico",
"Classificação binária",
"Classificação multiclasse",
"Classificação com Árvores de Decisão",
"Classificação com Random Forest",
"Classificação com k-Nearest Neighbors (k-NN)",
"Classificação com Support Vector Machines (SVM)",
"Regressão com Árvores de Decisão",
"Regressão com Random Forest",
"Regressão com Support Vector Machines (SVM)",
"Clusterização básica (k-Means)",
"Aprendizado supervisionado",
"Aprendizado não supervisionado",
"Aprendizado semi-supervisionado",
"Aprendizado por reforço básico",
"Introdução ao Deep Learning",
"Redes neurais simples (perceptrons)",
"Redes neurais feedforward",
"Modelos de linguagem básicos",
"Introdução ao processamento de linguagem natural (NLP)",
"Análise de sentimentos básica",
"Reconhecimento de padrões básico",
"Visão computacional básica",
"Processamento de imagens simples",
"Aplicações básicas de Machine Learning"
                ],
                "avancado": [
"Redes neurais profundas (Deep Learning)",
"Redes neurais convolucionais (CNN)",
"Redes neurais recorrentes (RNN)",
"Transfer Learning",
"Redes neurais pré-treinadas",
"Modelos de linguagem avançados",
"Transformers (BERT, GPT)",
"Generative Adversarial Networks (GANs)",
"Detecção de objetos em imagens",
"Segmentação de imagens",
"Análise de vídeo",
"Reconhecimento facial",
"Reconhecimento de voz",
"Processamento de áudio",
"Sumarização de texto",
"Tradução automática",
"Recomendação de conteúdo",
"Sistemas de recomendação avançados",
"Integração de modelos de Machine Learning em aplicações",
"Análise de séries temporais",
"Análise de dados complexos",
"Previsão de tendências",
"Previsão de demanda",
"Análise de risco",
"Análise de fraudes",
"Personalização de produtos e serviços",
"Automatização de processos",
"Aplicações de Machine Learning em medicina",
"Aplicações de Machine Learning em finanças",
"Aplicações de Machine Learning em segurança cibernética",
"Aplicações de Machine Learning em automação industrial",
"Aplicações de Machine Learning em veículos autônomos",
"Aplicações de Machine Learning em assistentes virtuais",
"Aplicações de Machine Learning em pesquisa científica",
"Aplicações de Machine Learning em jogos",
"Aplicações de Machine Learning em simulações",
"Aplicações de Machine Learning em bioinformática",
"Aplicações de Machine Learning em análise de dados geoespaciais"
                ]
            }
        }
        self.tarefas_diarias = []

    def gerar_tarefas_diarias(self):
        self.tarefas_diarias.clear()
        while len(self.tarefas_diarias) < 4:
            linguagem, niveis = random.choice(list(self.linguagens.items()))
            topicos = niveis["avancado"] if self.estudante.nivel >= 50 else niveis["iniciante"]
            topico = random.choice(topicos)
            tarefa = (linguagem, topico)
            if tarefa not in self.tarefas_diarias:
                self.tarefas_diarias.append(tarefa)

    def obter_tarefas_diarias(self):
        return self.tarefas_diarias

if __name__ == "__main__":
    root = tk.Tk()
    estudante = Estudante("Uchida")
    sistema_estudo = SistemaEstudo(estudante)

    gui = GUI(root, sistema_estudo)
    root.mainloop()

import tkinter as tk

root = tk.Tk()