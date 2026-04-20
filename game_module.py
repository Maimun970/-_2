import random
import os

WORDS_FILE = "words.txt"
GALLOWS_FOLDER = "gallows"
MAX_MISTAKES = 6


def load_words():
    words_dict = {}
    with open(WORDS_FILE, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 2:
                    word, hint = parts
                    words_dict[word.lower()] = hint
    return words_dict


def get_random_word(words_dict):
    word_list = list(words_dict.keys())
    return random.choice(word_list)


def get_hint(words_dict, word):
    return words_dict.get(word, "Подсказка отсутствует")


def create_hidden_word(word, guessed_letters):
    result = ""
    for letter in word:
        if letter in guessed_letters:
            result += letter + " "
        else:
            result += "_ "
    return result.strip()


def load_gallows_stage(stage_number):
    filename = f"{GALLOWS_FOLDER}/stage_{stage_number}.txt"
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f"Стадия {stage_number} не найдена"


def is_word_guessed(word, guessed_letters):
    for letter in word:
        if letter not in guessed_letters:
            return False
    return True


def is_valid_letter(letter, guessed_letters):
    if len(letter) != 1:
        return False, "Введите только одну букву!"
    if not letter.isalpha():
        return False, "Введите букву!"
    if letter in guessed_letters:
        return False, "Вы уже вводили эту букву!"
    return True, ""


def get_game_state(mistakes):
    stage = load_gallows_stage(mistakes)
    return stage


def initialize_game():
    words_dict = load_words()
    word = get_random_word(words_dict)
    hint = get_hint(words_dict, word)
    guessed_letters = set()
    mistakes = 0
    return {
        'word': word,
        'hint': hint,
        'guessed_letters': guessed_letters,
        'mistakes': mistakes,
        'words_dict': words_dict
    }


def make_guess(game_state, letter):
    letter = letter.lower()
    word = game_state['word']
    
    if letter in word:
        game_state['guessed_letters'].add(letter)
        return True, "Правильно!"
    else:
        game_state['mistakes'] += 1
        return False, "Неправильно!"


def check_game_over(game_state):
    word = game_state['word']
    mistakes = game_state['mistakes']
    guessed_letters = game_state['guessed_letters']
    
    if is_word_guessed(word, guessed_letters):
        return True, "win"
    elif mistakes >= MAX_MISTAKES:
        return True, "lose"
    else:
        return False, ""


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_game_info(game_state, keys):
    current_word = game_state[keys['word']]
    current_guessed = game_state[keys['guessed']]
    current_mistakes = game_state[keys['mistakes']]
    current_hint = game_state[keys['hint']]
    
    print("\n" + "="*50)
    print(" ИГРА ВИСЕЛИЦА ".center(50, "="))
    print("="*50)
    print(get_game_state(current_mistakes))
    print("\n💡 Подсказка:", current_hint)
    print("\n Слово:", create_hidden_word(current_word, current_guessed))
    print("\n✅ Угаданные буквы:", ", ".join(sorted(current_guessed)) if current_guessed else "нет")
    print("❌ Ошибок:", current_mistakes, "из", MAX_MISTAKES)
    print("-"*50)


def get_user_input():
    try:
        letter = input("👉 Введите букву: ").lower()
        return letter
    except EOFError:
        return None


def show_game_result(game_state, result, keys):
    clear_screen()
    
    final_word = game_state[keys['word']]
    final_mistakes = game_state[keys['mistakes']]
    final_guessed = game_state[keys['guessed']]
    
    print("\n" + "="*50)
    print(" ИГРА ОКОНЧЕНА ".center(50, "="))
    print("="*50)
    print(get_game_state(final_mistakes))
    print("\n🎯 Загаданное слово:", final_word.upper())
    
    if result == "win":
        print("\n🎉 ПОЗДРАВЛЯЕМ! Вы угадали слово!")
        print("📊 Угадано за", len(final_guessed), "букв и", final_mistakes, "ошибок")
    else:
        print("\n😔 Вы проиграли. Попробуйте ещё раз!")
    
    print("="*50)


def run_game_loop(game_state, keys):
    game_over = False
    result_status = ""
    
    while not game_over:
        clear_screen()
        
        display_game_info(game_state, keys)
        
        is_over, status = check_game_over(game_state)
        if is_over:
            game_over = True
            result_status = status
            break
        
        letter = get_user_input()
        
        if letter is None:
            break
        
        is_valid, message = is_valid_letter(letter, game_state[keys['guessed']])
        if not is_valid:
            print("\n⚠️  ", message)
            input("Нажмите Enter для продолжения...")
            continue
        
        success, msg = make_guess(game_state, letter)
        print("\n✓ ", msg)
        input("Нажмите Enter для продолжения...")
    
    show_game_result(game_state, result_status, keys)


def play_again():
    while True:
        choice = input("\n🔄 Сыграть ещё раз? (да/нет): ").lower()
        if choice in ['да', 'd', 'yes', 'y']:
            return True
        elif choice in ['нет', 'n', 'no']:
            return False
        else:
            print("Введите 'да' или 'нет'")


def main():
    print("\n" + "="*50)
    print(" ДОБРО ПОЖАЛОВАТЬ В ИГРУ 'ВИСЕЛИЦА' ".center(50, "="))
    print("="*50)
    print("\nПравила игры:")
    print("1. Вам нужно угадать загаданное слово")
    print("2. Вводите по одной букве")
    print("3. У вас есть", MAX_MISTAKES, "ошибок")
    print("4. Используйте подсказку, если затрудняетесь")
    print("="*50)
    input("\nНажмите Enter, чтобы начать...")
    
    while True:
        game_state = initialize_game()
        
        keys = {
            'word': 'word',
            'hint': 'hint',
            'guessed': 'guessed_letters',
            'mistakes': 'mistakes'
        }
        
        run_game_loop(game_state, keys)
        
        if not play_again():
            print("\nСпасибо за игру! До свидания! 👋\n")
            break


if __name__ == "__main__":
    main()