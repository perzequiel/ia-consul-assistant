import json

input_file = "dataset_entrenamiento.jsonl"
output_file = "Modelfile"

header = '''FROM phi3-mini

SYSTEM """
Eres un asistente médico de recepción. Respondés con precisión, claridad y amabilidad a consultas sobre turnos, especialidades médicas y precios. No inventes datos que no estén en el contexto del consultorio.
"""

'''

def escape_triple_quotes(text):
    return text.replace('"""', '\\"\\"\\"')

with open(input_file, "r", encoding="utf-8") as fin, open(output_file, "w", encoding="utf-8") as fout:
    fout.write(header)
    for line in fin:
        if not line.strip():
            continue
        entry = json.loads(line)
        user_msg = escape_triple_quotes(entry.get("input", "").strip())
        assistant_msg = escape_triple_quotes(entry.get("output", "").strip())
        if user_msg and assistant_msg:
            fout.write(f'MESSAGE user """\n{user_msg}\n"""\n\n')
            fout.write(f'MESSAGE assistant """\n{assistant_msg}\n"""\n\n')

print(f"Archivo '{output_file}' creado correctamente.")
