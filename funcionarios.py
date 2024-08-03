import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class CadastrarFuncionarioWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastrar Funcionário")
        self.geometry("600x250")

        # Label e Entry para o nome do funcionário
        tk.Label(self, text="Nome do Funcionário:").pack()
        self.nome_entry = tk.Entry(self)
        self.nome_entry.pack()

        # Radiobuttons para selecionar o cargo do funcionário
        self.cargo_var = tk.StringVar()
        tk.Label(self, text="Cargo do Funcionário:").pack()
        tk.Radiobutton(self, text="Veterinário", variable=self.cargo_var, value="Veterinário").pack()
        tk.Radiobutton(self, text="Recepcionista", variable=self.cargo_var, value="Recepcionista").pack()

        # Label e Entry para a data de contratação do funcionário
        tk.Label(self, text="Data de Contratação:").pack()
        self.contratacao_entry = tk.Entry(self)
        self.contratacao_entry.pack()

        # Label e Entry para as observações do funcionário
        tk.Label(self, text="Observações:").pack()
        self.observacoes_entry = tk.Entry(self)
        self.observacoes_entry.pack()

        # Botões Salvar e Cancelar
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Salvar", command=self.salvar_funcionario).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side=tk.LEFT)

    def salvar_funcionario(self):
        # Obtendo os dados do funcionário
        nome = self.nome_entry.get()
        cargo = self.cargo_var.get()
        contratacao = self.contratacao_entry.get()
        observacoes = self.observacoes_entry.get()

        # Validando se todos os campos foram preenchidos
        if nome and cargo and contratacao:
            # Salvando os dados em um arquivo TXT
            with open("data/funcionario.txt", "a") as file:
                file.write(f"Nome: {nome}\nCargo: {cargo}\nData de Contratação: {contratacao}\nObservações: {observacoes}\n\n")
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
            self.destroy()  # Fechando a janela após o cadastro
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

class FuncionariosCadastradosWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Funcionários Cadastrados")

        # Criando a tabela para exibir os dados dos funcionários
        self.table = ttk.Treeview(self)
        self.table["columns"] = ("Nome", "Cargo", "Data de Contratação", "Observações", "")
        self.table.heading("#0", text="ID")
        self.table.heading("Nome", text="Nome")
        self.table.heading("Cargo", text="Cargo")
        self.table.heading("Data de Contratação", text="Data de Contratação")
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

        # Carregar dados dos funcionários do arquivo TXT
        with open("data/funcionario.txt", "r") as file:
            id_counter = 1
            for line in file:
                if line.startswith("Nome:"):
                    nome = line.split(":")[1].strip()
                    cargo = next(file).split(":")[1].strip()
                    contratacao = next(file).split(":")[1].strip()
                    observacoes = next(file).split(":")[1].strip()
                    self.table.insert("", "end", text=id_counter, values=(nome, cargo, contratacao, observacoes, "X"))
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
            with open("data/funcionario.txt", "r") as file:
                lines = file.readlines()

            with open("data/funcionario.txt", "w") as file:
                id_counter = 1
                for line in lines:
                    if line.startswith("Nome:"):
                        if id_counter != id_to_delete:
                            file.write(line)
                            file.write(lines[lines.index(line) + 1])
                            file.write(lines[lines.index(line) + 2])
                            file.write(lines[lines.index(line) + 3])
                        id_counter += 1
