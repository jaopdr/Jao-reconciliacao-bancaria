import pandas as pd
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

class Tela():
    # Inicialização da janela principal
    def __init__(self):
        self.root = Tk()  # Cria uma nova janela Tkinter
        self.config()  # Configurações da janela
        self.widgets()  # Adiciona os widgets (botões e texto) na janela

        # Variáveis para armazenar os dados dos arquivos
        self.extrato_bancario = None
        self.registros_contabeis = None

        self.root.mainloop()  # Loop principal para exibir a janela

    # Configurações da janela principal
    def config(self):
        self.root.title('Automação de Reconciliação Bancária')  # Define o título da janela

    # Adiciona os widgets (botões e texto) na janela
    def widgets(self):
        # Botão para carregar o arquivo de extrato bancário
        self.ler_extrato = Button(text='Abrir Extrato Bancário', command=self.ler_extrato)
        self.ler_extrato.pack(pady=10)

        # Botão para carregar o arquivo de registros contábeis
        self.ler_registros = Button(text='Abrir Registros Contábeis', command=self.ler_registros)
        self.ler_registros.pack(pady=10)

        # Botão para iniciar o processo de reconciliação
        self.reconciliar_btn = Button(text='Reconciliar', command=self.reconciliar)
        self.reconciliar_btn.pack(pady=10)

        # Área de texto para exibir os resultados da reconciliação
        self.texto = Text(self.root)
        self.texto.pack(fill='both')

    # Função para carregar o arquivo de extrato bancário
    def ler_extrato(self):
        self.arquivo = filedialog.askopenfilename()  # Abre a janela de seleção de arquivo
        if self.arquivo:
            self.extrato_bancario = pd.read_excel(self.arquivo)  # Lê o arquivo Excel selecionado
            self.texto.insert(END, "ARQUIVO DE EXTRATO CARREGADO: \n")  # Exibe mensagem na área de texto

    # Função para carregar o arquivo de registros contábeis
    def ler_registros(self):
        self.arquivo = filedialog.askopenfilename()  # Abre a janela de seleção de arquivo
        if self.arquivo:
            self.registros_contabeis = pd.read_excel(self.arquivo)  # Lê o arquivo Excel selecionado
            self.texto.insert(END, "ARQUIVO DE REGISTROS CARREGADO: \n")  # Exibe mensagem na área de texto

    # Função para reconciliar os dados dos arquivos carregados
    def reconciliar(self):
        # Verifica se ambos os arquivos foram carregados
        if self.registros_contabeis is not None and self.extrato_bancario is not None:
            # Realiza a reconciliação utilizando merge inner, left e right
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
            # Exibe mensagem de erro caso algum dos arquivos não tenha sido carregado
            messagebox.showerror("Erro", "Por favor, carregue os arquivos de extrato e registros antes de reconciliar.")

    # Função para exibir os resultados da reconciliação na área de texto
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

# Inicia a aplicação
Tela()