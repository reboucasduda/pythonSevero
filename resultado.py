import customtkinter as ctk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import re


def achar_resultado(interface, entrada_funcao, entrada_chute):
    funcao = entrada_funcao.get()
    chute = entrada_chute.get()
    janela2 = ctk.CTkToplevel(interface)
    janela2.title("Resultado")
    janela2.geometry("600x450")
    janela2.after(100, janela2.focus)

    mensagem = ctk.CTkLabel(
        janela2,
        text="Calculando a raiz...",
        font=("Arial", 16, "bold"),
    )
    mensagem.pack(pady=(20, 10))

    area_grafico = ctk.CTkFrame(janela2)
    area_grafico.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # Funcao = input("Digite uma função (ex: x^2, sen(x), exp(x)): ")  #Função que o usuario irá digitar

    # Trocar vírgula por ponto, maiscula por minuscula, e afins
    funcao_Corrigida = funcao.lower().replace(',', '.').replace('^', '**')
    funcao_Corrigida = re.sub(r'(\d)([a-z(])', r'\1*\2', funcao_Corrigida)

    # O chute inicial (é obrigatório pro método de Newton ter de onde começar)
    # chute_str = input("Digite o chute inicial: ")
    chute_inicial = float(chute.replace(',', '.')) #Coloquei essa condição pra caso o usuario coloque , no chute inicial


    def f(x):
        # Dicionário com as operações matemáticas pro eval() conseguir fazer a tradução pra numeros
        dicionario = {'x': x,
            # Trigonométricas
            'sin': np.sin, 'sen': np.sin,
            'cos': np.cos, 'tan': np.tan,
            # Trigonométricas inversas
            'arcsin': np.arcsin, 'arcsen': np.arcsin,
            'arccos': np.arccos, 'arctan': np.arctan,
            # Hiperbólicas
            'sinh': np.sinh, 'cosh': np.cosh, 'tanh': np.tanh,
            # Exponenciais e Logaritmos
            'exp': np.exp,
            'ln': np.log,        # log natural (base e)
            'log': np.log10,     # log na base 10
            'log2': np.log2,     # log na base 2
            # Extras de Engenharia
            'sqrt': np.sqrt,     # Raiz quadrada
            'abs': np.abs,       # Módulo / Valor absoluto
            # Constantes
            'pi': np.pi,
            'e': np.e}
        return eval(funcao_Corrigida, dicionario)

    #Função que calcula a derivada numérica
    def derivada(x):
        if x == 0:
            h = 0.00001
        else:
            h = 0.00001 * abs(x) # Botei abs pra caso o ponto seja negativo

        y_frente = f(x + h)
        y_tras = f(x - h)

        return (y_frente - y_tras) / (2 * h) # Calcula a inclinação da reta tangente

    #=========================================================================
    #METODO DE NEWTON  EM AÇÃO
    x_atual = chute_inicial
    tolerancia = 0.001
    erro = 1.0
    iteracao = 1

    #limite maximo de 100 iteraçoes pra nao crashar o computador ( mas se quiserem tirem)
    max_iteracoes = 100
    motivo_erro = None

    # print("TESTANDO POR ROUND O MÉTODO DE NEWTON ")


    #PLOTANDO GRAFICO
    amplitude = max(10, abs(chute_inicial)+2)#janela do grafico
    X = np.linspace(-amplitude, amplitude, 10000)#janela do grafico
    Y = f(X) # pegando a função
    fig = Figure(figsize=(6, 4), tight_layout=True)
    ax = fig.add_subplot(111)
    ax.axhline(0, color="black") #eixo horizontal
    curva = ax.plot(X, Y, color="blue")
    ponto_inicial, = ax.plot(
        chute_inicial,
        f(chute_inicial),
        "go",
        markersize=8
    )

    ax.axhline(0, color="black")
    ax.grid()

    ax.relim()
    ax.autoscale_view()
    tangente, = ax.plot(
        [], [],
        color="purple",
        linestyle="--",
        linewidth=1.5)#reta tangente so que sem parametro
    ponto_curva, = ax.plot([], [], "bo") #pontos pecorridos
    ponto_raiz, = ax.plot([], [], "ro")#raiz

    ax.grid()

    #Substituído, não estava aparecendo o gráfico
    #COMANDO QUE PERMITEM O GRAFICO SEM DINAMICO
    # plt.ion()
    # plt.show(block=False)
    # fig.canvas.draw_idle()
    # plt.pause(3) #deixa a curva parada um bom tempo
                       
    canvas = FigureCanvasTkAgg(fig, master=area_grafico)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()
    janela2.update_idletasks()

    #sumindo a marcação do ponto inicial
    ponto_inicial.set_visible(False)
    #progamando zom
    # Limites horizontais atuais
    x_min, x_max = ax.get_xlim()

    zoom = 1.5

    centro_x = (x_min + x_max) / 2
    largura = (x_max - x_min) / zoom

    novo_x_min = centro_x - largura / 2
    novo_x_max = centro_x + largura / 2

    # Aplica o zoom horizontal
    ax.set_xlim(novo_x_min, novo_x_max)

    # Identifica os valores da curva na região visível
    mascara = (X >= novo_x_min) & (X <= novo_x_max)
    Y_visivel = Y[mascara]
    Y_visivel = Y_visivel[np.isfinite(Y_visivel)]

    # Ajusta a escala vertical
    if len(Y_visivel) > 0:
        y_min = min(np.min(Y_visivel), 0)
        y_max = max(np.max(Y_visivel), 0)

        margem = max((y_max - y_min) * 0.1, 1)

        ax.set_ylim(y_min - margem, y_max + margem)

    canvas.draw()
    ##################################
    #Irá repetir as contas até a diferença  (o erro ser menor do que o estabelecido) ficar menor que a tolerância de 0.001
    while erro > tolerancia and iteracao <= max_iteracoes:
        y_atual = f(x_atual)
        derivada_atual = derivada(x_atual)

        #Proteção caso a derivada de zero (linha reta sem inclinação, logo nao tem)
        if derivada_atual == 0:
            motivo_erro = "A derivada é zero; o método de Newton não pode continuar."
            break
        Y_tangente = y_atual + derivada_atual * (X - x_atual)#to definindo a reta tangente atraves da formula la
        #A fórmula do método de Newton pra vcs enxergarem: x_novo = x - f(x)/f"(x)
        x_novo = x_atual - (y_atual / derivada_atual)
    ####################################GRAFICOO#################################################
        tangente.set_data(X, Y_tangente) #aplicando as coordenadas
        #print("Tangente:", Y_tangente[:5])
        #PONTOS DINAMICOS
        ponto_curva.set_data([x_atual], [y_atual])
        ponto_raiz.set_data([x_novo], [0])
    #autolização
        #Substituído, não estava aparecendo o gráfico
        # fig.canvas.draw_idle()
        # plt.pause(1) #TEMPO ENTRE CADA MUDANÇA
        canvas.draw()
        janela2.update_idletasks()
    ###############################CABOU O GRAFICO########################################################


        #Diferença entre o valor novo e o antigo pra saber a hora de parar as iteraçoes
        erro = abs(x_novo - x_atual)

        # print(f"Iteração {iteracao}: x = {x_novo:.6f}")

        #Atualiza o x pro próximo loop
        x_atual = x_novo
        iteracao += 1
    if erro <= tolerancia:
        mensagem.configure(
            text=f"Função: {funcao}\nRaiz aproximada: {x_atual:.4f}"
        )
    elif motivo_erro:
        mensagem.configure(text=motivo_erro)
    else:
        mensagem.configure(
            text=f"O método não convergiu após {max_iteracoes} iterações."
        )

    # print(f"Resultado Final: O valor encontrado é {x_atual:.6f}")