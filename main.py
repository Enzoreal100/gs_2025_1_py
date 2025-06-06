import random
import matplotlib.pyplot as plt
import seaborn as sns


# Responsavel por calcular a propagação do fogo
# Notação O grande: O(n^2)
def propagar_fogo_por_distancia(linha_inicial, col_inicial, tamanho):
    mapa_fogo = [[0.0 for _ in range(tamanho)] for _ in range(tamanho)]
    for i in range(tamanho):
        for j in range(tamanho):
            distancia = abs(i - linha_inicial) + abs(j - col_inicial)

            # Calcula certa aleatoriedade no fogo
            intensidade_base = 1.0 - 0.015 * distancia

            intensidade_final = 0.0

            if intensidade_base > 0:
                variacao = random.uniform(-0.05, 0.05)
                intensidade_com_aleatoriedade = intensidade_base + variacao

                intensidade_final = max(0.0, min(1.0, intensidade_com_aleatoriedade))

            intensidade_final = round(intensidade_final, 2)

            mapa_fogo[i][j] = intensidade_final
    return mapa_fogo


# exibe o mapa de calor
# Notação O grande: O(n^2)
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


# mostra a matriz de forma organizada
# Notação O grande: O(n^2)
def mostrar_matriz(matriz):
    for linha in matriz:
        print(" ".join(f"{v:.2f}" for v in linha))


# Agrupa os dados de intensidade do fogo.
# Notação O grande: O(n^2)
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


# Imprime o dicionário de resultados agrupados.
# Notação O grande: O(n^2) (no pior caso, devido à impressão de listas)
def printa_dict(resultados_simulacao):
    for linha, dados in resultados_simulacao.items():
        print(f"Linha {linha}: {dados['intensidades_originais']}")


# Função Quick Sort para ordenar as intensidades
# Notação O grande: O(N log N) (caso médio)
def quick_sort(arr, key=None):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]

    # aplica a key function se disponível, senão usa o elem diretamente
    if key:
        less = [x for x in arr if key(x) < key(pivot)]
        equal = [x for x in arr if key(x) == key(pivot)]
        greater = [x for x in arr if key(x) > key(pivot)]
    else:
        less = [x for x in arr if x < pivot]
        equal = [x for x in arr if x == pivot]
        greater = [x for x in arr if x > pivot]

    return quick_sort(less, key=key) + equal + quick_sort(greater, key=key)


# Função Busca Binária para encontrar a intensidade na lista ordenada
# Notação O grande: O(log N)
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


# func que mostra todas as áreas afetadas
# Notação O grande: O(n^2)
def todas_areas_afetadas(resultados_simulacao):
    print("\n📦 Resultados da simulação:")
    printa_dict(resultados_simulacao)

    for chave, valor in resultados_simulacao.items():
        intensidades = valor["intensidades_originais"]
        plt.plot(intensidades, label=f"Linha {chave}")
        plt.title("Intensidade do fogo nas áreas afetadas agrupadas")
        plt.xlabel("Posição na linha")
        plt.ylabel("Intensidade")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


# func que mostra a área selecionada
# Notação O grande: O(n^2)
def area_especifica(resultados_simulacao):
    linha = input("Digite a intensidade geral de fogo que deseja consultar (ex: 0.5): ")
    chave = f"{float(linha):.1f}"
    if chave in resultados_simulacao:
        intensidades = resultados_simulacao[chave]["intensidades_originais"]

        # Gráfico de barras simples
        x = list(range(len(intensidades)))
        y = intensidades
        plt.figure(figsize=(10, 4))
        plt.bar(x, y, color="orange")
        plt.xlabel("Posição na linha")
        plt.ylabel("Intensidade")
        plt.title(f"Intensidade do fogo na posição {chave}")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show()
    else:
        print("Linha não encontrada.\n")


# Func que busca a intensidade específica
# Notação O grande: O(N log N)
def buscar_intensidade(resultados_simulacao):
    linha = input(
        "Digite a intensidade geral de fogo que deseja ordenar e buscar (ex: 0.5): "
    )
    chave = f"{float(linha):.1f}"

    if chave in resultados_simulacao:
        intensidades_originais = resultados_simulacao[chave]["intensidades_originais"]
        coordenadas_originais = resultados_simulacao[chave]["coordenadas"]

        intensidades_com_coordenadas = list(
            zip(intensidades_originais, coordenadas_originais)
        )

        intensidades_com_coordenadas_ordenadas = quick_sort(
            intensidades_com_coordenadas, key=lambda x: x[0]
        )

        intensidades_ordenadas = [
            item[0] for item in intensidades_com_coordenadas_ordenadas
        ]
        coordenadas_ordenadas = [
            item[1] for item in intensidades_com_coordenadas_ordenadas
        ]

        print("\n🌡️ Intensidades ordenadas (Quick Sort):")
        print(intensidades_ordenadas)

        alvo = float(input("Digite a intensidade de fogo a ser buscada: "))

        idx_ordenado = busca_binaria(intensidades_ordenadas, alvo)

        if idx_ordenado != -1:
            coordenadas_encontradas = [
                coordenadas_originais[i]
                for i, val in enumerate(intensidades_originais)
                if val == alvo
            ]

            print(f"\n✅ Intensidade {alvo} encontrada:")
            print(f"📊 Índice na lista ordenada: {idx_ordenado}")
            print(f"📍 Coordenada(s) na linha original: {coordenadas_encontradas}\n")
        else:
            print(f"❌ Intensidade {alvo} não encontrada na linha {chave}.\n")
    else:
        print("Linha não encontrada.\n")


# Func responsável pela exibição e funcionamento do menu
# Notação O grande: O(1) por interação (ou dependente das funções chamadas)
def menu(resultados_simulacao):
    while True:
        msg = (
            "\nO que deseja fazer?\n"
            "\t1. Mostrar o dano em todas as áreas afetadas\n"
            "\t2. Mostrar o dano em uma área específica\n"
            "\t3. Buscar intensidade com Quick Sort e Busca Binária\n"
            "\t4. Sair\n\n"
        )
        resposta = input(msg)
        dict_ans = {
            "1": todas_areas_afetadas,
            "2": area_especifica,
            "3": buscar_intensidade,
            "4": exit,
        }

        while not resposta in dict_ans.keys():
            print("Por favor, digite um valor válido.\n")
            resposta = input(msg)

        if resposta == "4":
            dict_ans[resposta](("Encerrando..."))
        else:
            dict_ans[resposta](resultados_simulacao)


# Def responsável pela simulação dos dados de queimada
# Notação O grande: O(n^2)
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
