# Video Downloader

Aplicação desktop para download de vídeos do YouTube e TikTok com interface gráfica moderna. Permite escolher formato, resolução e tipo de mídia (vídeo ou áudio), com barra de progresso em tempo real.

## Funcionalidades

- Download de vídeos do YouTube e TikTok
- Modos de download: **Vídeo + Áudio**, **Vídeo sem Áudio** e **Somente Áudio (MP3)**
- Seleção de resolução (lista as resoluções disponíveis do vídeo)
- Seleção de formato de saída: `mp4` ou `webm`
- Barra de progresso e ETA em tempo real
- Seleção de pasta de destino via explorador de arquivos
- Interface escura (dark mode) com tema azul
- Executável `.exe` gerado via PyInstaller (sem necessidade de Python instalado)

## Pré-requisitos

- Python 3.8 ou superior
- pip

## Instalação

1. Clone ou baixe o projeto:

```bash
git clone https://github.com/juliocadelca/Download-Videos.git

cd "Download-Videos"
```

2. Instale as dependências:

```bash
pip install -r requirements.txt

```
Ou você poder usar UV

## Uso

### Executar via Python

```bash
python main.py
```

### Executar via executável

Use o arquivo `dist/VideoDownloader.exe` — não requer Python instalado.

### Como usar a interface

1. Cole a URL do YouTube ou TikTok no campo de texto
2. Clique em **Fetch Info** para carregar título e resoluções disponíveis
3. Selecione o modo de download (Vídeo + Áudio, Vídeo sem Áudio ou Somente Áudio)
4. Escolha o formato (`mp4` / `webm`) e a resolução desejada
5. Selecione a pasta de destino via **Browse**
6. Clique em **Download** e acompanhe o progresso

## Estrutura do Projeto

```
Download Vídeos/
├── main.py              # Interface gráfica (CustomTkinter)
├── downloader.py        # Lógica de download e extração de metadados (yt-dlp)
├── requirements.txt     # Dependências Python
├── app_icon.ico         # Ícone da aplicação
├── create_icon.py       # Script para gerar o ícone
├── build_app.py         # Script para compilar o .exe principal
├── build_installer.py   # Script para compilar o instalador
├── installer_script.py  # Lógica do instalador
├── install_pip.py       # Helper de instalação de dependências
├── test_imports.py      # Teste de importações
└── dist/
    ├── VideoDownloader.exe         # Executável da aplicação
    └── Install_VideoDownloader.exe # Instalador
```

## Dependências

| Pacote | Função |
|--------|--------|
| `customtkinter` | Interface gráfica moderna |
| `yt-dlp` | Download e extração de metadados de vídeos |
| `imageio-ffmpeg` | FFmpeg embutido para conversão de formatos |
| `pillow` | Manipulação de imagens |
| `pyinstaller` | Compilação para executável `.exe` |
| `pywin32` / `winshell` | Integração com o Windows (atalhos, etc.) |

## Compilar o Executável

Para gerar um novo `.exe`:

```bash
python build_app.py
```

O arquivo será gerado em `dist/VideoDownloader.exe`.

## Observações

- O download de áudio converte automaticamente para **MP3 192kbps**
- Ao selecionar "Somente Áudio", as opções de formato e resolução são desabilitadas
- O FFmpeg é obtido automaticamente via `imageio-ffmpeg`, sem instalação manual
- O projeto foi desenvolvido e testado no Windows
