import random
import matplotlib.pyplot as plt
import seaborn as sns


def gerar_mapa(tamanho):
    return [[random.randint(10, 100) for _ in range(tamanho)] for _ in range(tamanho)]


def propagar_fogo_por_distancia(linha_inicial, col_inicial, tamanho):
    mapa_fogo = [[0.0 for _ in range(tamanho)] for _ in range(tamanho)]
    for i in range(tamanho):
        for j in range(tamanho):
            distancia = abs(i - linha_inicial) + abs(j - col_inicial)

            intensidade_base = 1.0 - 0.15 * distancia

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


def processar_mapa_densidade_agrupado(mapa_densidade, tamanho):
    agrupamento_densidade = {}

    for linha in range(tamanho):
        for coluna in range(tamanho):
            valor_densidade = mapa_densidade[linha][coluna]

            if valor_densidade == 0:
                continue
            else:
                valor_decimal = valor_densidade / 100.0

                chave_principal = f"{valor_decimal:.1f}"

                valor_fogo_formatado = f"{valor_decimal:.2f}"

                coordenadas_str = f"{linha},{coluna}"

                if chave_principal not in agrupamento_densidade:
                    agrupamento_densidade[chave_principal] = {
                        "valores_fogo": [],
                        "coordenadas": [],
                    }

                agrupamento_densidade[chave_principal]["valores_fogo"].append(
                    valor_fogo_formatado
                )
                agrupamento_densidade[chave_principal]["coordenadas"].append(
                    coordenadas_str
                )

    return agrupamento_densidade


def printa_dict2(dict):
    for key in dict.keys():
        print(f"{key}: {dict[key]}")


def printa_dict(dict):
    for key in dict.keys():
        print(f"{key}: {printa_dict2(dict[key])}")


def simular():
    tamanho = 10

    mapa_densidade = gerar_mapa(tamanho)

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

    print("\n📦 Processando e exibindo o mapa de densidade agrupado:")
    resultado_agrupado = processar_mapa_densidade_agrupado(mapa_densidade, tamanho)
    printa_dict(resultado_agrupado)


simular()
