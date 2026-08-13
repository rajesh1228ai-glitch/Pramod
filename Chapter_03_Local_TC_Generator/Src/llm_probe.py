import requests
from urllib.parse import quote
from config_store import load_config
config = load_config()
model = config.get('ollama_model', 'gemma3:1b')
encoded = quote(model, safe='')
root = config.get('ollama_url').rstrip('/')
print('Ollama root', root)
paths = [
    '/',
    '/v1',
    '/v1/models',
    f'/v1/models/{encoded}',
    '/v1/generate',
    f'/v1/models/{encoded}/generate',
    f'/v1/models/{encoded}/complete',
    f'/v1/models/{encoded}/completions',
    f'/v1/models/{encoded}/chat/completions',
    f'/v1/models/{encoded}/outputs',
    '/v1/models/list',
    '/v1/models/'+encoded+'/output',
    '/v1/models/'+encoded+'/predict',
    '/openapi.json',
    '/v1/openapi.json',
    '/v1/swagger.json',
]
for p in paths:
    url = root + p
    try:
        if p in ['/', '/v1', '/v1/models', f'/v1/models/{encoded}', '/openapi.json', '/v1/openapi.json', '/v1/swagger.json']:
            r = requests.get(url, timeout=10)
        else:
            r = requests.post(url, json={'model': model, 'prompt': 'Test', 'max_tokens': 10, 'temperature': 0.2}, timeout=10)
        print('OL', p, r.status_code, r.text[:300].replace('\n',' '))
    except Exception as e:
        print('OL', p, 'ERROR', e)

print('\nGROQ PROBE')
keys = ['https://api.groq.com', 'https://api.groq.ai']
paths = [
    '/v1', '/v1/models', '/v1/chat/completions', '/v1/completions', '/v1/responses',
    '/v1/models/groq-1/outputs', '/v1/models/groq-1/generate', '/v1/models/groq-1/complete',
    '/v1/models/groq-1/completions', '/v1/models/groq-1/chat/completions',
    '/v1/models/groq-1/predict', '/v1/models/groq-1', '/v1/responses', '/v1/generate',
]
for base in keys:
    for p in paths:
        url = base + p
        try:
            r = requests.post(url, headers={'Authorization': f"Bearer {config.get('groq_api_key')}", 'Content-Type': 'application/json'}, json={'model':'groq-1','messages':[{'role':'user','content':'Test'}],'max_tokens':10,'temperature':0.2}, timeout=10)
            print('GR', base, p, r.status_code, r.text[:200].replace('\n',' '))
        except Exception as e:
            print('GR', base, p, 'ERROR', e)
