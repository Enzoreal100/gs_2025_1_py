import random
import matplotlib.pyplot as plt
import seaborn as sns


def propagar_fogo_por_distancia(linha_inicial, col_inicial, tamanho):

    mapa_fogo = [[0.0 for _ in range(tamanho)] for _ in range(tamanho)]
    for i in range(tamanho):
        for j in range(tamanho):
            distancia = abs(i - linha_inicial) + abs(j - col_inicial)

            intensidade_base = 1.0 - 0.05 * distancia

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
            if valor_fogo == 1.0: # Para garantir que 1.0 seja agrupado corretamente como "1.0"
                chave_principal = "1.0"

            coordenadas_str = f"{linha},{coluna}"

            if chave_principal not in agrupamento_fogo:
                agrupamento_fogo[chave_principal] = {
                    "intensidades_originais": [], # Renomeado para refletir o mapa de fogo
                    "coordenadas": [],
                }

            agrupamento_fogo[chave_principal]["intensidades_originais"].append(
                valor_fogo
            )
            agrupamento_fogo[chave_principal]["coordenadas"].append(
                coordenadas_str
            )

    return agrupamento_fogo


def printa_dict(dict):
    for key in dict.keys():
        print(f"{key}: \n"
              f"    intensidades_originais: {dict[key]['intensidades_originais']}\n "
              f"    coordenadas: {dict[key]['coordenadas']}\n")


def menu():
    msg = f'O que deseja fazer?\n \t1. mostrar o dano em todas as áreas afetadas\n \t2. mostrar o dano em uma área específica\n \t 3. Sair\n\n\n'
    print(msg)
    resposta = input()
    while not resposta.isnumeric():
        print("Por favor, digite um valor válido.\n\n")
        print(msg)
        resposta = input()
    return resposta


def simular(tamanho=10):
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
    print("Agrupamento de intensidades de fogo (valor aproximado: {intensidades originais, coordenadas}):")
    return resultado_agrupado_fogo

resultados_simulacao = simular(15)
answer = menu()