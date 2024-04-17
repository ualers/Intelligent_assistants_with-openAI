
import time
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, Filters
from openai import OpenAI
from telegram import Bot
from pathlib import Path
import os
import threading

key_api = 'key'
TOKEN = "token_bot_father"
chat_id = 'chat_id'

client = OpenAI(
    api_key=key_api,
)
bot = Bot(token='token_bot_father')

emojis = ['😊', '🤖', '🚀', '💡', '🎉']
def enviar_resposta_com_emoji(resposta):
    emoji = random.choice(emojis)  
    resposta_com_emoji = f"{emoji} {resposta}"  
    return resposta_com_emoji


def enviar_audio(openai_response):

    list_voz = [
        'onyx',
        'echo',
        'fable',
        'nova',
        'shimmer',
        'alloy'
    ]
    voz_escolhido = random.choice(list_voz)
    #teste = random.uniform(1.05, 1.1)
    speech_file_path = Path(__file__).parent / f"info por {voz_escolhido}.mp3"
    response = client.audio.speech.create(
    model="tts-1-hd",
    #speed=teste,
    voice=voz_escolhido,
    input=f'olá eu sou {voz_escolhido}, {openai_response}'
    )
    
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(diretorio_script, f"info por {voz_escolhido}.mp3")

    response.stream_to_file(speech_file_path)
    bot.send_audio(chat_id=chat_id, audio=open(audio_path, 'rb'))
    return True

def start(update, context):
    update.message.reply_text('Olá ')

def reply_message(update, context):
    user_message = update.message.text
    asst = ''
    threead_id = ''
    file_idx = ['here_file_id1', 'here_file_id2']
    ferramentas = [{"type": "retrieval"}]
    modelo_de_IA = "gpt-3.5-turbo-1106"

    openai_response = mensagem_com_assistente_existente(user_message, threead_id, asst, file_idx, ferramentas, modelo_de_IA)
    random_action_mensagem_ou_audio = random.random()
    if random_action_mensagem_ou_audio > 0.3:
        
        update.message.reply_text(openai_response)
    else:
        if user_message.startswith("quero saber o  conteudo do arquivo") or user_message.endswith('conteudo do arquivo'):
            print('conteudo do arquivo')
            update.message.reply_text(openai_response)
        else:
            audio_flag = enviar_audio(openai_response)
            if audio_flag == True:
                print("audio enviado")
    #openai_response_com_emog = enviar_resposta_com_emoji(openai_response)
    

def mensagem_com_assistente_existente(mensagem, threead_id, asst, file_idx, ferramentas, modelo_de_IA):

    message = client.beta.threads.messages.create(
        thread_id=threead_id,
        role="user",
        content=mensagem,
        file_ids=file_idx
    )
    
    run = client.beta.threads.runs.create(
        thread_id=threead_id,
        assistant_id=asst,
        tools=ferramentas,
        model=modelo_de_IA,
        instructions="voce é o meu assitente financeiro  seu objetivo é relatar meus gastos e ganhos  com base no arquivo e tambem atualizar meus ganhos e gastos do arquivo quando eu solicitar, responda em portugues"
        
    )
    while True:
        time.sleep(2)  
        run_status = client.beta.threads.runs.retrieve(
            thread_id=threead_id,
            run_id=run.id
        )
        if run_status.status == 'completed': 
            break
        elif run_status.status == 'failed': 
            return "ocorreu um erro no servidor aguarde 20 segundos e pergunte novamente"
        elif run_status.status == 'in_progress': 
            print("in_progress")
        else:
            print("Aguardando a execução ser completada...")
        
    messages = client.beta.threads.messages.list(
        thread_id=threead_id
    )
    for message in messages:
        for mensagem_contexto in message.content:
            valor_texto = mensagem_contexto.text.value
            
            return valor_texto
            
        break

def main():
        
    while True:
        updater = Updater(TOKEN, use_context=True)
        
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_message))
        
        updater.start_polling(poll_interval=2, timeout=15)
        updater.idle()

        time.sleep(3600)
main()