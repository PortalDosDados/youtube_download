import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pathlib import Path
import os
import re
import subprocess
import threading
import imageio_ffmpeg
from groq import Groq

# ==========================================
# 1. FUNÇÕES AUXILIARES
# ==========================================


def limpar_nome_arquivo(titulo):
    return re.sub(r'[<>:"/\\|?*]', "_", titulo)

# ==========================================
# 2. LÓGICA: DOWNLOADER (ABA 1)
# ==========================================


def tarefa_download(url, botao, label_status):
    try:
        destino = Path.home() / "Downloads"
        destino.mkdir(exist_ok=True)

        label_status.config(text="🔍 Analisando...", fg="blue")
        yt = YouTube(url, on_progress_callback=on_progress)
        titulo_limpo = limpar_nome_arquivo(yt.title)

        label_status.config(text="📥 Baixando Vídeo...", fg="orange")
        video_stream = yt.streams.filter(
            adaptive=True, type="video", file_extension="mp4").order_by("resolution").desc().first()
        nome_v = f"temp_v_{titulo_limpo}.mp4"
        video_path = video_stream.download(
            output_path=destino, filename=nome_v)

        label_status.config(text="📥 Baixando Áudio...", fg="orange")
        audio_stream = yt.streams.filter(
            adaptive=True, type="audio", file_extension="mp4").order_by("abr").desc().first()
        nome_a = f"temp_a_{titulo_limpo}.mp4"
        audio_path = audio_stream.download(
            output_path=destino, filename=nome_a)

        label_status.config(text="⚙️ Unindo...", fg="blue")
        saida_path = destino / f"{titulo_limpo}.mp4"

        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [ffmpeg_exe, '-y', '-i',
               str(video_path), '-i', str(audio_path), '-c', 'copy', str(saida_path)]

        creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        subprocess.run(cmd, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, creationflags=creation_flags)

        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)

        label_status.config(text="✅ Sucesso!", fg="green")
        messagebox.showinfo("Sucesso", f"Salvo em:\n{saida_path}")

    except Exception as e:
        label_status.config(text="❌ Erro", fg="red")
        messagebox.showerror("Erro", str(e))
    finally:
        botao.config(state=tk.NORMAL, text="Baixar Vídeo (HD)")


def iniciar_download():
    url = entry_url_down.get()
    if not url:
        return
    btn_down.config(state=tk.DISABLED, text="Aguarde...")
    threading.Thread(target=tarefa_download, args=(
        url, btn_down, lbl_status_down)).start()

# ==========================================
# 3. LÓGICA: IA WHISPER + LLAMA (A GRANDE MUDANÇA)
# ==========================================


