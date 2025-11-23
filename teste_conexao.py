import os
from groq import Groq

print("--- INICIANDO DIAGNÓSTICO LANCELOT ---")

# 1. Perguntar a chave
api_key = input("Cole sua API Key da Groq aqui e dê Enter: ").strip() 
# O .strip() remove espaços vazios automaticamente!

print(f"\n1. Chave recebida (Primeiros 5 chars): {api_key[:5]}...")

try:
    print("2. Tentando conectar com a Groq...")
    client = Groq(api_key=api_key)
    
    # Teste simples de chat (sem áudio, só texto)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Diga 'Olá Lancelot' se estiver me ouvindo."}
        ],
        model="llama3-8b-8192",
    )

    resposta = chat_completion.choices[0].message.content
    print(f"\n✅ SUCESSO! A Groq respondeu: {resposta}")
    print("Conclusão: Sua chave e internet estão ótimas. O problema pode ser o tamanho do áudio no app principal.")

except Exception as e:
    print("\n❌ FALHA NA CONEXÃO.")
    print("Detalhe do erro:")
    print(e)
    print("\nSOLUÇÕES POSSÍVEIS:")
    print("1. Desative temporariamente o Antivírus/Firewall.")
    print("2. Verifique se você está conectado a uma VPN (desligue-a).")
    print("3. Gere uma nova chave na Groq (console.groq.com).")

input("\nPressione Enter para sair...")