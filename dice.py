import random

# Tabelas de arte ASCII para cada tipo de dado
ASCII_DICE = {
    4: {
        1: ["  ^  ", " / \\ ", "/_1_\\"],
        2: ["  ^  ", " /2\\ ", "/___\\"],
        3: ["  ^  ", " /3\\ ", "/___\\"],
        4: ["  ^  ", " /4\\ ", "/___\\"],
    },
    6: {
        1: ["+-----+", "|     |", "|  *  |", "|     |", "+-----+"],
        2: ["+-----+", "|*    |", "|     |", "|    *|", "+-----+"],
        3: ["+-----+", "|*    |", "|  *  |", "|    *|", "+-----+"],
        4: ["+-----+", "|*   *|", "|     |", "|*   *|", "+-----+"],
        5: ["+-----+", "|*   *|", "|  *  |", "|*   *|", "+-----+"],
        6: ["+-----+", "|*   *|", "|*   *|", "|*   *|", "+-----+"],
    },
    12: {},  # ASCII simplificado
    20: {},  # ASCII simplificado
}

def roll_dice(sides: int, amount: int = 1):
    if sides not in [4, 6, 12, 20]:
        print(f"Dado D{sides} não suportado.")
        return

    print(f"\nRolando {amount} D{sides}...\n")

    results = [random.randint(1, sides) for _ in range(amount)]
    show_dice(results, sides)

def show_dice(results, sides):
    if sides in [4, 6] and sides in ASCII_DICE:
        # Exibe arte ASCII específica
        lines = [""] * len(ASCII_DICE[sides][1])
        for result in results:
            art = ASCII_DICE[sides].get(result, ["[???]"])
            for i, line in enumerate(art):
                lines[i] += "   " + line
        for line in lines:
            print(line)
    else:
        # ASCII genérico para D12, D20 etc.
        for result in results:
            print(f"[ D{sides} → {result} ]")

# Exemplo de uso:
if __name__ == "__main__":
    while True:
        try:
            user_input = input("\nDigite o dado (ex: 1d6, 2d20) ou 'sair': ").strip().lower()
            if user_input == "sair":
                break

            if "d" not in user_input:
                print("Formato inválido. Use algo como 2d6 ou 1d20.")
                continue

            amount_str, sides_str = user_input.split("d")
            amount = int(amount_str)
            sides = int(sides_str)

            roll_dice(sides, amount)

        except Exception as e:
            print(f"Erro: {e}")
