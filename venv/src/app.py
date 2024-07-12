import pandas as pd
import numpy as np
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

class Tela():
    def __init__(self):
        self.root = Tk()
        self.config()
        self.widgets()

        self.extrato_bancario = None
        self.registros_contabeis = None

        self.root.mainloop()
        
    def config(self):
        self.root.title('Automação de Reconciliação Bancária')
        
    def widgets(self):
        self.ler_extrato = Button(text='Abrir Extrato Bancário', command=self.ler_extrato)
        self.ler_extrato.pack(pady=10)

        self.ler_registros = Button(text='Abrir Registros Contábeis', command=self.ler_registros)
        self.ler_registros.pack(pady=10)

        self.reconciliar_btn = Button(text='Reconciliar', command=self.reconciliar)
        self.reconciliar_btn.pack(pady=10)

        self.texto = Text(self.root)
        self.texto.pack(fill='both')
        
    def ler_extrato(self):
        self.arquivo = filedialog.askopenfilename()
        if self.arquivo:
            self.extrato_bancario = pd.read_excel(self.arquivo)
            self.texto.insert(END, "ARQUIVO DE EXTRATO CARREGADO: \n")
            
    def ler_registros(self):
        self.arquivo = filedialog.askopenfilename()
        if self.arquivo:
            self.registros_contabeis = pd.read_excel(self.arquivo)
            self.texto.insert(END, "ARQUIVO DE REGISTROS CARREGADO: \n")
            
    def reconciliar(self):
        if self.registros_contabeis is not None and self.extrato_bancario is not None:
            df_inner = pd.merge(
                self.extrato_bancario,
                self.registros_contabeis,
                on=['Data', 'Descrição', 'Valor'],
                how='inner'
            )

            df_extrato = pd.merge(
                self.extrato_bancario, 
                self.registros_contabeis, 
                on=['Data', 'Descrição', 'Valor'], 
                how='left', indicator=True
            )

            only_in_registros = df_extrato[df_extrato['_merge'] == 'left_only']
            df_somenteExtratos = only_in_registros.drop(columns=['_merge'])

            df_registros = pd.merge(
                self.extrato_bancario, 
                self.registros_contabeis, 
                on=['Data', 'Descrição', 'Valor'], 
                how='right', indicator=True
            )

            only_in_extrato = df_registros[df_registros['_merge'] == 'right_only']
            df_somenteRegistros = only_in_extrato.drop(columns=['_merge'])

            self.aparecer_resultados(df_inner, df_somenteExtratos, df_somenteRegistros)
        else:
            messagebox.showerror("Erro", "Por favor, carregue os arquivos de extrato e registros antes de reconciliar.")

    def aparecer_resultados(self, df_inner, df_somenteExtratos, df_somenteRegistros):
        self.texto.insert(END, '\n')
        self.texto.insert(END, 'RESULTADOS RECONCILIAÇÃO:')
        self.texto.insert(END, '\n')
        self.texto.insert(END, '- Transações encontradas em ambos os conjuntos:\n')
        self.texto.insert(END, str(df_inner) + "\n\n")

        if df_somenteExtratos.empty:
            self.texto.insert(END, "- Não há transações presentes no extrato bancário e ausentes nos registros contábeis\n\n")
        else:
            self.texto.insert(END, "- Transações presentes no extrato bancário e ausentes nos registros contábeis:\n")
            self.texto.insert(END, str(df_somenteExtratos) + "\n\n")

        if df_somenteRegistros.empty:
            self.texto.insert(END, "- Não há transações presentes nos registros contábeis e ausentes no extrato bancário\n\n")
        else:
            self.texto.insert(END, "- Transações presentes nos registros contábeis e ausentes no extrato bancário:\n")
            self.texto.insert(END, str(df_somenteRegistros) + "\n\n")

# Iniciar a aplicação
Tela()