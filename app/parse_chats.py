# app/parse_chats_respuestas.py

import os
import re
import json

CHAT_ROOT_DIR = "chats"
OUTPUT_FILE = "dataset_entrenamiento.json"

pattern = re.compile(r"^(\d{1,2}/\d{1,2}/\d{2,4}) (\d{1,2}:\d{2}) - (.*?): (.*)$")
consultorio_nombre = "consultoriosmedicosvillar"
dataset = []

for user_dir in os.listdir(CHAT_ROOT_DIR):
    full_user_dir = os.path.join(CHAT_ROOT_DIR, user_dir)
    if os.path.isdir(full_user_dir):
        for file in os.listdir(full_user_dir):
            if file.endswith(".txt"):
                path = os.path.join(full_user_dir, file)
                print(f"Procesando: {path}")
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                conversation = []
                for line in lines:
                    line = line.strip()
                    match = pattern.match(line)
                    if not match:
                        continue

                    date, time, sender, message = match.groups()
                    conversation.append((sender, message))

                # Agrupar como pares pregunta → respuesta
                i = 0
                while i < len(conversation):
                    sender, msg = conversation[i]
                    if sender != consultorio_nombre:
                        # juntar los mensajes del paciente hasta que hable el consultorio
                        input_msgs = [msg]
                        i += 1
                        while i < len(conversation) and conversation[i][0] != consultorio_nombre:
                            input_msgs.append(conversation[i][1])
                            i += 1
                        # ahora esperamos la respuesta del consultorio
                        if i < len(conversation) and conversation[i][0] == consultorio_nombre:
                            reply = conversation[i][1]
                            dataset.append({
                                "input": " ".join(input_msgs),
                                "output": reply
                            })
                            i += 1
                    else:
                        i += 1

# Guardar el dataset en JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

print(f"✅ Dataset generado con {len(dataset)} pares en {OUTPUT_FILE}")
