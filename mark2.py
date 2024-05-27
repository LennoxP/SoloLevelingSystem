import json
import os

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
        print(f"Parabéns, {self.nome}! Você subiu para o nível {self.nivel}!")
        self.salvar_progresso()

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


import random

class SistemaEstudo:
    def __init__(self, estudante):
        self.estudante = estudante
        self.linguagens = {
            "Python": [
                "Sintaxe Básica", "Estruturas de Controle", "Funções", "POO", "Bibliotecas", 
                "Manipulação de Arquivos", "Exceções", "Decoradores", "Geradores", "Concurrency"
            ],
            "JavaScript": [
                "Sintaxe Básica", "DOM", "ES6+", "Node.js", "Frameworks", 
                "Event Loop", "Promises", "Async/Await", "APIs", "Websockets"
            ],
            "Java": [
                "Sintaxe Básica", "Estruturas de Controle", "OOP", "Coleções", "Streams", 
                "JVM", "Multithreading", "JavaFX", "JDBC", "Spring Framework"
            ],
            "C#": [
                "Sintaxe Básica", "Estruturas de Controle", "OOP", "LINQ", "Async/Await", 
                "Entity Framework", "WPF", "ASP.NET Core", "Delegates", "Eventos"
            ],
            "Ruby": [
                "Sintaxe Básica", "Estruturas de Controle", "OOP", "Blocks", "Metaprogramming", 
                "Ruby on Rails", "Gems", "File I/O", "Concurrency", "Modules"
            ]
        }
        self.tarefas_diarias = []

    def gerar_tarefas_diarias(self):
        self.tarefas_diarias.clear()
        while len(self.tarefas_diarias) < 4:
            linguagem, topicos = random.choice(list(self.linguagens.items()))
            topico = random.choice(topicos)
            tarefa = (linguagem, topico)
            if tarefa not in self.tarefas_diarias:
                self.tarefas_diarias.append(tarefa)

    def obter_tarefas_diarias(self):
        return self.tarefas_diarias

import tkinter as tk
from tkinter import ttk, messagebox

class GUI:
    def __init__(self, root, sistema_estudo):
        self.root = root
        self.sistema_estudo = sistema_estudo

        self.root.title("Sistema de Estudos - Solo Leveling")
        self.root.geometry("500x500")
        self.root.configure(bg='black')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='black', foreground='yellow', font=('Helvetica', 12, 'bold'))
        style.configure('TButton', background='black', foreground='yellow', font=('Helvetica', 10, 'bold'))
        style.map('TButton', background=[('active', 'black')], foreground=[('active', 'yellow')])

        self.lbl_nome = ttk.Label(root, text=f"Estudante: {sistema_estudo.estudante.nome}")
        self.lbl_nome.pack(pady=10)

        self.lbl_status = ttk.Label(root, text=sistema_estudo.estudante.mostrar_status())
        self.lbl_status.pack(pady=10)

        self.btn_gerar_tarefas = ttk.Button(root, text="Gerar Tarefas Diárias", command=self.gerar_tarefas)
        self.btn_gerar_tarefas.pack(pady=10)

        self.tarefas_frame = ttk.Frame(root)
        self.tarefas_frame.pack(pady=10)

        self.btn_resetar = ttk.Button(root, text="Resetar", command=self.resetar_progresso)
        self.btn_resetar.pack(side=tk.LEFT, anchor=tk.SW, padx=10, pady=10)

        self.tarefas_labels = []

    def gerar_tarefas(self):
        self.sistema_estudo.gerar_tarefas_diarias()
        self.atualizar_tarefas()

    def atualizar_tarefas(self):
        for widget in self.tarefas_frame.winfo_children():
            widget.destroy()

        self.tarefas_labels.clear()

        for linguagem, topico in self.sistema_estudo.obter_tarefas_diarias():
            frame = ttk.Frame(self.tarefas_frame)
            frame.pack(pady=5)

            lbl = ttk.Label(frame, text=f"{linguagem}: {topico}")
            lbl.pack(side=tk.LEFT, padx=5)

            btn_concluir = ttk.Button(frame, text="Concluir", command=lambda l=lbl: self.concluir_tarefa(l))
            btn_concluir.pack(side=tk.LEFT, padx=5)

            self.tarefas_labels.append((lbl, btn_concluir))

        self.lbl_status.config(text=self.sistema_estudo.estudante.mostrar_status())

    def concluir_tarefa(self, lbl):
        lbl.config(text=f"{lbl.cget('text')} - Concluído")
        lbl.master.winfo_children()[1].config(state=tk.DISABLED)
        self.sistema_estudo.estudante.completar_tarefa(25)
        self.lbl_status.config(text=self.sistema_estudo.estudante.mostrar_status())
        if self.sistema_estudo.estudante.experiencia >= 100:
            self.sistema_estudo.estudante.subir_de_nivel()
            self.lbl_status.config(text=self.sistema_estudo.estudante.mostrar_status())

    def resetar_progresso(self):
        resposta = messagebox.askyesno("Resetar Progresso", "Você tem certeza que deseja resetar seu progresso?")
        if resposta:
            self.sistema_estudo.estudante.resetar_progresso()
            self.lbl_status.config(text=self.sistema_estudo.estudante.mostrar_status())
            self.gerar_tarefas()

if __name__ == "__main__":
    root = tk.Tk()
    estudante = Estudante("Uchida")
    sistema_estudo = SistemaEstudo(estudante)
    gui = GUI(root, sistema_estudo)
    root.mainloop()
