# 📺 YouTube Downloader & AI Content Generator

> **Uma ferramenta desktop completa para baixar vídeos em alta qualidade e gerar posts técnicos para LinkedIn usando Inteligência Artificial.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Functional-brightgreen)

## 📖 Sobre o Projeto

Este projeto é uma aplicação desktop (GUI) desenvolvida em Python que resolve dois problemas principais de criadores de conteúdo e estudantes:

1. **Download de Vídeos:** Permite baixar vídeos do YouTube em máxima resolução (1080p, 4K), unindo automaticamente faixas de vídeo e áudio.
2. **Geração de Conteúdo com IA:** Utiliza modelos de ponta (Llama 3.3 e Whisper v3 via Groq) para "ouvir" o vídeo e escrever posts técnicos e virais para o LinkedIn, mesmo que o vídeo original não tenha legendas.

---

## ✨ Funcionalidades

### 📥 Módulo Downloader

- Download de vídeos em alta resolução (Adaptive Streams).
- Fusão automática de Áudio + Vídeo (sem necessidade de instalar FFmpeg manualmente).
- Download apenas de áudio (MP3/MP4).
- Interface amigável com barra de progresso.

### 🤖 Módulo AI Content (Content Repurposing)

- **Transcrição via Áudio:** O sistema baixa o áudio temporariamente e usa o modelo **Whisper Large V3** para transcrever o conteúdo com alta precisão.
- **Geração de Posts:** Transforma a transcrição em um post estruturado para LinkedIn (com ganchos, bullet points e CTA).
- **Sem Dependência de Legendas:** Funciona com qualquer vídeo que tenha fala, independente de ter Closed Captions (CC) no YouTube.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Interface Gráfica:** Tkinter (Nativo)
- **Download engine:** `pytubefix`
- **Processamento de Mídia:** `imageio-ffmpeg`
- **Inteligência Artificial:** `groq` (API gratuita para inferência rápida de Llama e Whisper)

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

1. Ter o **Python** instalado.
2. Obter uma **API Key Gratuita** na [Groq Cloud](https://console.groq.com/keys).

### Passo a Passo

1. **Clone o repositório**

    ```bash
    git clone [https://github.com/PortalDosDados/youtube_download.git](https://github.com/PortalDosDados/youtube_download.git)
    cd youtube_download
    ```

2. **Crie um ambiente virtual (Recomendado)**

    - No Windows:

        ```bash
        python -m venv .venv
        .venv\Scripts\activate
        ```

    - No Linux/Mac:

        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

3. **Instale as dependências**

    ```bash
    pip install -r requirements.txt
    ```

4. **Execute a aplicação**

    ```bash
    python app.py
    ```

---

## 📝 Como Usar

### Aba 1: Baixar Vídeos

1. Cole a URL do vídeo do YouTube.
2. Clique em **"Baixar (HD)"**.
3. O vídeo será salvo automaticamente na sua pasta de **Downloads** do sistema.

### Aba 2: Gerar Post LinkedIn

1. Cole a URL do vídeo que deseja usar como base.
2. Insira sua **API Key da Groq** (ex: `gsk_...`).
3. Clique em **"✨ Gerar Post"**.
4. O sistema irá baixar o áudio, transcrever e gerar o texto na tela para você copiar.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Se você tiver uma ideia de melhoria:

1. Faça um Fork do projeto.
2. Crie uma Branch para sua Feature (`git checkout -b feature/NovaFeature`).
3. Faça o Commit (`git commit -m 'Adicionando nova feature'`).
4. Faça o Push (`git push origin feature/NovaFeature`).
5. Abra um Pull Request.

---

## ⚠️ Aviso Legal

Este software foi desenvolvido para fins educacionais e de produtividade pessoal. O download de conteúdo protegido por direitos autorais sem permissão do autor pode violar os Termos de Serviço do YouTube. Utilize com responsabilidade.

---

**Desenvolvido com 💙 por [PortalDosDados](https://github.com/PortalDosDados).**
