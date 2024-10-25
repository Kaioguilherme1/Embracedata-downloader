#!/usr/bin/env python3

#version 0.1.1

import logging
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

import requests

# Configurações do log
logging.basicConfig(
    filename='Inpe_download.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Variável global para o diretório de salvamento
save_directory = 'Dados'  # Diretório padrão
cancel_download = False  # Variável para controle de cancelamento

# Cidades disponíveis
cidades = ['BLJ03', 'BVJ03', 'CAJ2M', 'CGK21', 'FZA0M', 'SAA0K', 'SMK29']

# Função para baixar arquivos
def download_files():
    global save_directory, cancel_download  # Acessa a variável global
    ano_inicio = int(ano_inicio_entry.get())
    ano_fim = int(ano_fim_entry.get())
    dia_inicio = int(dia_inicio_entry.get())
    dia_fim = int(dia_fim_entry.get())

    if dia_inicio > dia_fim or ano_inicio > ano_fim:
        messagebox.showerror('Erro', 'Verifique os limites de datas.')
        return

    os.makedirs(save_directory, exist_ok=True)

    tipos_disponiveis = ['SAO', 'RSF']
    tipos_a_baixar = (
        [tipo_arquivo_combobox.get()]
        if tipo_arquivo_combobox.get() != 'Todos'
        else tipos_disponiveis
    )

    # Obtém as cidades selecionadas
    cidades_selecionadas = [
        cidade for cidade, var in zip(cidades, vars_check) if var.get()
    ]
    if not cidades_selecionadas:
        messagebox.showwarning('Aviso', 'Nenhuma cidade selecionada.')
        return

    total_files = (
        (ano_fim - ano_inicio + 1)
        * (dia_fim - dia_inicio + 1)
        * 3
        * 10
        * 6
        * len(tipos_a_baixar)
        * len(cidades_selecionadas)
    )
    progress_var.set(0)
    progress_bar['maximum'] = total_files

    # Reseta contadores
    global total_downloaded, total_not_found
    total_downloaded = 0
    total_not_found = 0

    # Inicia a thread para o download
    cancel_download = False  # Reseta o cancelamento
    threading.Thread(
        target=perform_download,
        args=(
            ano_inicio,
            ano_fim,
            dia_inicio,
            dia_fim,
            tipos_a_baixar,
            cidades_selecionadas,
        ),
    ).start()


def perform_download(
    ano_inicio,
    ano_fim,
    dia_inicio,
    dia_fim,
    tipos_a_baixar,
    cidades_selecionadas,
):
    global total_downloaded, total_not_found, cancel_download
    for cidade in cidades_selecionadas:
        for ano in range(ano_inicio, ano_fim + 1):
            ano_directory = os.path.join(save_directory, str(ano))
            os.makedirs(
                ano_directory, exist_ok=True
            )  # Cria o diretório do ano se não existir

            for dia in range(dia_inicio, dia_fim + 1):
                dia_str = str(dia).zfill(
                    3
                )  # Garante que o dia tenha 3 dígitos
                dia_directory = os.path.join(ano_directory, dia_str)
                os.makedirs(
                    dia_directory, exist_ok=True
                )  # Cria o diretório do dia se não existir

                for a in range(0, 3):
                    for b in range(0, 10):
                        for c in range(0, 6):
                            if cancel_download:
                                logging.info(
                                    'Download cancelado pelo usuário.'
                                )
                                # mostra no display a msg
                                log_display.insert(
                                    tk.END,
                                    'Download cancelado pelo usuário.\n',
                                )
                                log_display.see('end')
                                messagebox.showinfo(
                                    'Download Concluído',
                                    f'Foram baixados {total_downloaded} arquivos e {total_not_found} não foram encontrados.',
                                )
                                log_display.insert(
                                    tk.END,
                                    f'\nTotal de arquivos baixados: {total_downloaded}\nTotal de arquivos não encontrados: {total_not_found}\n',
                                )
                                return  # Sai da função se o download for cancelado

                            numero = f'{a}{b}{c}'
                            for tipo in tipos_a_baixar:
                                filename = f'{cidade}_{ano}{dia_str}{numero}000.{tipo}'
                                URL = f'https://embracedata.inpe.br/ionosonde/{cidade}/{ano}/{dia_str}/{filename}'

                                try:
                                    logging.info(f'Tentando baixar: {URL}')
                                    log_display.insert(
                                        tk.END, f'Tentando baixar: {URL}\n'
                                    )
                                    log_display.see('end')
                                    response = requests.get(URL)
                                    if response.status_code == 200:
                                        with open(
                                            os.path.join(
                                                dia_directory, filename
                                            ),
                                            'wb',
                                        ) as f:
                                            f.write(response.content)
                                        logging.info(
                                            f'Baixado com sucesso: {URL}'
                                        )
                                        log_display.insert(
                                            tk.END,
                                            f'Baixado com sucesso: {URL}\n',
                                        )
                                        log_display.see('end')
                                        total_downloaded += 1  # Incrementa o contador de downloads
                                    else:
                                        logging.warning(
                                            f'Arquivo não encontrado: {URL} - Status Code: {response.status_code}'
                                        )
                                        log_display.insert(
                                            tk.END,
                                            f'Arquivo não encontrado: {URL} - Status Code: {response.status_code}\n',
                                        )
                                        log_display.see('end')
                                        total_not_found += 1  # Incrementa o contador de não encontrados
                                except Exception as e:
                                    logging.error(f'Erro ao baixar {URL}: {e}')
                                    log_display.insert(
                                        tk.END, f'Erro ao baixar {URL}: {e}\n'
                                    )
                                    log_display.see('end')
                                    total_not_found += 1  # Incrementa o contador de não encontrados

                                progress_var.set(progress_var.get() + 1)
                                root.update_idletasks()  # Atualiza a interface gráfica

    # Exibe o resultado final
    messagebox.showinfo(
        'Download Concluído',
        f'Foram baixados {total_downloaded} arquivos e {total_not_found} não foram encontrados.',
    )
    log_display.insert(
        tk.END,
        f'\nTotal de arquivos baixados: {total_downloaded}\nTotal de arquivos não encontrados: {total_not_found}\n',
    )


def select_directory():
    global save_directory  # Acessa a variável global
    directory = filedialog.askdirectory()
    if directory:
        save_directory = directory
        save_directory_label.config(
            text=save_directory
        )  # Atualiza o label com o diretório selecionado


def cancel_download_action():
    global cancel_download
    cancel_download = True  # Define a variável de cancelamento


# Criando a janela principal
root = tk.Tk()
root.title('INPE Data Downloader')

# Configuração do layout
frame = ttk.Frame(root, padding='10')
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Configurar colunas para serem responsivas
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.columnconfigure(2, weight=1)
frame.columnconfigure(3, weight=1)

# Configurar linhas para serem responsivas
for i in range(11):  # Adicionando linhas para que todos os widgets se expandam
    frame.rowconfigure(i, weight=1)

# Entrada para o ano de início
ttk.Label(frame, text='Ano de Início:').grid(column=0, row=0, sticky=tk.W)
ano_inicio_entry = ttk.Entry(frame, width=5)
ano_inicio_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))

