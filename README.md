# 🛡️ Lancelot Suite: YouTube Downloader & Content AI

> **Ferramenta Desktop para Automação de Conteúdo e Download de Vídeos.**
> Transforma vídeos técnicos em posts virais para LinkedIn usando Inteligência Artificial de ponta.

## 🚀 Visão Geral

O **Lancelot Suite** é uma aplicação desktop desenvolvida em Python que resolve dois grandes problemas de produtividade:
1.  **Download de Alta Qualidade:** Baixa vídeos do YouTube em 1080p/4K (unindo áudio e vídeo automaticamente).
2.  **Repurposing de Conteúdo:** Ouve o áudio de um vídeo (mesmo sem legendas), transcreve usando o modelo **Whisper v3** e cria um post técnico para o LinkedIn usando o **Llama 3.3**, focado no estilo "Portal dos Dados".

---

## 🛠️ Funcionalidades

### Aba 1: Downloader Pro
* ✅ Download de vídeos em máxima resolução (HD/4K).
* ✅ Download de faixas de áudio separadas.
* ✅ Fusão automática usando FFmpeg embutido (Portátil).
* ✅ Barra de status em tempo real.

### Aba 2: AI Content Generator (V5)
* ✅ **Ouvido Absoluto:** Não depende das legendas do YouTube. O app baixa o áudio temporariamente e usa IA para ouvir.
* ✅ **Transcrição Precisa:** Utiliza o modelo `whisper-large-v3` da Groq.
* ✅ **Copywriting Técnico:** Gera posts formatados com bullet points, ganchos e CTA, seguindo o manual de marca do "Portal dos Dados".
* ✅ **Modelo Atualizado:** Utiliza o `llama-3.3-70b-versatile`.

---

## 📋 Pré-requisitos

Para rodar este projeto, você precisa de:

1.  **Python 3.10 ou superior** instalado.
2.  Uma **API Key da Groq** (Gratuita).
    * Obtenha aqui: [https://console.groq.com/keys](https://console.groq.com/keys)

---

## 🔧 Instalação Passo a Passo

### 1. Clone ou Baixe o Repositório
```bash
git clone [https://github.com/seu-usuario/lancelot-suite.git](https://github.com/seu-usuario/lancelot-suite.git)
cd lancelot-suite

Para Baixar Vídeos:
Vá na aba "📥 Baixar".

Cole a URL do YouTube.

Clique em "Baixar (HD)".

O arquivo será salvo na sua pasta Downloads.

Para Gerar Posts (IA):
Vá na aba "🤖 LinkedIn (V5)".

Cole a URL do vídeo que deseja transformar em post.

Cole sua API Key da Groq (começa com gsk_...).

Clique em "✨ Gerar Post".

Aguarde o processo (Download do áudio -> Transcrição -> Escrita).

❓ Solução de Problemas Comuns
Erro: "Model decommissioned"

Você está usando uma versão antiga do código. Certifique-se de que no app.py o modelo está definido como llama-3.3-70b-versatile.

Erro: "FFmpeg not found"

O projeto usa a biblioteca imageio-ffmpeg para não exigir instalação manual. Tente reinstalar as dependências: pip install --force-reinstall imageio-ffmpeg.

Erro: "Connection Error"

Verifique se há espaços em branco antes ou depois da sua API Key.

Desative VPNs ou Firewalls que possam bloquear o Python.