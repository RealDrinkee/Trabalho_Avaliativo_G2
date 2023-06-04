import pygame
import random
from emojis import emojis

#PATROCIO ChatGPT

# Inicialização do Pygame
pygame.init()

# Definição das cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definição das dimensões da janela
WIDTH = 400
HEIGHT = 400

# Definição do tamanho do card
CARD_WIDTH = 80
CARD_HEIGHT = 80

# Definição do espaçamento entre os cards
CARD_SPACING = 10

# Definição do tamanho da fonte
FONT_SIZE = 24

# Definição das posições dos cards
CARD_POSITIONS = [(CARD_SPACING + (CARD_WIDTH + CARD_SPACING) * x, CARD_SPACING + (CARD_HEIGHT + CARD_SPACING) * y)
                  for x in range(4) for y in range(4)]

# Criação da janela do jogo
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tabuleiro do Junin")

# Definição das fontes
font = pygame.font.Font(None, FONT_SIZE)

def generate_random_cards():
    # Função responsável por gerar uma lista de cartas aleatórias para o jogo
    list_01 = random.sample(range(0, 8), 8)
    list_02 = random.sample(range(0, 8), 8)
    result = []
    for index in range(0, 8):
        result.append(list_01[index])
        result.append(list_02[index])
    return result

def show_completed_game(my_list):
    # Função para exibir o tabuleiro completo do jogo
    for index, item in enumerate(my_list):
        emoji_text = emojis[item]
        text_surface = font.render(emoji_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(CARD_POSITIONS[index][0] + CARD_WIDTH // 2, CARD_POSITIONS[index][1] + CARD_HEIGHT // 2))
        window.blit(text_surface, text_rect)

def show_game(my_list, hits):
    # Função para exibir o tabuleiro atual do jogo
    for index, item in enumerate(my_list):
        if index + 1 in hits:
            emoji_text = emojis[item]
            text_surface = font.render(emoji_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(CARD_POSITIONS[index][0] + CARD_WIDTH // 2, CARD_POSITIONS[index][1] + CARD_HEIGHT // 2))
            window.blit(text_surface, text_rect)
        else:
            pygame.draw.rect(window, WHITE, (CARD_POSITIONS[index][0], CARD_POSITIONS[index][1], CARD_WIDTH, CARD_HEIGHT))
            number_text = font.render(str(index + 1), True, BLACK)
            number_rect = number_text.get_rect(center=(CARD_POSITIONS[index][0] + CARD_WIDTH // 2, CARD_POSITIONS[index][1] + CARD_HEIGHT // 2))
            window.blit(number_text, number_rect)

    pygame.display.flip()

def play_game():
    # Função principal que executa o jogo
    my_list = generate_random_cards()
    hits = []
    score = 1000

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for index, position in enumerate(CARD_POSITIONS):
                    card_rect = pygame.Rect(position[0], position[1], CARD_WIDTH, CARD_HEIGHT)
                    if card_rect.collidepoint(mouse_pos):
                        if index + 1 in hits:
                            print("Número inválido ou já foi escolhido. Tente novamente!")
                        elif index + 1 in my_list:
                            if len(hits) % 2 == 0:
                                print(f"Você escolheu o número {index + 1}. O emoji correspondente é: {emojis[my_list[index]]}")
                                score += 50
                                hits.append(index + 1)
                            else:
                                if my_list[hits[-1] - 1] == my_list[index]:
                                    print(f"Par encontrado! Você ganhou 1 ponto!")
                                    score += 50
                                    hits.append(index + 1)
                                else:
                                    print(f"Você não acertou. Tente novamente!")
                                    score -= 50
                        else:
                            print("Número inválido. Tente novamente!")

        window.fill(BLACK)
        show_game(my_list, hits)

        if len(hits) == len(my_list):
            print("Parabéns! Você encontrou todos os pares!")
            break

        pygame.display.flip()

    print('########### JOGO COMPLETO ###########')
    show_completed_game(my_list)
    print(f"Seu placar final: {score} pontos.")
    return score

def menu():
    # Função para exibir o menu de opções do jogo
    print("Tabuleiro do Junin")
    print("1 - Iniciar\n2 - Ranking\n3 - Sair")
    opc = int(input("Qual opção desejada: "))
    return opc

def confirm_menu_option(username):
    # Função para confirmar a opção escolhida no menu
    opc = 0
    while True:
        try:
            opc = menu()
            if opc == 1:
                first_option(username)
            elif opc == 2:
                show_ranking()
            elif opc == 3:
                print("Muito obrigado por jogar nosso game!")
                break
            else:
                print("Opção inválida!")
        except ValueError:
            print("Digite uma opção válida!")

def first_option(username):
    # Função para iniciar o jogo
    score = play_game()
    with open("users.txt", "a") as file:
        file.write(f"{username}: {score}\n")
        print("Informações do usuário salvas com sucesso!")

def show_ranking():
    # Função para exibir o ranking dos jogadores
    with open("users.txt", "r") as file:
        lines = file.readlines()
    users = []
    for line in lines:
        username, score = line.strip().split(":")
        users.append((username, int(score)))
    users.sort(key=lambda x: x[1], reverse=True)

    print("Ranking de Usuários:")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user[0]} - Score: {user[1]}")

def login():
    # Função para solicitar o nome de usuário do jogador
    username = str(input("Qual é o seu nome de usuário: ")).upper()
    return username

def main():
    # Função principal do programa
    username = login()
    confirm_menu_option(username)

if __name__ == "__main__":
    main()
