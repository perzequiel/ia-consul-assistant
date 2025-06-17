import json

with open("dataset_entrenamiento.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("dataset_entrenamiento.jsonl", "w", encoding="utf-8") as out_f:
    for item in data:
        json.dump(item, out_f, ensure_ascii=False)
        out_f.write("\n")

print("✅ Dataset convertido a JSONL: dataset_entrenamiento.jsonl")