import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def select_file():
    """Abre uma janela para selecionar a imagem"""
    file_path = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)

def convert_to_ico():
    """Converte a imagem selecionada para ícone .ico"""
    input_path = entry_path.get()
    if not input_path:
        messagebox.showwarning("Aviso", "Selecione uma imagem primeiro!")
        return
    
    try:
        img = Image.open(input_path)
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}.ico"
        
        img.save(output_path, format="ICO", sizes=[(256, 256)])
        messagebox.showinfo("Sucesso", f"Ícone gerado em:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao converter: {e}")

# ----------------- Interface Tkinter -----------------
root = tk.Tk()
root.title("Conversor para Ícone (.ico)")
root.geometry("400x150")
root.resizable(False, False)

# Entrada de caminho
frame = tk.Frame(root)
frame.pack(pady=20)

entry_path = tk.Entry(frame, width=40)
entry_path.pack(side=tk.LEFT, padx=5)

btn_browse = tk.Button(frame, text="Procurar", command=select_file)
btn_browse.pack(side=tk.LEFT)

# Botão de conversão
btn_convert = tk.Button(root, text="Converter para .ico", command=convert_to_ico)
btn_convert.pack(pady=10)

root.mainloop()
