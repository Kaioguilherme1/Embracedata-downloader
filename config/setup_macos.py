from cx_Freeze import setup, Executable

# Opções de build
build_exe_options = {
    "packages": ["os", "requests"],
    "include_files": [],
    "build_exe": "build/macos",  # Define a pasta de saída
}

# Setup para gerar o binário no macOS
setup(
    name="Embracedata-Downloader",
    version="0.1.0",
    description="Ferramenta automatizada para download de dados da plataforma Embracedata do INPE",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "src/Embracedata_Downloader.py",  # Caminho para o arquivo principal
            target_name="Embracedata-Downloader",  # Nome do binário
        )
    ],
)
