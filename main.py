import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import traceback


def otimizar_rota(arquivo_csv):
    df = pd.read_csv(arquivo_csv)
    colunas_necessarias = {"corredor", "prateleira"}
    colunas_existentes = set(df.columns.str.lower())

    if not colunas_necessarias.issubset(colunas_existentes):
        raise ValueError(
            "O CSV precisa conter as colunas 'corredor' e 'prateleira'."
        )

    # Mapeia os nomes reais das colunas (preservando maiusculas/minusculas originais).
    mapa_colunas = {col.lower(): col for col in df.columns}
    rota_otimizada = df.sort_values(
        by=[mapa_colunas["corredor"], mapa_colunas["prateleira"]]
    )
    return rota_otimizada


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Otimizador de Picking")
        self.root.geometry("900x550")

        self.arquivo_csv = None
        self.df_otimizado = None
        self.colunas = []

        self._build_ui()

    def _build_ui(self):
        frame_top = ttk.Frame(self.root, padding=12)
        frame_top.pack(fill="x")

        self.label_arquivo = ttk.Label(
            frame_top, text="Nenhum arquivo selecionado."
        )
        self.label_arquivo.pack(side="left", padx=(0, 10), fill="x", expand=True)

        btn_abrir = ttk.Button(
            frame_top, text="Selecionar CSV", command=self.selecionar_arquivo
        )
        btn_abrir.pack(side="left")

        btn_salvar = ttk.Button(
            frame_top, text="Salvar rota otimizada", command=self.salvar_csv
        )
        btn_salvar.pack(side="left", padx=(8, 0))

        frame_tabela = ttk.Frame(self.root, padding=(12, 0, 12, 12))
        frame_tabela.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(frame_tabela, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        scroll_y = ttk.Scrollbar(
            frame_tabela, orient="vertical", command=self.tree.yview
        )
        scroll_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll_y.set)

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo de pedidos",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
        )
        if not caminho:
            return

        try:
            self.df_otimizado = otimizar_rota(caminho)
            self.arquivo_csv = caminho
            self.label_arquivo.config(text=f"Arquivo: {caminho}")
            self.renderizar_tabela(self.df_otimizado)
        except Exception as erro:
            messagebox.showerror("Erro ao processar CSV", str(erro))

    def renderizar_tabela(self, df):
        self.tree.delete(*self.tree.get_children())
        self.colunas = list(df.columns)
        self.tree["columns"] = self.colunas

        for coluna in self.colunas:
            self.tree.heading(coluna, text=coluna)
            self.tree.column(coluna, width=120, anchor="center")

        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def salvar_csv(self):
        if self.df_otimizado is None:
            messagebox.showwarning(
                "Sem dados",
                "Selecione e processe um CSV antes de salvar a rota otimizada.",
            )
            return

        caminho_saida = filedialog.asksaveasfilename(
            title="Salvar rota otimizada",
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")],
            initialfile="rota_otimizada.csv",
        )
        if not caminho_saida:
            return

        try:
            self.df_otimizado.to_csv(caminho_saida, index=False)
            messagebox.showinfo("Sucesso", f"Arquivo salvo em:\n{caminho_saida}")
        except Exception as erro:
            messagebox.showerror("Erro ao salvar arquivo", str(erro))


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = App(root)
        root.mainloop()
    except Exception as erro:
        detalhe = traceback.format_exc()
        messagebox.showerror(
            "Erro ao iniciar o aplicativo",
            f"O app encontrou um erro inesperado ao iniciar.\n\n{erro}\n\n{detalhe}",
        )
