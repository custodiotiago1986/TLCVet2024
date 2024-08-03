import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random

from animais import CadastrarAnimalWindow, AnimaisCadastradosWindow
from consultas import AbrirConsultaWindow, VerificarConsultasWindow
from funcionarios import CadastrarFuncionarioWindow, FuncionariosCadastradosWindow

class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Splash Screen")
        self.geometry("400x200")
        self.attributes('-topmost', True)  # Mantém a splash screen no topo
        self.overrideredirect(True)  # Remove a barra de título e os botões de controle da janela
        self.create_widgets()

    def create_widgets(self):
        image_path = "img/splash_screen.png"  # Caminho da imagem da splash screen
        label = ttk.Label(self, text="TLC VET 2024", font=("Helvetica", 20))
        label.pack(side=tk.RIGHT, padx=10, pady=10)
        img = self.resize_image(image_path, 150, 150)
        image_label = ttk.Label(self, image=img)
        image_label.image = img
        image_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.after(3000, self.destroy)  # Fecha a splash screen após 3 segundos

        # Centraliza a splash screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def resize_image(self, image_path, width, height):
        try:
            original_image = Image.open(image_path)
            resized_image = original_image.resize((width, height), Image.LANCZOS)
            return ImageTk.PhotoImage(resized_image)
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {image_path}")
            return None


class DiagBox(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Dica do dia")
        self.geometry("400x260")
        # self.overrideredirect(True)  # Removido para adicionar a barra de título
        self.create_widgets()

    def create_widgets(self):
        image_path = "img/diagbox_image.png"  # Caminho da imagem da caixa de diálogo
        img = self.resize_image(image_path, 100, 100)
        image_label = ttk.Label(self, image=img)
        image_label.image = img
        image_label.grid(row=0, column=0, padx=10, pady=10)

        # Frases
        frases = [
            # 10 frases sobre gatos
            "Os gatos têm 32 músculos em cada orelha.",
            "Um grupo de gatos é chamado de clowder.",
            "Os gatos passam cerca de 70% de suas vidas dormindo.",
            "Os gatos têm cinco dedos nas patas dianteiras e quatro nas traseiras.",
            "Os gatos podem fazer mais de 100 sons diferentes.",
            "Os gatos têm uma terceira pálpebra chamada membrana nictitante.",
            "Os gatos não conseguem sentir o sabor doce.",
            "O cérebro dos gatos é 90% semelhante ao cérebro humano.",
            "Os gatos podem girar suas orelhas 180 graus.",
            "Os gatos têm glândulas de cheiro nas patas.",
            # 10 frases sobre cães
            "Os cães têm um olfato entre 10.000 e 100.000 vezes mais apurado que o dos humanos.",
            "O cão mais rápido do mundo é o Greyhound.",
            "Os cães têm glândulas sudoríparas apenas nas patas.",
            "Os cães podem ser treinados para detectar doenças como câncer e diabetes.",
            "Os cães têm três pálpebras, incluindo uma pálpebra extra para proteção.",
            "O nariz de cada cão é único, assim como as impressões digitais humanas.",
            "Os cães sonham como os humanos.",
            "Os cães podem ouvir sons quatro vezes mais distantes que os humanos.",
            "Os cães têm cerca de 1.700 papilas gustativas.",
            "Os cães podem aprender mais de 1000 palavras.",
            # 10 dicas de uso do aplicativo
            "Clique em 'Cadastrar Animal' para adicionar um novo paciente.",
            "Use 'Cadastrar Funcionário' para adicionar novos membros à equipe.",
            "Clique em 'Abrir Consulta' para iniciar uma nova consulta.",
            "Em 'Animais Cadastrados', você pode ver todos os animais registrados.",
            "Verifique 'Funcionários Cadastrados' para listar todos os funcionários.",
            "Use 'Verificar Consultas' para acompanhar as consultas agendadas.",
            "Mantenha as informações dos animais sempre atualizadas.",
            "Utilize a busca para encontrar registros rapidamente.",
            "Faça backup dos dados regularmente.",
            "Mantenha o software atualizado para obter novas funcionalidades."
        ]

        frase_escolhida = random.choice(frases)
        label = ttk.Label(self, text=frase_escolhida, wraplength=250, justify="center")
        label.grid(row=0, column=1, padx=10, pady=10)

        ok_button = ttk.Button(self, text="OK", command=self.destroy)
        ok_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Centraliza a diag box
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def resize_image(self, image_path, width, height):
        try:
            original_image = Image.open(image_path)
            resized_image = original_image.resize((width, height), Image.LANCZOS)
            return ImageTk.PhotoImage(resized_image)
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {image_path}")
            return None


class GerenciadorClinicaVeterinaria(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TLC VET 2024")
        self.iconbitmap('img/main.ico')  # Ícone da janela
        self.create_widgets()
        self.center_window()  # Centraliza a janela principal

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        self.geometry("600x480")  # Tamanho inicial da janela
        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill="both")

        # Criando os botões
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(expand=True, pady=50)

        # Lista de opções e imagens
        options = [
            ("Cadastrar Animal", "img/animal.png", CadastrarAnimalWindow),
            ("Cadastrar Funcionário", "img/funcionario.png", CadastrarFuncionarioWindow),
            ("Abrir Consulta", "img/consulta.png", AbrirConsultaWindow),
            ("Animais Cadastrados", "img/animais_cadastrados.png", AnimaisCadastradosWindow),
            ("Funcionários Cadastrados", "img/funcionarios_cadastrados.png", FuncionariosCadastradosWindow),
            ("Verificar Consultas", "img/verificar_consultas.png", VerificarConsultasWindow)
        ]

        for i, (text, image_path, command) in enumerate(options):
            # Redimensionar a imagem para 100x100 (pode ajustar conforme necessário)
            img = self.resize_image(image_path, 100, 100)
            button = ttk.Button(buttons_frame, text=text, image=img, compound="top", command=lambda c=command: self.open_window(c))
            button.image = img  # Manter referência à imagem
            button.grid(row=i//3, column=i%3, padx=20, pady=20)

    def open_window(self, command):
        window = command(self)

    def resize_image(self, image_path, width, height):
        try:
            original_image = Image.open(image_path)
            resized_image = original_image.resize((width, height), Image.LANCZOS)
            return ImageTk.PhotoImage(resized_image)
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {image_path}")
            return None


if __name__ == "__main__":
    app = GerenciadorClinicaVeterinaria()
    app.withdraw()  # Oculta a janela principal
    splash = SplashScreen(app)
    app.after(3000, lambda: [app.deiconify(), splash.destroy(), DiagBox(app)])  # Abre a janela principal e a diagbox após 3 segundos
    app.mainloop()
