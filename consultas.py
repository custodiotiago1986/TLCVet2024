import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class AbrirConsultaWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Inserir Consulta")
        self.geometry("500x180")
        
        # Label e Combobox para selecionar o paciente
        tk.Label(self, text="Selecione o Paciente:").pack()
        self.paciente_combo = ttk.Combobox(self, state="readonly")
        self.paciente_combo.pack()
        self.carregar_pacientes()  # Carregar os pacientes disponíveis
        
        # Label e Entry para a data da consulta
        tk.Label(self, text="Data da Consulta:").pack()
        self.data_entry = tk.Entry(self)
        self.data_entry.pack()
        
        # Label e Entry para o motivo da consulta
        tk.Label(self, text="Motivo da Consulta:").pack()
        self.motivo_entry = tk.Entry(self)
        self.motivo_entry.pack()
        
        # Botões Salvar e Cancelar
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Salvar", command=self.salvar_consulta).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side=tk.LEFT)
        
    def carregar_pacientes(self):
        # Carregar os nomes dos pacientes do arquivo TXT
        pacientes = []
        with open("data/paciente.txt", "r") as file:
            for line in file:
                if line.startswith("Nome:"):
                    pacientes.append(line.split(":")[1].strip())
        self.paciente_combo["values"] = pacientes
        
    def salvar_consulta(self):
        # Obtendo os dados da consulta
        paciente = self.paciente_combo.get()
        data = self.data_entry.get()
        motivo = self.motivo_entry.get()
        
        # Validando se todos os campos foram preenchidos
        if paciente and data and motivo:
            # Salvando os dados em um arquivo TXT
            with open("data/consulta.txt", "a") as file:
                file.write(f"Paciente: {paciente}\nData: {data}\nMotivo: {motivo}\n\n")
            messagebox.showinfo("Sucesso", "Consulta cadastrada com sucesso!")
            self.destroy()  # Fechando a janela após o cadastro
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")


class VerificarConsultasWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Verificar Consultas")               

        # Criando a tabela para exibir os dados das consultas
        self.table = ttk.Treeview(self)
        self.table["columns"] = ("Paciente", "Data", "Motivo", "")
        self.table.heading("#0", text="ID")
        self.table.heading("Paciente", text="Paciente")
        self.table.heading("Data", text="Data")
        self.table.heading("Motivo", text="Motivo")
        self.table.heading("", text="")
        self.table.pack(expand=True, fill="both")

        # Botão para atualizar os dados
        ttk.Button(self, text="Atualizar", command=self.atualizar_tabela).pack()

        # Carregar dados inicialmente
        self.atualizar_tabela()

        # Configurar evento de duplo clique para excluir registro
        self.table.bind("<Double-1>", self.excluir_registro)

    def atualizar_tabela(self):
        # Limpar a tabela antes de atualizar os dados
        for record in self.table.get_children():
            self.table.delete(record)

        # Carregar dados das consultas do arquivo TXT
        with open("data/consulta.txt", "r") as file:
            id_counter = 1
            for line in file:
                if line.startswith("Paciente:"):
                    paciente = line.split(":")[1].strip()
                    data = next(file).split(":")[1].strip()
                    motivo = next(file).split(":")[1].strip()
                    self.table.insert("", "end", text=id_counter, values=(paciente, data, motivo, "X"))
                    id_counter += 1

    def excluir_registro(self, event):
        # Obter o item selecionado
        item = self.table.selection()

        if item:
            # Obter o ID do registro a ser excluído
            id_to_delete = int(self.table.item(item, "text"))

            # Remover o registro da tabela
            self.table.delete(item)

            # Ler todos os registros do arquivo e reescrevê-los, exceto o registro excluído
            with open("data/consulta.txt", "r") as file:
                lines = file.readlines()

            with open("data/consulta.txt", "w") as file:
                id_counter = 1
                for line in lines:
                    if line.startswith("Paciente:"):
                        if id_counter != id_to_delete:
                            file.write(line)
                            file.write(lines[lines.index(line) + 1])
                            file.write(lines[lines.index(line) + 2])
                            file.write(lines[lines.index(line) + 3])
                        id_counter += 1