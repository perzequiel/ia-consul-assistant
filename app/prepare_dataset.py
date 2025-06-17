import os
import json
import re

CHAT_DIR = "chats_por_usuario"
OUTPUT_FILE = "finetune_phi_data.jsonl"

dialogs = []

for filename in os.listdir(CHAT_DIR):
    path = os.path.join(CHAT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    for i in range(len(lines) - 1):
        input_msg = lines[i]
        response_msg = lines[i + 1]
        if not response_msg.lower().startswith("hola") and len(response_msg) < 10:
            continue  # filtro básico

        dialogs.append({"input": input_msg, "output": response_msg})

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for d in dialogs:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")

print(f"✅ Dataset generado con {len(dialogs)} ejemplos en {OUTPUT_FILE}")
