import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from matplotlib.backends.backend_pdf import PdfPages


df = pd.read_csv('vendas_SanPIo.csv', delimiter=';')

# Obter a data atual e formatar para o nome do arquivo
data_atual = datetime.now().strftime("%d.%m.%Y")  # Formata a data no formato DD.MM.AAAA
nome_arquivo = f"Vendas_San_Pio_Ate_{data_atual}.pdf"

# Definir o caminho para a pasta "Downloads" com a data atual no nome do arquivo
caminho_downloads = os.path.join(os.path.expanduser("~"), "Downloads", nome_arquivo)


# Definir o caminho para a pasta "Downloads"
#caminho_downloads = os.path.join(os.path.expanduser("~"), "Downloads", "graficos_gerados.pdf")

# Pré-processamento dos dados 
df['Venda Faturada'] = df['Status Pedido'].apply(lambda x: 'FATURADO' if x == 'FATURADO' else 'NAO FATURADO')
vendas_totais = df.groupby('Venda Faturada')['Valor Total'].sum()
status_vendas = df.groupby('Status Pedido')['Valor Total'].sum()
status_vendas = status_vendas[status_vendas >= 0].dropna()
vendas_por_mes = df.groupby('Data Pedido')['Valor Total'].sum()
df_sorted_clientes = df.groupby('Cliente')['Valor Total'].sum().reset_index().sort_values(by='Valor Total', ascending=False).head(10)
df_sorted_itens = df.groupby('Descrição Item')['Valor Total'].sum().reset_index().sort_values(by='Valor Total', ascending=False).head(10)

# Salvar gráficos no PDF na pasta Downloads
with PdfPages(caminho_downloads) as pdf:
    # Gráfico 1: Venda Total por Status de Faturamento
    plt.figure(figsize=(10, 6))
    ax1 = vendas_totais.plot(kind='bar', color=['skyblue', 'salmon'])
    plt.title('Venda Total por Status de Faturamento')
    plt.xlabel('Status de Faturamento')
    plt.ylabel('Valor Total')
    plt.xticks(rotation=0)
    for p in ax1.patches:
        plt.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')
    pdf.savefig()
    plt.close()

    # Gráfico 2: Distribuição de Vendas por Status de Pedido
    plt.figure(figsize=(10, 6))
    plt.pie(status_vendas, labels=status_vendas.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'], startangle=140, wedgeprops={'edgecolor': 'black'})
    plt.title('Distribuição de Vendas por Status de Pedido')
    pdf.savefig()
    plt.close()

    # Gráfico 3: Vendas por Dia
    plt.figure(figsize=(10, 6))
    ax3 = vendas_por_mes.plot(kind='bar', color='blue')
    plt.title('Vendas por Dia')
    plt.xlabel('Dia')
    plt.ylabel('Total de Vendas')
    plt.xticks(fontsize=8)  
    plt.yticks(fontsize=8)
    plt.tight_layout(pad=2)
    for p in ax3.patches:
        height = p.get_height()
        plt.annotate(f'{height:.2f}', xy=(p.get_x() + p.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
    pdf.savefig()
    plt.close()

    # Gráfico 4: Top 10 Clientes por Valor de Compras
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Valor Total', y='Cliente', data=df_sorted_clientes, hue='Cliente', palette='viridis', dodge=False, legend=False)
    plt.title('Top 10 Clientes por Valor de Compras')
    plt.xlabel('Valor das Vendas')
    plt.ylabel('Cliente')
    plt.xticks(fontsize=8)  
    plt.yticks(fontsize=8)
    plt.tight_layout(pad=2)
    for index, value in enumerate(df_sorted_clientes['Valor Total']):
        plt.text(value, index, f'{value:.2f}', color='black', va="center", ha="left")
    pdf.savefig()
    plt.close()

    # Gráfico 5: Top 10 Itens por Valor de Venda
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Valor Total', y='Descrição Item', data=df_sorted_itens, hue='Descrição Item', palette='viridis', dodge=False, legend=False)
    plt.title('Top 10 Itens por Valor de Venda')
    plt.xlabel('Valor das Vendas')
    plt.ylabel('Itens')
    plt.xticks(fontsize=8)  
    plt.yticks(fontsize=8)
    plt.tight_layout(pad=2) 
    for index, value in enumerate(df_sorted_itens['Valor Total']):
        plt.text(value, index, f'{value:.2f}', color='black', va="center", ha="left")
    pdf.savefig()
    plt.close()

print(f"Gráficos salvos com sucesso em: {caminho_downloads}")
