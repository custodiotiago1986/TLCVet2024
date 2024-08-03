import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class CadastrarAnimalWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Inserir Paciente")
        self.geometry("600x250")
        
        # Label e Entry para o nome do paciente
        tk.Label(self, text="Nome do Paciente:").pack()
        self.nome_entry = tk.Entry(self)
        self.nome_entry.pack()
        
        # Radiobuttons para selecionar o tipo do paciente
        self.tipo_var = tk.StringVar()
        tk.Label(self, text="Tipo do Paciente:").pack()
        tk.Radiobutton(self, text="Cachorro", variable=self.tipo_var, value="cachorro").pack()
        tk.Radiobutton(self, text="Gato", variable=self.tipo_var, value="gato").pack()
        
        # Label e Entry para a data de nascimento do paciente
        tk.Label(self, text="Data de Nascimento:").pack()
        self.nascimento_entry = tk.Entry(self)
        self.nascimento_entry.pack()
        
        # Label e Entry para as observações do paciente
        tk.Label(self, text="Observações:").pack()
        self.observacoes_entry = tk.Entry(self)
        self.observacoes_entry.pack()
        
        # Botões Salvar e Cancelar
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Salvar", command=self.salvar_paciente).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side=tk.LEFT)
        
    def salvar_paciente(self):
        # Obtendo os dados do paciente
        nome = self.nome_entry.get()
        tipo = self.tipo_var.get()
        nascimento = self.nascimento_entry.get()
        observacoes = self.observacoes_entry.get()
        
        # Validando se todos os campos foram preenchidos
        if nome and tipo and nascimento:
            # Salvando os dados em um arquivo TXT
            with open("data/paciente.txt", "a") as file:
                file.write(f"Nome: {nome}\nTipo: {tipo}\nData de Nascimento: {nascimento}\nObservações: {observacoes}\n\n")
            messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
            self.destroy()  # Fechando a janela após o cadastro
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

class AnimaisCadastradosWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Animais Cadastrados")
        # self.state("zoomed")  # Maximizando a janela por padrão

        # Criando a tabela para exibir os dados dos pacientes
        self.table = ttk.Treeview(self)
        self.table["columns"] = ("Nome", "Tipo", "Data de Nascimento", "Observações", "")
        self.table.heading("#0", text="ID")
        self.table.heading("Nome", text="Nome")
        self.table.heading("Tipo", text="Tipo")
        self.table.heading("Data de Nascimento", text="Data de Nascimento")
        self.table.heading("Observações", text="Observações")
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

        # Carregar dados dos pacientes do arquivo TXT
        with open("data/paciente.txt", "r") as file:
            id_counter = 1
            for line in file:
                if line.startswith("Nome:"):
                    nome = line.split(":")[1].strip()
                    tipo = next(file).split(":")[1].strip()
                    nascimento = next(file).split(":")[1].strip()
                    observacoes = next(file).split(":")[1].strip()
                    self.table.insert("", "end", text=id_counter, values=(nome, tipo, nascimento, observacoes, "X"))
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
            with open("data/paciente.txt", "r") as file:
                lines = file.readlines()

            with open("data/paciente.txt", "w") as file:
                id_counter = 1
                for line in lines:
                    if line.startswith("Nome:"):
                        if id_counter != id_to_delete:
                            file.write(line)
                            file.write(lines[lines.index(line) + 1])
                            file.write(lines[lines.index(line) + 2])
                            file.write(lines[lines.index(line) + 3])
                        id_counter += 1
