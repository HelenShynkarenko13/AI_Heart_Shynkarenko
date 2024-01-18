from simpful import *
import telebot
bot = telebot.TeleBot("6985814036:AAGzLG8A89R1FPhXIRM33MOyg9tsiTLgq1E")

# Create a Mamdani-type fuzzy system
FS = FuzzySystem()
x1_L = FuzzySet(function=Trapezoidal_MF(0, 0, 10.8879492600423, 25), term="L")
x1_LA = FuzzySet(function=Trapezoidal_MF(2.5, 25, 34, 44), term="LA")
x1_A = FuzzySet(function=Trapezoidal_MF(25, 44, 50, 60), term="A")
x1_HA = FuzzySet(function=Trapezoidal_MF(55, 60, 70, 75), term="HA")
x1_H = FuzzySet(function=Trapezoidal_MF(67, 75, 100, 120), term="H")
FS.add_linguistic_variable("x1", LinguisticVariable([x1_L,x1_LA, x1_A, x1_HA, x1_H],
                                                                  universe_of_discourse=[0, 100]), verbose=True)

x2_L = FuzzySet(function=Trapezoidal_MF(1.3, 13, 14.7410147991543, 18.5), term="L")
x2_A = FuzzySet(function=Trapezoidal_MF(15.9397463002114, 18.5, 19.1, 23.3), term="A")
x2_HA = FuzzySet(function=Trapezoidal_MF(22.3, 25, 27, 30), term="HA")
x2_H = FuzzySet(function=Trapezoidal_MF(28.7262156448203, 30, 40.9, 48.1), term="H")
FS.add_linguistic_variable("x2",
                           LinguisticVariable([x2_L, x2_A, x2_HA, x2_H], universe_of_discourse=[13, 40]), verbose=True)

x3_L = FuzzySet(function=Trapezoidal_MF(-3.6, 0, 0.2, 2), term="L")
x3_A = FuzzySet(function=Trapezoidal_MF(1.3953488372093, 2, 2.2, 4), term="A")
x3_H= FuzzySet(function=Trapezoidal_MF(3.38, 4.02, 5.91120507399577, 8.02), term="H")
FS.add_linguistic_variable("x3", LinguisticVariable(
    [x3_L, x3_A, x3_H], universe_of_discourse=[0, 8]),
                           verbose=True)

# Створення вихідного терму
y_L = FuzzySet(function=Trapezoidal_MF(0, 0, 8.98520084566595, 25), term="L")
y_A = FuzzySet(function=Trapezoidal_MF(2.5, 25, 32.0295983086681, 50), term="A")
y_HA = FuzzySet(function=Trapezoidal_MF(35, 50, 55.9196617336152, 70), term="HA")
y_H = FuzzySet(function=Trapezoidal_MF(61, 70, 79.5983086680761, 100), term="H")
FS.add_linguistic_variable("y", LinguisticVariable(
    [y_L, y_A, y_HA, y_H], universe_of_discourse=[0, 100]),
                           verbose=True)
# Add rules
FS.add_rules_from_file(path='rules.txt')

@bot.message_handler(commands=['help', 'start'])
def info_msg(message):
    bot.send_message(message.chat.id, "Вітаю!\n"
                                      "Цей бот призначений для надання оцінки ризику виникнення серцевого нападу. "
                                      "Щоб почати анкетування натисність команду /run.\n"
                                      "Пройдіть невеличке анкетування і отримайте результат")


@bot.message_handler(commands=['run'])
def run_quiz(message):
    bot.send_message(message.from_user.id, "Анкетування розпочато\n"
                                           "Щоб припинити анкетування натисність /exit\n\n"
                                           "Який Ваш вік?")
    bot.register_next_step_handler(message, get_x1)
def get_x1(message):
    if message.text.lower() == '/exit':
        bot.send_message(message.chat.id, "Анкетування припинено")
        return
    global x1
    try:
        x1 = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Некоректне значення!\n"
                                          "Має бути цифра", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_x1)
        return
    if x1 < 0 or x1 > 100:
        bot.send_message(message.chat.id, "Некоректне значення!\n"
                                          "Вік може бути від 0 до 100", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_x1)
        return
    bot.send_message(message.chat.id, "Який у Вас індекс маси тіла? (кг/м2)")
    bot.register_next_step_handler(message, get_x2)
def get_x2(message):
    if message.text.lower() == '/exit':
        bot.send_message(message.chat.id, "Анкетування припинено")
        return
    global x2
    try:
        x2 = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Некоректне значення!\n"
                                          "Має бути цифра", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_x2)
        return
    if x2 < 13 or x2 > 40:
        bot.send_message(message.chat.id, "️Некоректне значення!\n"
                                          "Індекс маси тіла має бути від 13 до 48", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_x2)
        return
    bot.send_message(message.chat.id, "Кількість хронічних хвороб?",  parse_mode='Markdown')
    bot.register_next_step_handler(message, get_x3)

def get_x3(message):
    if message.text.lower() == '/exit':
        bot.send_message(message.chat.id, "Анкетування припинено")
        return
    global x3
    try:
        x3 = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Некоректне значення!\n"
                                          "Має бути цифра", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_x3)
        return
    if x3 < 0 or x3 > 8:
        bot.send_message(message.chat.id,"Введіть, будь ласка, значення між 0 та 8", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_x3)
        return
    give_y(message)

def give_y(message):
    bot.send_message(message.chat.id, "_" + message.chat.first_name + ", Ваші дані_\nВаш вік: " + str(x1) + "\nІндекс маси тіла: " + str(x2) + " кг/м2\nКількість хронічних хвороб: " + str(x3), parse_mode='Markdown')

    variables = ["x1", "x2", "x3"]
    values = [x1, x2, x3]
    for variable, value in zip(variables, values):
        FS.set_variable(variable, value)
    mamdani = FS.Mamdani_inference()
    bot.send_message(message.chat.id, "Оцінка:\n" + get_y(mamdani.get("y")), parse_mode='Markdown')
    bot.send_message(message.chat.id, "Дякуємо за Вашу увагу!\nЩоб отримати нову оцінку введіть /run")


def get_y(coef):
    if 0 <= coef < 25:
        return "Ймовірність виникнення серцевого нападу достатньо низька - від 0% до 25%"
    elif 25 <= coef < 50:
        return "Ймовірність виникнення серцевого нападу середня - від 25% до 50%."
    elif 50 <= coef <= 70:
        return "Ймовірність виникнення серцевого нападу вище середнього - від 50% до 70%. Зверніться до лікаря."
    elif 70 <= coef <= 100:
        return "Ймовірність виникнення серцевого нападу висока - від 70% до 100%. Терміново зверніться до лікаря."


@bot.message_handler(commands=['exit'])
@bot.message_handler(func = lambda msg: msg.text is not None and '/' not in msg.text)
def query_handler(message):
    bot.send_message(message.chat.id, "Анкетування завершено")
    info_msg(message)


bot.infinity_polling()
