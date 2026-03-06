# 🛰️ Embracedata Downloader

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Build Status](https://github.com/kaio-guilherme/Embracedata-downloader/workflows/PyInstaller%20Build%20and%20Release/badge.svg)](https://github.com/kaio-guilherme/Embracedata-downloader/actions)

Embracedata Downloader é uma ferramenta **desktop** que facilita o download automatizado de dados ionosféricos da plataforma [Embracedata do INPE](https://embracedata.inpe.br), permitindo acesso rápido e organizado a informações de clima espacial e geofísicas para pesquisa e análise científica.

![Screenshot](https://img.shields.io/badge/Version-0.2.1-green.svg)

## ✨ Características

- 🖥️ **Interface Gráfica Intuitiva** - Interface desktop amigável desenvolvida com Tkinter
- 📊 **Download em Massa** - Baixe múltiplos arquivos de diferentes períodos simultaneamente
- 🏙️ **Múltiplas Estações** - Suporte para 8 cidades brasileiras de monitoramento ionosférico
- 📁 **Tipos de Dados Variados** - SAO, RSF, DFT, SKY, DVL
- 📝 **Sistema de Logs** - Acompanhamento detalhado de todos os downloads
- ⏸️ **Cancelamento Flexível** - Interrompa downloads a qualquer momento
- 💾 **Organização Automática** - Arquivos salvos de forma estruturada
- 🔄 **Multi-threaded** - Downloads executados em threads separadas sem travar a interface

## 📋 Pré-requisitos

- Python 3.12 ou superior
- Sistema Operacional: Windows, macOS ou Linux

## 🚀 Instalação

### Opção 1: Executável Pré-compilado (Recomendado)

Baixe a versão compilada para seu sistema operacional na [página de releases](https://github.com/kaio-guilherme/Embracedata-downloader/releases):

- **Windows**: `Embracedata_Downloader-windows.exe`
- **macOS**: `Embracedata_Downloader-macos`
- **Linux**: `Embracedata_Downloader-linux`

### Opção 2: Executar do Código Fonte

1. Clone o repositório:
```bash
git clone https://github.com/kaio-guilherme/Embracedata-downloader.git
cd Embracedata-downloader
```

2. Instale as dependências usando Poetry:
```bash
poetry install
```

Ou usando pip:
```bash
pip install requests
```

3. Execute o aplicativo:
```bash
python Embracedata_Downloader.py
```

## 📖 Como Usar

1. **Configure o Período**
   - Defina o ano inicial e final (ex: 2020 a 2024)
   - Defina o dia juliano inicial e final (1 a 366)

2. **Selecione os Tipos de Arquivo**
   - ☑️ SAO - Ionogramas em formato SAO
   - ☑️ RSF - Arquivos RSF
   - ☑️ DFT - Arquivos DFT 
   - ☑️ SKY - Arquivos SKY
   - ☑️ DVL - Arquivos DVL 

3. **Escolha as Cidades**
   - BLJ03 - Belém
   - BVJ03 - Boa Vista
   - CAJ2M - Cachoeira Paulista
   - CGK21 - Campo Grande
   - FZA0M - Fortaleza
   - SAA0K - São José dos Campos
   - SAJ03 - Santarém
   - SMK29 - Santa Maria

4. **Selecione o Diretório de Destino**
   - Clique em "Selecionar Diretório"
   - Escolha onde salvar os arquivos (padrão: `./Dados`)

5. **Inicie o Download**
   - Clique em "Iniciar Download"
   - Acompanhe o progresso na área de logs
   - Use "Cancelar Download" se necessário

## 📊 Tipos de Dados Disponíveis

| Tipo | Descrição | Formatos |
|------|-----------|----------|
| SAO | Ionogramas em formato SAO | 000 |
| RSF | Arquivos de resumo RSF | 000 |
| DFT | Drift Data Files | 430, 700 |
| SKY | Sky Map Files | 430, 700 |
| DVL | Doppler Velocity Log | 430, 700 |

## 🏗️ Estrutura do Projeto

```
Embracedata-downloader/
├── Embracedata_Downloader.py  # Aplicação principal
├── pyproject.toml             # Configuração do Poetry
├── poetry.lock                # Lock file de dependências
├── LICENSE                    # Licença MIT
├── README.md                  # Este arquivo
├── Inpe_download.log          # Arquivo de log (gerado)
├── icons/                     # Ícones da aplicação
│   ├── icon.icns             # Ícone macOS
│   ├── icon.ico              # Ícone Windows
│   └── icon.png              # Ícone genérico
└── .github/
    └── workflows/
        └── build.yaml         # CI/CD GitHub Actions
```

## 🛠️ Desenvolvimento

### Configurar Ambiente de Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
poetry install --with dev,build

# Executar testes
poetry run task test

# Verificar formatação de código
poetry run task lint

# Criar commit seguindo convenções
poetry run task commit
```

### Compilar Executável

```bash
# Instalar PyInstaller
pip install pyinstaller

# Compilar (Windows)
pyinstaller --onefile --noconsole --icon=./icons/icon.ico Embracedata_Downloader.py

# Compilar (macOS)
pyinstaller --onefile --noconsole --icon=./icons/icon.icns Embracedata_Downloader.py

# Compilar (Linux)
pyinstaller --onefile --noconsole Embracedata_Downloader.py
```

## 🔍 Logs

Todos os downloads são registrados no arquivo `Inpe_download.log` com:
- Timestamp de cada operação
- URLs acessadas
- Status de sucesso/falha
- Erros encontrados

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças usando Commitizen (`poetry run task commit`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Convenções de Commit

Este projeto usa [Commitizen](https://commitizen-tools.github.io/commitizen/) com [Conventional Gitmoji](https://github.com/ljnsn/cz-conventional-gitmoji):

```bash
poetry run cz commit
```

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👤 Autor

**Kaio Guilherme**
- Email: kaioguilherme444@gmail.com
- GitHub: [@kaio-guilherme](https://github.com/Kaioguilherme1)

## 🙏 Agradecimentos

- [INPE](https://www.inpe.br/) - Instituto Nacional de Pesquisas Espaciais
- [Embracedata](https://embracedata.inpe.br) - Plataforma de dados ionosféricos
- Comunidade Python

## 📚 Recursos Adicionais

- [Documentação INPE Embracedata](https://embracedata.inpe.br)
- [Sobre Ionosondas](https://www.inpe.br/climaespacial/)
- [Python Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

---

**Nota**: Este projeto não é oficialmente afiliado ao INPE. É uma ferramenta desenvolvida de forma independente para facilitar o acesso aos dados públicos da plataforma Embracedata.
