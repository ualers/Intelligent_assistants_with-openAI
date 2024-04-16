from openai import OpenAI
import time
import os

key_api = 'you_key'
client = OpenAI(
    api_key=key_api,
)



file = client.files.create(
    file=open("doc_financeiro.txt", "rb"),
    purpose='assistants'
)
file2 = client.files.create(
    file=open("doc_financeiro_2.txt", "rb"),
    purpose='assistants'
)
assistant = client.beta.assistants.create(
    name="Assitente financeiro", 
    instructions="voce é o meu assitente financeiro  seu objetivo é relatar meus gastos e ganhos  com base no arquivo e tambem atualizar meus ganhos e gastos do arquivo quando eu solicitar, responda em portugues",
    tools=[{"type": "retrieval"}],
    model="gpt-3.5-turbo-1106",
    file_ids=[file.id, file2.id]
)
print([file.id, file2.id])
thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content='''quanto eu tenho em caixa?''',
    file_ids=[file.id, file2.id]
)
print(thread.id)
print(assistant.id)
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="voce é o meu assitente financeiro  seu objetivo é relatar meus gastos e ganhos  com base no arquivo e tambem atualizar meus ganhos e gastos do arquivo quando eu solicitar, responda em portugues",
    tools=[{"type": "retrieval"}],
    model="gpt-3.5-turbo-1106"
)

while True:
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    if run_status.status == 'completed': 
        break
    else:
        print("Aguardando a execução ser completada...")
    time.sleep(2)  
messages = client.beta.threads.messages.list(
    thread_id=thread.id
)
for message in messages:
    for mensagem_contexto in message.content:  
        valor_texto = mensagem_contexto.text.value
        print(valor_texto)
        thread_id = thread.id
        assistant_id = assistant.id
        run_id = run.id
        name = "Assistente"
        diretorio_script = os.path.dirname(os.path.abspath(__file__))
        nome_arquivo_gerenciador = os.path.join(diretorio_script, 'gerenciador_agente_1.txt')
        with open('gerenciador_agente_1.txt', 'a') as arquivo:
            arquivo.write(f'Nome: {name} \n')
            arquivo.write(f'thread_id:{thread_id}\n')
            arquivo.write(f'assistant_id:{assistant_id}\n')
            arquivo.write(f'------------------------\n')
    break







