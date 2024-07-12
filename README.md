# Automação de Reconciliação Bancária

## Descrição do Projeto
Este projeto implementa uma automação para reconciliação bancária utilizando Python com Tkinter para a interface gráfica e Pandas para manipulação de dados.

## Que Problema Resolve
Facilita o processo de reconciliação entre extratos bancários e registros contábeis, identificando transações em comum e discrepâncias entre os conjuntos de dados.

## Funcionalidades
- Carregar arquivos de extrato bancário e registros contábeis.
- Realizar a reconciliação automática para identificar:
  - Transações presentes em ambos os conjuntos.
  - Transações presentes apenas no extrato bancário.
  - Transações presentes apenas nos registros contábeis.
- Exibir resultados detalhados na interface gráfica.

## Stacks Utilizadas
- Python
- Pandas
- Tkinter

## Instalação

### Como Clonar o Repositório
```bash
git clone https://github.com/seu_usuario/nome_do_repositorio.git
```

### Como Criar e Ativar o Ambiente Virtual

```bash
cd nome_do_repositorio
python -m venv venv
```
#### No Windows
```bash
venv\Scripts\activate
```
#### No macOS/Linux
```bash
source venv/bin/activate
```
### Para Instalar as Dependências do Requirements.txt
```bash
pip install -r requirements.txt
```

## Como Usar a Interface Gráfica

1. Clique no botão "Abrir Extrato Bancário" para carregar o arquivo de extrato bancário.
2. Clique no botão "Abrir Registros Contábeis" para carregar o arquivo de registros contábeis.
3. Clique no botão "Reconciliar" para iniciar o processo de reconciliação.
4. Os resultados serão exibidos na interface gráfica, indicando:
   - As transações encontradas em ambos os conjuntos.
   - As transações presentes apenas no extrato bancário e ausentes nos registros contábeis.
   - As transações presentes apenas nos registros contábeis e ausentes no extrato bancário.