def tarefa_gerar_post_via_audio(url, api_key, text_area, botao, label_status):
    arquivo_audio_temp = "temp_audio_to_transcribe.mp4"  # Usaremos MP4 audio stream

    try:
        client = Groq(api_key=api_key)

        # 1. Baixar APENAS o áudio do vídeo (leve e rápido)
        label_status.config(text="📥 Baixando áudio do vídeo...", fg="blue")
        yt = YouTube(url)

        # Pega o stream de áudio mais leve possível para subir rápido
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            raise Exception("Não foi possível encontrar stream de áudio.")

        audio_stream.download(filename=arquivo_audio_temp)

        # 2. Enviar para Groq Whisper (Ouvir o áudio)
        label_status.config(
            text="👂 A IA está ouvindo (Transcrevendo)...", fg="purple")

        with open(arquivo_audio_temp, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(arquivo_audio_temp, file.read()),
                model="whisper-large-v3",  # Modelo Multilíngue Poderoso
                response_format="json",
                # Força português (opcional, pode remover para auto-detect)
                language="pt",
                temperature=0.0
            )

        texto_transcrito = transcription.text

        # Remove o arquivo temporário
        if os.path.exists(arquivo_audio_temp):
            os.remove(arquivo_audio_temp)

        # 3. Gerar o Post com Llama 3
        label_status.config(text="✍️ Escrevendo o post...", fg="purple")

        prompt_sistema = """
        Você é um Copywriter especializado em conteúdo técnico para LinkedIn, com foco em dados, IA prática, produtividade e manutenção industrial.

        Transforme a transcrição do vídeo em um post para o projeto Portal dos Dados, seguindo estas diretrizes:

        1. Estilo:
        - Tom profissional, direto, claro e com frases curtas.
        - Linguagem acessível para técnicos de PCM, engenheiros de manutenção e analistas de dados.
        - Evite floreios; priorize objetividade e autoridade técnica.

        2. Estrutura:
        - Headline forte e curta, criando ganho imediato de atenção.
        - Corpo dividido em blocos de leitura rápida.
        - Sempre utilize espaçamento entre os parágrafos.
        - Inclua bullet points quando houver conceitos, passos ou recomendações.
        - Destaque ideias-chave que aumentem produtividade e eliminem desperdício operacional.

        3. Enfoque estratégico:
        - Relacione o conteúdo ao uso de dados, automação, inteligência artificial e boas práticas de manutenção.
        - Conecte o aprendizado do vídeo com decisões de alto impacto na rotina de gestão da manutenção.
        - Valorize o pensamento analítico e a eliminação de gargalos.
        - Sempre entregue um insight acionável.

        4. Finalização:
        - Inclua uma CTA chamando o leitor para comentar ou compartilhar uma experiência.
        - Finalize sempre com a frase exata: “Quando não se agrega valor, se agrega custo.”
        - Inclua as hashtags padrão:
          #PortalDosDados #Dados #AnáliseDeDados #Analytics #DataScience
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user",
                    "content": f"Transcrição:\n{texto_transcrito[:15000]}..."}
            ],
            model="llama-3.3-70b-versatile",
        )

        resultado = chat_completion.choices[0].message.content

        # 4. Resultado
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, resultado)
        label_status.config(text="✅ Post Gerado com Sucesso!", fg="green")

    except Exception as e:
        label_status.config(text="❌ Erro", fg="red")
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, f"ERRO:\n{str(e)}")
        # Tenta limpar lixo se der erro
        if os.path.exists(arquivo_audio_temp):
            os.remove(arquivo_audio_temp)
    finally:
        botao.config(state=tk.NORMAL, text="✨ Gerar Post LinkedIn")


def iniciar_geracao():
    url = entry_url_ai.get()
    api_key = entry_api.get()

    if not url or not api_key:
        messagebox.showwarning("Aviso", "Preencha URL e API Key.")
        return

    btn_ai.config(state=tk.DISABLED, text="⏳ Processando...")
    threading.Thread(target=tarefa_gerar_post_via_audio, args=(
        url, api_key, txt_result, btn_ai, lbl_status_ai)).start()

# ==========================================
# 4. INTERFACE
# ==========================================


root = tk.Tk()
root.title("Lancelot Suite V4 - AI Audio Engine")
root.geometry("650x600")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# ABA 1
frame_down = tk.Frame(notebook, bg="#f5f5f5")
notebook.add(frame_down, text="  📥 Baixar  ")
tk.Label(frame_down, text="Link do Vídeo:", bg="#f5f5f5").pack(pady=(20, 5))
entry_url_down = tk.Entry(frame_down, width=65)
entry_url_down.pack(pady=5)
btn_down = tk.Button(frame_down, text="Baixar (HD)", command=iniciar_download,
                     bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
btn_down.pack(pady=15)
lbl_status_down = tk.Label(frame_down, text="Pronto", bg="#f5f5f5", fg="gray")
lbl_status_down.pack()

# ABA 2
frame_ai = tk.Frame(notebook, bg="#f5f5f5")
notebook.add(frame_ai, text="  🤖 LinkedIn (Whisper)  ")
tk.Label(frame_ai, text="Este modo OUVE o vídeo (Funciona sem legenda!)",
         bg="#f5f5f5", fg="#d35400", font=("Arial", 8, "bold")).pack(pady=(10, 0))

tk.Label(frame_ai, text="1. Link do Vídeo:", bg="#f5f5f5",
         font=("Arial", 9, "bold")).pack(pady=(10, 0))
entry_url_ai = tk.Entry(frame_ai, width=65)
entry_url_ai.pack(pady=5)

tk.Label(frame_ai, text="2. API Key Groq:", bg="#f5f5f5",
         font=("Arial", 9, "bold")).pack(pady=(10, 0))
entry_api = tk.Entry(frame_ai, width=65, show="*")
entry_api.pack(pady=5)

btn_ai = tk.Button(frame_ai, text="✨ Gerar Post (Via Áudio)",
                   command=iniciar_geracao, bg="#d35400", fg="white", font=("Arial", 10, "bold"))
btn_ai.pack(pady=15)

lbl_status_ai = tk.Label(
    frame_ai, text="Aguardando...", bg="#f5f5f5", fg="gray")
lbl_status_ai.pack()

txt_result = scrolledtext.ScrolledText(frame_ai, width=75, height=15)
txt_result.pack(pady=10)

root.mainloop()
