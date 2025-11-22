import tkinter as tk
from tkinter import messagebox
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pathlib import Path
import os
import re
import subprocess
import threading
import imageio_ffmpeg  # <--- NOVA BIBLIOTECA AQUI

def limpar_nome_arquivo(titulo):
    return re.sub(r'[<>:"/\\|?*]', "_", titulo)

# Função que roda em segundo plano
def tarefa_download(url, botao, label_status):
    try:
        destino = Path.home() / "Downloads"
        destino.mkdir(exist_ok=True)

        # 1. Obter informações
        label_status.config(text="A analisar o vídeo...")
        yt = YouTube(url, on_progress_callback=on_progress)
        
        titulo_limpo = limpar_nome_arquivo(yt.title)
        
        # 2. Baixar Streams (Alta Qualidade)
        label_status.config(text="A baixar vídeo (sem áudio)...")
        video_stream = yt.streams.filter(adaptive=True, type="video", file_extension="mp4").order_by("resolution").desc().first()
        nome_temp_video = f"temp_v_{titulo_limpo}.mp4"
        video_path = video_stream.download(output_path=destino, filename=nome_temp_video)

        label_status.config(text="A baixar áudio...")
        audio_stream = yt.streams.filter(adaptive=True, type="audio", file_extension="mp4").order_by("abr").desc().first()
        nome_temp_audio = f"temp_a_{titulo_limpo}.mp4"
        audio_path = audio_stream.download(output_path=destino, filename=nome_temp_audio)

        # 3. Mesclar usando o FFmpeg embutido (A MÁGICA ACONTECE AQUI)
        label_status.config(text="A processar (Juntando)...")
        saida_path = destino / f"{titulo_limpo}.mp4"

        # Pega o executável direto da biblioteca Python
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

        cmd = [
            ffmpeg_exe, '-y',
            '-i', str(video_path),
            '-i', str(audio_path),
            '-c', 'copy',
            str(saida_path)
        ]
        
        # Executa sem abrir janela preta
        processo = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)

        # 4. Limpeza
        if os.path.exists(video_path): os.remove(video_path)
        if os.path.exists(audio_path): os.remove(audio_path)

        if processo.returncode == 0:
            label_status.config(text="Concluído!", fg="green")
            messagebox.showinfo("Sucesso", f"Vídeo salvo em:\n{saida_path}")
        else:
            label_status.config(text="Erro na fusão", fg="red")
            messagebox.showerror("Erro", f"Falha ao juntar arquivos.\n{processo.stderr.decode()}")

    except Exception as e:
        label_status.config(text="Erro Geral", fg="red")
        messagebox.showerror("Erro Crítico", f"Ocorreu um erro:\n{str(e)}")
    finally:
        botao.config(state=tk.NORMAL, text="Baixar Vídeo")

def iniciar_download():
    url = entry_url.get()
    if not url:
        messagebox.showwarning("Aviso", "Insira a URL.")
        return

    botao_download.config(state=tk.DISABLED, text="A Baixar...")
    t = threading.Thread(target=tarefa_download, args=(url, botao_download, lbl_status))
    t.start()

# --- GUI ---
root = tk.Tk()
root.title("Lancelot TubeDownloader (Portable)")
root.geometry("550x250")

lbl_instrucao = tk.Label(root, text="Insira a URL do YouTube:")
lbl_instrucao.pack(pady=10)

entry_url = tk.Entry(root, width=60)
entry_url.pack(pady=5)

botao_download = tk.Button(root, text="Baixar Vídeo", command=iniciar_download, bg="#007acc", fg="white", font=("Arial", 10, "bold"))
botao_download.pack(pady=20)

lbl_status = tk.Label(root, text="Pronto para baixar", fg="gray")
lbl_status.pack()

root.mainloop()