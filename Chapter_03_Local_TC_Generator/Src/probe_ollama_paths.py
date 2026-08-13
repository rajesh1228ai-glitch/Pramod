import requests
from urllib.parse import quote
from config_store import load_config
config = load_config()
print('OLLAMA_ROOT', config.get('ollama_url'))
model = config.get('ollama_model','gemma3:1b')
encoded = quote(model, safe='')
paths = [
    '/', '/version', '/v1/version', '/status', '/health', '/v1/health', '/v1/status',
    '/v1', '/v1/models', f'/v1/models/{model}', f'/v1/models/{encoded}',
    f'/v1/models/{model}/', f'/v1/models/{encoded}/',
    f'/v1/models/{model}/generate', f'/v1/models/{encoded}/generate',
    f'/v1/models/{model}/complete', f'/v1/models/{encoded}/complete',
    f'/v1/models/{model}/outputs', f'/v1/models/{encoded}/outputs',
    f'/v1/models/{model}/responses', f'/v1/models/{encoded}/responses',
    f'/v1/models/{model}/predict', f'/v1/models/{encoded}/predict',
    f'/v1/models/{model}/chat/completions', f'/v1/models/{encoded}/chat/completions',
    '/v1/generate', '/v1/complete', '/v1/completions', '/v1/chat/completions', '/v1/responses', '/v1/outputs', '/v1/predict',
    '/openapi.json', '/v1/openapi.json', '/v1/swagger.json', '/docs', '/swagger',
]
root = config.get('ollama_url').rstrip('/')
for p in paths:
    url = root + p
    try:
        method = 'GET' if p in ['/', '/version', '/v1/version', '/status', '/health', '/v1/health', '/v1/status', '/v1', '/v1/models', f'/v1/models/{model}', f'/v1/models/{encoded}', f'/v1/models/{model}/', f'/v1/models/{encoded}/', '/openapi.json', '/v1/openapi.json', '/v1/swagger.json', '/docs', '/swagger'] else 'POST'
        print('---', method, url)
        if method == 'GET':
            r = requests.get(url, timeout=10)
        else:
            r = requests.post(url, json={'model': model, 'prompt': 'Test', 'max_tokens': 3, 'temperature': 0.2}, timeout=10)
        print(r.status_code)
        print(r.text[:400].replace('\n',' '))
    except Exception as e:
        print('ERROR', url, e)
