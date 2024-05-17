from config import *
import telebot
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ForceReply
# inicio Bot
# La Variable de Telegram Token hace referencia al Token que ubica nuestro BOT en las BD de Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)
# Variable global
usuarios = {}


# /start
@bot.message_handler(commands=['start', 'ayuda', 'help'])
def cmd_start(message):
    # Comandos disponibles
    bot.send_message(
        message.chat.id, " Este Bot se encuentra en estado de Desarrollo.\nPuede presentar fallas en su Funcionamiento. Aun no es recomendable su uso.")
    bot.send_message(message.chat.id, "Hola, soy Karen tu Asistente Virtual.\n Para proceder a ayudarte, Porfavor dime ¿Quien eres?. \n A continuación responde una serie de preguntas para poder ayudarte mejor...")
    bot.send_message(message.chat.id, "Selecciona una de las Opciones")
    bot.send_message(
        message.chat.id, "Usa este comando para poder ayudarte \n /iniciemos")
    bot.send_message(
        message.chat.id, "Esta Opción para comenzar una Nueva conversación /iniciemos \n Esta Opción, para pasar al error directamente /select_error ")


@bot.message_handler(commands=['iniciemos'])
def cmd_init(message):
    # Comando Nombre
    markup = ForceReply()
    msg = bot.send_message(
        message.chat.id, "¿Como te llamas? \n Digita Tu Nombre completo", reply_markup=markup)
    bot.register_next_step_handler(msg, cmd_select_pais)


def cmd_select_pais(message):
    # Comando Pais
    markup = ReplyKeyboardMarkup(
        one_time_keyboard=True,
        input_field_placeholder="Escoja su pais de residencia...",
        resize_keyboard=True
    )
    markup.add("Colombia", "Venezuela", "Ecuador", "Peru", "Argentina")
    msg = bot.send_message(
        message.chat.id, 'Seleccione su pais de residencia', reply_markup=markup)
    bot.register_next_step_handler(msg, cmd_select_departamento)

def cmd_select_departamento(message):
    if message.text == "Colombia":
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True,
            # Crear una varable q muestre la lista de Departamentos, dependiendo de la seleccion de Pais
            input_field_placeholder="Escoja su Departamento de residencia...", resize_keyboard=True
        )
        markup.add("Amazonas", "Antioquia", "Arauca", "Atlantico", "Bolivar", "Boyacá", "Caldas", "Caquetá", "Casanare", "Cauca", "Cesar", "Chocó", "Córdoba", "Cundinamarca", "Guainia", "Guaviare", "Huila", "La Guajira", "Magdalena", "Meta", "Nariño", "Norte de santander", "Putumayo", "Quindío", "Risaralda", "San andres y Providencia", " Santander", "Sucre", "Tolima", "Valle del Cauca", "Vaupés", "Vichada")
        msg = bot.send_message(
            message.chat.id, 'Seleccione su Departamento de residencia', reply_markup=markup)

    elif message.text == "Venezuela":
        msg = bot.send_message(message.chat.id, "Actualmente No podemos Brindar Soporte en tu Pais de Residencia \n Esto puede Deberse a que no contamos con ningun registro en tu Pais")
    elif message.text == "Ecuador":
        msg = bot.send_message(message.chat.id, "Actualmente No podemos Brindar Soporte en tu Pais de Residencia \n Esto puede Deberse a que no contamos con ningun registro en tu Pais")
    elif message.text == "Peru":
        msg = bot.send_message(message.chat.id, "Actualmente No podemos Brindar Soporte en tu Pais de Residencia \n Esto puede Deberse a que no contamos con ningun registro en tu Pais")
    elif message.text == "Argentina":
        msg = bot.send_message(message.chat.id, "Actualmente No podemos Brindar Soporte en tu Pais de Residencia \n Esto puede Deberse a que no contamos con ningun registro en tu Pais")

    bot.register_next_step_handler(msg, cmd_select_institucion)

def cmd_select_institucion(message):
    # Comando Instituciòn Educativa
    markup = ReplyKeyboardMarkup(
        one_time_keyboard=True,
        input_field_placeholder="Escoja su institución educativa...",
        resize_keyboard=True
    )
    # Crear una varable q muestre la lista de escuelas, dependiendo de la seleccion del departamento
    markup.add("")
    msg = bot.send_message(
        message.chat.id, 'Seleccione su Institución Educativa', reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_edad)


def preguntar_edad(message):
    # edad usuario
    usuarios[message.chat.id] = {}
    usuarios[message.chat.id]["nombre"] = message.text
    markup = ForceReply()
    msg = bot.send_message(
        message.chat.id, "Ingrese su Edad.", reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_sexo)


def preguntar_sexo(message):
    if not message.text.isdigit():
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id, 'Error: Indique en Numeros enteros su edad Correspondiente')
        bot.register_next_step_handler(msg, preguntar_sexo)
    else:
        usuarios[message.chat.id]["edad"] = message.text
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True,
            input_field_placeholder="Escoja su Sexo",
            resize_keyboard=True
        )
        markup.add("Masculino", "Femenino", "Otro", "Prefiero No decirlo")
        msg = bot.send_message(
            message.chat.id, '¿Cual es tu sexo?', reply_markup=markup)
        bot.register_next_step_handler(msg, select_error)


@bot.message_handler(commands=['select_error'])
def cmd_init(message):
    markup = ReplyKeyboardMarkup(
        one_time_keyboard=True,
        input_field_placeholder="Selecciona uno de los siguientes...",
        resize_keyboard=True
    )
    markup.add("error_707", "error_801", "error_808", "error_907", "error_908",
               "errorr_909", "error_107", "error_089", "error_404", "error_500")
    msg = bot.send_message(
        message.chat.id, 'A continuación Selecciona el codigo de error que se muestra en pantalla')
    bot.send_message(
        message.chat.id, 'Este Codigo se muestra en color rojo, el la parte superior derecha de la pantalla. \n Seleccione el Codigo que Presenta', reply_markup=markup)
    bot.register_next_step_handler(msg, commands_error)


def select_error(message):
    if message.text != "Masculino" and message.text != "Femenino" and message.text != "Otro" and message.text != "Prefiero No decirlo":
        msg = bot.send_message(
            message.chat_id, 'ERROR: Sexo no valido.\n Seleccione una Opción')
        bot.register_next_step_handler(msg, preguntar_sexo)
    else:
        usuarios[message.chat.id]["select_error"] = message.text
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True,
            input_field_placeholder="Selecciona uno de los siguientes...",
            resize_keyboard=True
        )
        markup.add("error_707", "error_801", "error_808", "error_907", "error_908",
                   "errorr_909", "error_107", "error_089", "error_404", "error_500")
        msg = bot.send_message(
            message.chat.id, 'A continuación Selecciona el codigo de error que se muestra en pantalla')
        bot.send_message(
            message.chat.id, 'Este Codigo se muestra en color rojo, el la parte superior derecha de la pantalla. \n Seleccione el Codigo que Presenta', reply_markup=markup)
        bot.register_next_step_handler(msg, commands_error)
# El paso anterior Muestra en Pantalla Los Botones de Errores
# Dependiendo del Id del Boton Muestra la Respuesta Correspondiente


# MAIN ####################
if __name__ == '__main__':
    print("Iniciando Bot de soporte...")
    bot.infinity_polling()