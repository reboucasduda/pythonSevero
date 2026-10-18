import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

interface = ctk.CTk()
interface.title('Teste')
interface.geometry('500x400')
interface.resizable(False, False)

#centralizando tudo
interface.grid_columnconfigure(0, weight=1)
interface.grid_columnconfigure(1, weight=1)

# Entrada da função
ctk.CTkLabel(interface, text='Digite sua função F(x) = 0:').grid(row=0, column=0, padx=10, pady=(40, 10), sticky='e')
entrada_funcao = ctk.CTkEntry(interface, width=200, placeholder_text='ex: x^3 - 2*x - 5')
entrada_funcao.grid(row=0, column=1, padx=10, pady=(40, 10), sticky='w')

# Entrada do chute
ctk.CTkLabel(interface, text='Digite o chute inicial:').grid(row=1, column=0, padx=10, pady=10, sticky='e')
entrada_chute = ctk.CTkEntry(interface, width=200, placeholder_text='ex: 2, 3.5')
entrada_chute.grid(row=1, column=1, padx=10, pady=10, sticky='w')

def achar_resultado():
    funcao = entrada_funcao.get()
   # funcao_transf = float(funcao)
    chute = entrada_chute.get()
    #chute_transf = float(chute)
    janela2 = ctk.CTkToplevel(interface)
    janela2.title('Resultado')
    janela2.geometry('600x450')
    janela2.after(100, janela2.focus)

    # Mensagem em cima
    mensagem = ctk.CTkLabel(
        janela2,
        text=f'Resultado encontrado! sua raiz é: raiz ',
        font=('Arial', 16, 'bold')
    )
    mensagem.configure(text=f'Raiz aproximada: {funcao} com chute inicial: {chute}')
    mensagem.pack(pady=(20, 10))

    #Espaço para o gráfico
    area_grafico = ctk.CTkFrame(janela2)
    area_grafico.pack(fill='both', expand=True, padx=20, pady=(0, 20))

calcular = ctk.CTkButton(interface, text='Calcular', width=200, height=40, command=achar_resultado)
calcular.grid(row=2, column=0, columnspan=2, pady=30)

interface.mainloop()