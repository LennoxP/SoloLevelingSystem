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
        self.carregar_progresso()

    def completar_tarefa(self, pontos_experiencia):
        self.experiencia += pontos_experiencia
        self.tarefas_completas += 1
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
        popup.geometry("800x200")
        popup.configure(bg='black')

        title_bar = tk.Frame(popup, bg='black', relief='raised', bd=0)
        title_bar.pack(fill=tk.X)

        close_button = tk.Button(title_bar, text='X', command=popup.destroy, bg='black', fg='white', bd=0)
        close_button.pack(side=tk.RIGHT)        

        label = tk.Label(popup, text=f"Parabéns, {self.nome}! Você subiu para o nível {self.nivel}!",
                         bg='black', fg='#FFD700', font=('Bebas Neue', 18, 'bold'))
        label.pack(expand=True)
        popup.wm_iconbitmap('')  # Remove o ícone da janela pop-up

    def mostrar_status(self):
        return f"Nome: {self.nome}, Nível: {self.nivel}, Experiência: {self.experiencia}, Tarefas Completas: {self.tarefas_completas}"

    def salvar_progresso(self):
        progresso = {
            "nome": self.nome,
            "nivel": self.nivel,
            "experiencia": self.experiencia,
            "tarefas_completas": self.tarefas_completas
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

    def resetar_progresso(self):
        self.nivel = 1
        self.experiencia = 0
        self.tarefas_completas = 0
        self.salvar_progresso()

class GUI:
    def __init__(self, root, sistema_estudo):
        self.root = root
        self.sistema_estudo = sistema_estudo

        # Remove a barra de título
        self.root.overrideredirect(True)
        self.root.geometry("1114x580")
        self.root.configure(bg='black')
        self.root.wm_attributes('-alpha', 0.9)  # Define transparência

        # Adiciona uma barra personalizada
        self.title_bar = tk.Frame(root, bg='black', relief='raised', bd=0)
        self.title_bar.pack(fill=tk.X)

        # Remove o texto "Solo Leveling" do canto superior esquerdo
        self.close_button = tk.Button(self.title_bar, text='X', command=self.root.quit, bg='black', fg='white', bd=0)
        self.close_button.pack(side=tk.RIGHT)

        self.title_bar.bind("<B1-Motion>", self.move_window)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='black', foreground='white', font=('Bebas Neue', 30, 'bold'))
        style.configure('TButton', background='black', foreground='#FFD700', font=('Bebas Neue', 15, 'bold'))
        style.map('TButton', background=[('active', 'black')], foreground=[('active', '#FFD700')])

        self.lbl_nome = ttk.Label(root, text=f"Solo Leveling", foreground='white', font=('Solo Level Demo', 70,))
        self.lbl_nome.pack(pady=10)

        self.lbl_status = ttk.Label(root, text=sistema_estudo.estudante.mostrar_status(), foreground='#4169E1', font=('Bebas Neue', 18, 'bold'))
        self.lbl_status.pack(pady=10)

        self.btn_gerar_tarefas = ttk.Button(root, text="Gerar Tarefas Diárias", command=self.gerar_tarefas)
        self.btn_gerar_tarefas.pack(pady=10)

        self.tarefas_frame = tk.Frame(root, bg='black')
        self.tarefas_frame.pack(pady=10)

        self.btn_resetar = ttk.Button(root, text="Resetar", command=self.resetar_progresso)
        self.btn_resetar.pack(side=tk.LEFT, anchor=tk.SW, padx=10, pady=10)

        self.tarefas_labels = []

    def move_window(self, event, window=None):
        if window is None:
            window = self.root
        x = window.winfo_pointerx() - window.offset_x
        y = window.winfo_pointery() - window.offset_y
        window.geometry(f"+{x}+{y}")

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

            lbl_linguagem = ttk.Label(frame, text=linguagem, foreground='red', font=('Bebas Neue', 20, 'bold'))
            lbl_linguagem.pack(side=tk.LEFT, padx=5)

            lbl_topico = ttk.Label(frame, text=f": {topico}", foreground='white', font=('Bebas Neue', 20, 'bold'))
            lbl_topico.pack(side=tk.LEFT, padx=5)

            btn_concluir = ttk.Button(frame, text="Concluir", command=lambda l=lbl_linguagem, t=topico: self.concluir_tarefa(l, t))
            btn_concluir.pack(side=tk.LEFT, padx=5)

            self.tarefas_labels.append((lbl_linguagem, lbl_topico, btn_concluir))

        self.lbl_status.config(text=self.sistema_estudo.estudante.mostrar_status())

    def concluir_tarefa(self, lbl, topico):
        lbl.config(text=f"{lbl.cget('text')} - Concluído")
        lbl.master.winfo_children()[2].config(state=tk.DISABLED)
        self.sistema_estudo.estudante.completar_tarefa(25)
        self.mostrar_popup_missao_concluida(topico)
        self.lbl_status.config(text=self.sistema_estudo.estudante.mostrar_status())

    def mostrar_popup_missao_concluida(self, habilidade):
        popup = tk.Toplevel()
        popup.overrideredirect(True)
        popup.geometry("800x200")
        popup.configure(bg='black')

        title_bar = tk.Frame(popup, bg='black', relief='raised', bd=0)
        title_bar.pack(fill=tk.X)

        close_button = tk.Button(title_bar, text='X', command=popup.destroy, bg='black', fg='white', bd=0)
        close_button.pack(side=tk.RIGHT)

        title_bar.bind("<B1-Motion>", lambda event: self.move_window(event, popup))

        label = tk.Label(popup, text=f"Missão Concluída! Sua nova habilidade é criar uma {habilidade}.",
                         bg='black', fg='#FFD700', font=('Bebas Neue', 18, 'bold'))
        label.pack(expand=True)

    def resetar_progresso(self):
        resposta = messagebox.askyesno("Resetar Progresso", "Você tem certeza que deseja resetar seu progresso?")
        if resposta:
            self.sistema_estudo.estudante.resetar_progresso()
            self.lbl_status.config(text=self.sistema_estudo.estudante.mostrar_status())
            self.gerar_tarefas()

