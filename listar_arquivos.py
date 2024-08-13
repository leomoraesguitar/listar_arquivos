import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import subprocess
import platform

class FileSizeViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Tamanho de Arquivos e Pastas")
        self.geometry("600x400")

        # Botão para selecionar a pasta
        self.select_folder_button = tk.Button(self, text="Selecionar Pasta", command=self.select_folder)
        self.select_folder_button.pack(pady=10)

        # Tabela para exibir os nomes e tamanhos dos arquivos e pastas
        self.tree = ttk.Treeview(self, columns=("Nome", "Tamanho"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Tamanho", text="Tamanho")
        self.tree.column("Nome", anchor="w")
        self.tree.column("Tamanho", anchor="center", width=150)
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Evento de clique duplo
        self.tree.bind("<Double-1>", self.on_double_click)

    def select_folder(self):
        # Abrir o diálogo para selecionar a pasta
        folder_path = filedialog.askdirectory()

        if folder_path:
            # Limpar a tabela existente
            for i in self.tree.get_children():
                self.tree.delete(i)

            # Obter a lista de arquivos e pastas na pasta selecionada
            items_list = []
            for item_name in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item_name)
                if os.path.isfile(item_path):
                    item_size = os.path.getsize(item_path)
                    items_list.append((item_name, item_path, item_size))
                elif os.path.isdir(item_path):
                    folder_size = self.get_folder_size(item_path)
                    items_list.append((item_name + "/", item_path, folder_size))

            # Ordenar a lista de arquivos e pastas pelo tamanho em ordem decrescente
            items_list.sort(key=lambda x: x[2], reverse=True)

            # Inserir os arquivos e pastas ordenados na tabela
            for item_name, item_path, item_size in items_list:
                self.tree.insert("", "end", values=(item_name, self.format_size(item_size)), tags=(item_path,))

    def get_folder_size(self, folder_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)
        return total_size

    def format_size(self, size):
        if size >= 1024 * 1024 * 1024:  # Maior que 1 GB
            return f"{size / (1024 * 1024 * 1024):.2f} GB"
        else:  # Menor que 1 GB, exibe em MB
            return f"{size / (1024 * 1024):.2f} MB"

    def on_double_click(self, event):
        # Obter o item clicado
        selected_item = self.tree.selection()[0]
        item_path = self.tree.item(selected_item, "tags")[0]

        # Abrir o arquivo ou pasta
        self.open_item(item_path)

    def open_item(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", path])
        else:  # Linux
            subprocess.call(["xdg-open", path])

if __name__ == "__main__":
    app = FileSizeViewer()
    app.mainloop()
