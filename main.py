import random
from emojis import emojis

class invalid_character(Exception):
    pass


# Função feita para gerar as cartas aleatoriamente
def generate_random_cards():
    list_01 = random.sample(range(0, 8), 8)
    list_02 = random.sample(range(0, 8), 8)
    result = []
    for index in range(0, 8):
        result.append(list_01[index])
        result.append(list_02[index])
    return result

# Função para mostrar o tabuleiro completo
def show_completed_game(my_list):
    for index, item in enumerate(my_list):
        print(emojis[item], end=(
            '\n' if (index + 1) % 4 == 0 else '\t'
        ))

# Função para mostrar o tabuleiro nas escolhas
def show_game(my_list, hits):
    visible_list = [emojis[my_list[i]] if i + 1 in hits else str(i+1) for i in range(len(my_list))]
    for index, item in enumerate(visible_list):
        print(item, end=('\n' if (index + 1) % 4 == 0 else '\t'))
    print('\nEscolha um número para revelar o emoji:')

# Função praticamente principal 
def play_game():
    my_list = generate_random_cards()
    hits = []
    score = 1000

    while True:
        try:
            print('-------> JOGO EM ANDAMENTO <-------')
            show_game(my_list, hits)

            first_choice = int(input("Escolha o primeiro número: "))

            if first_choice in hits:
                print("Número inválido ou já foi escolhido. Tente novamente!")
                continue

            if first_choice in my_list:
                print(f"Você escolheu o número {first_choice}. O emoji correspondente é: {emojis[my_list[first_choice-1]]}")
                second_choice = int(input("Escolha o segundo número: "))

                if second_choice == first_choice or second_choice in hits:
                    print("Número inválido ou já foi escolhido. Tente novamente!")
                    continue

                if second_choice in my_list:
                    if my_list[first_choice-1] == my_list[second_choice-1]:
                        print(f"Par encontrado! Você ganhou 1 ponto!")
                        score += 50
                        hits.extend([first_choice, second_choice])
                    else:
                        print(f"Você não acertou. Tente novamente!")
                        score -= 50
                else:
                    print("Número inválido. Tente novamente!")
            else:
                print("Número inválido. Tente novamente!")

            if len(hits) == len(my_list):
                print("Parabéns! Você encontrou todos os pares!")
                break
        except invalid_character:
            print("Caracter invalido!")

    print('-------> JOGO COMPLETO <-------')
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
    # Função para o usuario colocar o nome desejado
    username = str(input("Qual é o seu nome de usuário: ")).upper()
    return username

def main():
    username = login()
    confirm_menu_option(username)

if __name__ == "__main__":
    main()
