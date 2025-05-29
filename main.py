import random
import matplotlib.pyplot as plt
import seaborn as sns


# Gera um mapa de densidade (apenas para referência visual)
def gerar_mapa(tamanho):
    """
    Gera um mapa de densidade aleatória.
    Atualmente não é usado na simulação de propagação do fogo, mas pode ser útil para futuras extensões.
    """
    return [[random.randint(10, 100) for _ in range(tamanho)] for _ in range(tamanho)]


# Calcula o índice de devastação baseado na distância do ponto inicial
def propagar_fogo_por_distancia(linha_inicial, col_inicial, tamanho):
    """
    Calcula o mapa de devastação do fogo com base na distância de Manhattan
    do ponto de origem. Adiciona uma pequena aleatoriedade e garante precisão de 0.01.

    Args:
        linha_inicial (int): A linha de origem do fogo.
        col_inicial (int): A coluna de origem do fogo.
        tamanho (int): O tamanho da grade (tamanho x tamanho).

    Returns:
        list[list[float]]: Uma matriz representando o mapa de devastação do fogo.
    """
    mapa_fogo = [[0.0 for _ in range(tamanho)] for _ in range(tamanho)]
    for i in range(tamanho):
        for j in range(tamanho):
            # Calcula a distância de Manhattan do ponto inicial
            distancia = abs(i - linha_inicial) + abs(j - col_inicial)

            # Calcula a intensidade base (diminui 0.15 por unidade de distância para um raio um pouco maior)
            intensidade_base = 1.0 - 0.15 * distancia  # Alterado de 0.2 para 0.15

            intensidade_final = 0.0  # Inicializa como 0.0 por padrão

            # Aplica aleatoriedade apenas se a intensidade base for positiva
            if intensidade_base > 0:
                # Adiciona uma variação aleatória proporcional à intensidade base
                # A variação é entre -0.05 e +0.05
                variacao = random.uniform(-0.05, 0.05)
                intensidade_com_aleatoriedade = intensidade_base + variacao

                # Garante que os valores fiquem entre 0.0 e 1.0
                intensidade_final = max(0.0, min(1.0, intensidade_com_aleatoriedade))

            # Arredonda para duas casas decimais (precisão de 0.01)
            intensidade_final = round(intensidade_final, 2)

            mapa_fogo[i][j] = intensidade_final
    return mapa_fogo


# Exibe o mapa de calor usando seaborn e matplotlib
def exibir_heatmap(matriz):
    """
    Exibe um mapa de calor visual da matriz de devastação.

    Args:
        matriz (list[list[float]]): A matriz de devastação a ser exibida.
    """
    plt.figure(figsize=(6, 5))
    sns.heatmap(matriz, cmap="YlOrRd", linewidths=0.5, linecolor='gray', square=True,
                cbar_kws={'label': 'Índice de Devastação'})
    plt.title("Mapa de Calor da Propagação do Fogo")
    plt.xlabel("Colunas")
    plt.ylabel("Linhas")
    plt.show()


# Exibe a matriz no terminal
def mostrar_matriz(matriz):
    """
    Exibe a matriz de devastação no terminal com os valores formatados.

    Args:
        matriz (list[list[float]]): A matriz de devastação a ser exibida.
    """
    for linha in matriz:
        # Formata cada valor para ter duas casas decimais
        print(" ".join(f"{v:.2f}" for v in linha))


# Simulação principal
def simular():
    """
    Função principal que executa a simulação de propagação do fogo,
    solicitando a entrada do usuário e exibindo os resultados.
    """
    tamanho = 10  # Define o tamanho da grade da simulação (10x10)

    # O mapa de densidade é gerado, mas não é usado na lógica de propagação de fogo atual
    mapa_densidade = gerar_mapa(tamanho)

    print("[🔥] Simulação de propagação de fogo por distância iniciada.")
    try:
        # Solicita ao usuário a linha e coluna de origem do fogo
        linha = int(input(f"Digite a linha de origem do fogo (0 a {tamanho - 1}): "))
        coluna = int(input(f"Digite a coluna de origem do fogo (0 a {tamanho - 1}): "))

        # Verifica se as coordenadas estão dentro do limite da grade (0 a tamanho-1)
        if not (0 <= linha < tamanho and 0 <= coluna < tamanho):
            raise ValueError(
                "Coordenadas fora do limite. Por favor, digite valores entre 0 e " + str(tamanho - 1) + ".")
    except ValueError as e:
        # Captura erros de entrada inválida (não-números ou fora do limite)
        print(f"Erro: {e}")
        return  # Sai da função se houver um erro

    # Calcula o mapa de devastação do fogo com base nas coordenadas fornecidas
    mapa_fogo = propagar_fogo_por_distancia(linha, coluna, tamanho)

    print("\n📊 Matriz de devastação (texto):")
    mostrar_matriz(mapa_fogo)

    print("\n🖼️ Exibindo mapa de calor...")
    exibir_heatmap(mapa_fogo)


# Roda a simulação diretamente
simular()