import random

class SistemaEstudo:
    def __init__(self, estudante):
        self.estudante = estudante
        self.linguagens = {
            "Python": {
                "iniciante": [
                    "Sintaxe Básica", "Estruturas de Controle", "Funções", "POO", "Bibliotecas", 
                    "Manipulação de Arquivos", "Exceções", "Decoradores", "Geradores", "Concurrency"
                ],
                "avancado": [
                    "Desenvolvimento de um sistema de gerenciamento de projetos", "Implementação de algoritmos avançados", 
                    "Criação de um aplicativo web completo", "Análise de dados e visualização", "Web scraping", 
                    "Criação de um aplicativo GUI"
                ]
            },
            "JavaScript": {
                "iniciante": [
                    "Sintaxe Básica", "DOM", "ES6+", "Node.js", "Frameworks", 
                    "Event Loop", "Promises", "Async/Await", "APIs", "Websockets"
                ],
                "avancado": [
                    "Desenvolvimento de um framework front-end", "Construção de um servidor completo com Node.js", 
                    "Implementação de segurança em aplicações web", "Otimização de performance em aplicações complexas"
                ]
            },
            "Java": {
                "iniciante": [
                    "Sintaxe Básica", "Estruturas de Controle", "OOP", "Coleções", "Streams", 
                    "JVM", "Multithreading", "JavaFX", "JDBC", "Spring Framework"
                ],
                "avancado": [
                    "Desenvolvimento de um sistema distribuído", "Implementação de microsserviços", 
                    "Otimização de desempenho para aplicações enterprise", "Análise e design de sistemas complexos"
                ]
            },
            "C#": {
                "iniciante": [
                    "Sintaxe Básica", "Estruturas de Controle", "OOP", "LINQ", "Async/Await", 
                    "Entity Framework", "WPF", "ASP.NET Core", "Delegates", "Eventos"
                ],
                "avancado": [
                    "Desenvolvimento de aplicações multi-threaded avançadas", "Construção de APIs RESTful com ASP.NET Core", 
                    "Implementação de arquitetura MVVM em aplicações WPF", "Otimização de desempenho em aplicações C#"
                ]
            },
            "Ruby": {
                "iniciante": [
                    "Sintaxe Básica", "Estruturas de Controle", "OOP", "Blocks", "Metaprogramming", 
                    "Ruby on Rails", "Gems", "File I/O", "Concurrency", "Modules"
                ],
                "avancado": [
                    "Desenvolvimento de aplicações com Ruby on Rails avançadas", "Implementação de background jobs com Sidekiq", 
                    "Otimização de performance em aplicações Ruby", "Metaprogramação avançada em Ruby"
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

    root.offset_x = 0
    root.offset_y = 0

    def on_start(event):
        root.offset_x = event.x
        root.offset_y = event.y

    gui = GUI(root, sistema_estudo)
    root.bind("<Button-1>", on_start)
    root.mainloop()
