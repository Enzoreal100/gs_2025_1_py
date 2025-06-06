import random
import matplotlib.pyplot as plt
import seaborn as sns


def propagar_fogo_por_distancia(linha_inicial, col_inicial, tamanho):

    mapa_fogo = [[0.0 for _ in range(tamanho)] for _ in range(tamanho)]
    for i in range(tamanho):
        for j in range(tamanho):
            distancia = abs(i - linha_inicial) + abs(j - col_inicial)

            intensidade_base = 1.0 - 0.015 * distancia

            intensidade_final = 0.0

            if intensidade_base > 0:
                variacao = random.uniform(-0.05, 0.05)
                intensidade_com_aleatoriedade = intensidade_base + variacao

                intensidade_final = max(0.0, min(1.0, intensidade_com_aleatoriedade))

            intensidade_final = round(intensidade_final, 2)

            mapa_fogo[i][j] = intensidade_final
    return mapa_fogo


def exibir_heatmap(matriz):
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        matriz,
        cmap="YlOrRd",
        linewidths=0.5,
        linecolor="gray",
        square=True,
        cbar_kws={"label": "Índice de Devastação"},
    )
    plt.title("Mapa de Calor da Propagação do Fogo")
    plt.xlabel("Colunas")
    plt.ylabel("Linhas")
    plt.show()


def mostrar_matriz(matriz):
    for linha in matriz:
        print(" ".join(f"{v:.2f}" for v in linha))


def processar_mapa_fogo_agrupado(mapa_fogo, tamanho):
    agrupamento_fogo = {}

    for linha in range(tamanho):
        for coluna in range(tamanho):
            valor_fogo = mapa_fogo[linha][coluna]

            if valor_fogo < 0.1:
                continue

            # Calcula a chave principal com base no primeiro dígito decimal
            chave_principal = f"{int(valor_fogo * 10) / 10:.1f}"
            if (
                valor_fogo == 1.0
            ):  # Para garantir que 1.0 seja agrupado corretamente como "1.0"
                chave_principal = "1.0"

            coordenadas_str = f"{linha},{coluna}"

            if chave_principal not in agrupamento_fogo:
                agrupamento_fogo[chave_principal] = {
                    "intensidades_originais": [],  # Renomeado para refletir o mapa de fogo
                    "coordenadas": [],
                }

            agrupamento_fogo[chave_principal]["intensidades_originais"].append(
                valor_fogo
            )
            agrupamento_fogo[chave_principal]["coordenadas"].append(coordenadas_str)

    return agrupamento_fogo


def printa_dict(resultados_simulacao):
    for linha, dados in resultados_simulacao.items():
        print(f"Linha {linha}: {dados['intensidades_originais']}")


# Função Quick Sort para ordenar as intensidades
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivo = arr[0]
        menores = [x for x in arr[1:] if x <= pivo]
        maiores = [x for x in arr[1:] if x > pivo]
        return quick_sort(menores) + [pivo] + quick_sort(maiores)


# Função Busca Binária para encontrar a intensidade na lista ordenada
def busca_binaria(arr, alvo):
    inicio = 0
    fim = len(arr) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        if arr[meio] == alvo:
            return meio
        elif arr[meio] < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1


def menu(resultados_simulacao):
    while True:
        msg = (
            "\nO que deseja fazer?\n"
            "\t1. Mostrar o dano em todas as áreas afetadas\n"
            "\t2. Mostrar o dano em uma área específica\n"
            "\t3. Sair\n"
            "\t4. Buscar intensidade com Quick Sort e Busca Binária\n\n"
        )
        resposta = input(msg)

        while not resposta.isnumeric() or resposta not in {"1", "2", "3", "4"}:
            print("Por favor, digite um valor válido.\n")
            resposta = input(msg)

        if resposta == "1":
            print("\n📦 Resultados da simulação:")
            printa_dict(resultados_simulacao)

            for chave, valor in resultados_simulacao.items():
                intensidades = valor['intensidades_originais']
                plt.plot(intensidades, label=f"Linha {chave}")

            plt.title("Intensidade do fogo nas áreas afetadas agrupadas")
            plt.xlabel("Posição na linha")
            plt.ylabel("Intensidade")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        elif resposta == "2":
            linha = input("Digite a linha que deseja consultar (ex: 12.0): ")
            chave = f"{float(linha):.1f}"
            if chave in resultados_simulacao:
                intensidades = resultados_simulacao[chave]['intensidades_originais']

                # Gráfico de barras simples
                x = list(range(len(intensidades)))
                y = intensidades
                plt.figure(figsize=(10, 4))
                plt.bar(x, y, color='orange')
                plt.xlabel("Posição na linha")
                plt.ylabel("Intensidade")
                plt.title(f"Intensidade do fogo na posição {chave}")
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                plt.tight_layout()
                plt.show()
            else:
                print("Linha não encontrada.\n")

        elif resposta == "3":
            print("Encerrando...")
            break

        elif resposta == "4":
            linha = input("Digite a linha para ordenar e buscar (ex: 0.5): ")
            chave = f"{float(linha):.1f}"

            if chave in resultados_simulacao:
                intensidades_originais = resultados_simulacao[chave]['intensidades_originais']
                intensidades_ordenadas = quick_sort(intensidades_originais.copy())

                print("\n🌡️ Intensidades ordenadas (Quick Sort):")
                print(intensidades_ordenadas)

                alvo = float(input("Digite a intensidade de fogo a ser buscada: "))
                idx_ordenado = busca_binaria(intensidades_ordenadas, alvo)

                if idx_ordenado != -1:
                    coordenadas = [i for i, val in enumerate(intensidades_originais) if val == alvo]
                    print(f"\n✅ Intensidade {alvo} encontrada:")
                    print(f"📊 Índice na lista ordenada: {idx_ordenado}")
                    print(f"📍 Coordenada(s) na linha original: {coordenadas}\n")
                else:
                    print(f"❌ Intensidade {alvo} não encontrada na linha {chave}.\n")
            else:
                print("Linha não encontrada.\n")


def simular(tamanho=50):
    print("[🔥] Simulação de propagação de fogo por distância iniciada.")
    try:
        linha = int(input(f"Digite a linha de origem do fogo (0 a {tamanho - 1}): "))
        coluna = int(input(f"Digite a coluna de origem do fogo (0 a {tamanho - 1}): "))

        if not (0 <= linha < tamanho and 0 <= coluna < tamanho):
            raise ValueError(
                "Coordenadas fora do limite. Por favor, digite valores entre 0 e "
                + str(tamanho - 1)
                + "."
            )
    except ValueError as e:
        print(f"Erro: {e}")
        return

    mapa_fogo = propagar_fogo_por_distancia(linha, coluna, tamanho)

    print("\n📊 Matriz de devastação (texto):")
    mostrar_matriz(mapa_fogo)

    print("\n🖼️ Exibindo mapa de calor...")
    exibir_heatmap(mapa_fogo)

    print("\n📦 Processando e exibindo o mapa de intensidade do fogo agrupado:")
    resultado_agrupado_fogo = processar_mapa_fogo_agrupado(mapa_fogo, tamanho)
    print(
        "Agrupamento de intensidades de fogo (valor aproximado: {intensidades originais, coordenadas}):"
    )
    return resultado_agrupado_fogo


resultados_simulacao = simular()
if resultados_simulacao:
    answer = menu(resultados_simulacao)
