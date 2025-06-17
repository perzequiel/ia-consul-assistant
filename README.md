```bash
ollama run phi3
```

despues matalo con contrl+d

correr app/parse_chats.py 
```bash
python app/parse_chats.py 
```
(con los chats en la carpeta chats y unzipeados) te crea el dataset_entrenamiento.json

```bash
python convert.py 
```

te creae el dataset_entrenamiento.jsonl


despues para generar el Modelfile

```bash
python create_model_file.py 
```

ojo que te pisa el system (el prompt inicial)

con esto te crea el asistente
```bash
ollama create mi-asistente-medico -f Modelfile 
```

para ejecutarlo

```
ollama run mi-asistente-medico
```