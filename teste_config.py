import json

def load_config(path='config.json'):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

config = load_config()

print("🔑 Chave da API:", config['openai_api_key'][:10] + "...(ocultado)")
print("📄 Arquivo da persona:", config['persona_file'])