ttk.Label(frame, text='Ano de Fim:').grid(column=2, row=0, sticky=tk.W)
ano_fim_entry = ttk.Entry(frame, width=5)
ano_fim_entry.grid(column=3, row=0, sticky=(tk.W, tk.E))

# Entrada para o dia de início
ttk.Label(frame, text='Dia de Início (1-365):').grid(
    column=0, row=1, sticky=tk.W
)
dia_inicio_entry = ttk.Entry(frame, width=5)
dia_inicio_entry.grid(column=1, row=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text='Dia de Fim (1-365):').grid(column=2, row=1, sticky=tk.W)
dia_fim_entry = ttk.Entry(frame, width=5)
dia_fim_entry.grid(column=3, row=1, sticky=(tk.W, tk.E))

# Combobox para tipos de arquivo
ttk.Label(frame, text='Tipo de Arquivo:').grid(column=0, row=2, sticky=tk.W)
tipo_arquivo_combobox = ttk.Combobox(
    frame, values=['Todos', 'SAO', 'RSF'], state='readonly'
)
tipo_arquivo_combobox.grid(column=1, row=2, columnspan=3, sticky=(tk.W, tk.E))
tipo_arquivo_combobox.current(0)

# Checkbuttons para cidades
vars_check = []
for i, cidade in enumerate(cidades):
    var = tk.BooleanVar(value=False)
    check = ttk.Checkbutton(frame, text=cidade, variable=var)
    check.grid(column=i % 3, row=3 + (i // 3), sticky=tk.W)  # Ajusta a posição
    vars_check.append(var)

# Botão para selecionar diretório
ttk.Button(frame, text='Selecionar Diretório', command=select_directory).grid(
    column=0, row=6, columnspan=2, sticky=(tk.W, tk.E)
)

# Label para mostrar o diretório selecionado
save_directory_label = ttk.Label(frame, text=save_directory)
save_directory_label.grid(column=0, row=7, columnspan=4, sticky=(tk.W, tk.E))

# Botão para iniciar o download
ttk.Button(frame, text='Iniciar Download', command=download_files).grid(
    column=0, row=8, columnspan=2, sticky=(tk.W, tk.E)
)

# Botão para cancelar o download
ttk.Button(
    frame, text='Cancelar Download', command=cancel_download_action
).grid(column=2, row=8, columnspan=2, sticky=(tk.W, tk.E))

# Barra de progresso
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(frame, variable=progress_var, maximum=100)
progress_bar.grid(column=0, row=9, columnspan=4, sticky=(tk.W, tk.E))

# Área de texto para logs
log_display = scrolledtext.ScrolledText(frame, width=60, height=10)
log_display.grid(column=0, row=10, columnspan=4, sticky=(tk.W, tk.E))

# Inicia a aplicação
root.mainloop()
