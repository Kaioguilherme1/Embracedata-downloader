from cx_Freeze import setup, Executable
import sys

# Opções de build, especificando 64 bits
build_exe_options = {
    "packages": ["os", "requests"],
    "include_files": [],
    "build_exe": "build/win64",  # Define a pasta de saída
}

# Definindo a base como "Win64GUI" para aplicações com interface gráfica (sem console)
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Setup para Windows 64 bits
setup(
    name="Embracedata-Downloader",
    version="0.1.0",
    description="Ferramenta automatizada para download de dados da plataforma Embracedata do INPE",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "src/Embracedata_Downloader.py",  # Caminho para o arquivo principal
            base=base,
            target_name="Embracedata-Downloader.exe",  # Gera um .exe de 64 bits
        )
    ],
)
