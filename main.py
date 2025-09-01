import tkinter as tk
from tkinter import messagebox
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pathlib import Path
import os
import re

# Função que faz o download do vídeo
def baixar_video():
    url = entry_url.get()
    if not url:
        messagebox.showwarning("Aviso", "Por favor, insira a URL do YouTube.")
        return
    
    try:
        # Pasta Downloads
        destino = Path.home() / "Downloads"
        destino.mkdir(exist_ok=True)

        # Cria objeto YouTube
        yt = YouTube(url, on_progress_callback=on_progress)
        
        # Streams de vídeo e áudio
        video_stream = yt.streams.filter(adaptive=True, type="video", file_extension="mp4").order_by("resolution").desc().first()
        audio_stream = yt.streams.filter(adaptive=True, type="audio", file_extension="mp4").order_by("abr").desc().first()

        # Download temporário
        video_path = video_stream.download(output_path=destino, filename="temp_video.mp4") # type: ignore
        audio_path = audio_stream.download(output_path=destino, filename="temp_audio.mp4") # type: ignore

        # Sanitiza título para nome do arquivo
        titulo_sanitizado = re.sub(r'[<>:"/\\|?*]', "_", yt.title)
        saida_path = destino / f"{titulo_sanitizado}.mp4"

        # Mescla com ffmpeg
        os.system(f'ffmpeg -y -i "{video_path}" -i "{audio_path}" -c copy "{saida_path}"')

        # Remove arquivos temporários
        os.remove(video_path) # type: ignore
        os.remove(audio_path) # type: ignore

        messagebox.showinfo("Sucesso", f"Vídeo salvo em:\n{saida_path}")
    
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro:\n{str(e)}")

# Criando janela principal
root = tk.Tk()
root.title("Download de Vídeos YouTube")
root.geometry("500x150")

# Label e Entry para URL
label_url = tk.Label(root, text="Insira a URL do YouTube:")
label_url.pack(pady=10)

entry_url = tk.Entry(root, width=60)
entry_url.pack(pady=5)

# Botão para iniciar download
botao_download = tk.Button(root, text="Baixar Vídeo", command=baixar_video, bg="green", fg="white")
botao_download.pack(pady=20)

# Inicia a aplicação
root.mainloop()
