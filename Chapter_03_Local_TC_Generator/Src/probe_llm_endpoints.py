import requests
from config_store import load_config
config = load_config()
print('OLLAMA_URL', config.get('ollama_url'))
print('OLLAMA_MODEL', config.get('ollama_model'))
print('GROQ_KEY_PRESENT', bool(config.get('groq_api_key')))
base = config.get('ollama_url').rstrip('/')
paths = [
    ('GET', '/'),
    ('GET', '/v1'),
    ('GET', '/v1/models'),
    ('POST', '/v1/generate'),
    ('POST', f"/v1/models/{config.get('ollama_model')}/generate"),
    ('POST', f"/v1/models/{config.get('ollama_model')}/complete"),
    ('POST', f"/v1/models/{config.get('ollama_model')}/chat/completions"),
]
for method, path in paths:
    url = base + path
    try:
        if method == 'GET':
            r = requests.get(url, timeout=10)
        else:
            r = requests.post(url, json={'model': config.get('ollama_model'), 'prompt': 'Test', 'max_tokens': 10, 'temperature': 0.2}, timeout=10)
        print('OLLAMA', method, url, '=>', r.status_code, r.text[:300].replace('\n',' '))
    except Exception as e:
        print('OLLAMA', method, url, 'ERROR', e)

print('--- GROQ ---')
base = 'https://api.groq.com/v1'
paths = [
    '/chat/completions',
    '/completions',
    '/responses',
    '/models/groq-1/outputs',
    '/models/groq-1/generate',
]
headers = {'Authorization': f"Bearer {config.get('groq_api_key')}", 'Content-Type': 'application/json'}
payload = {'model': 'groq-1', 'messages': [{'role': 'user', 'content': 'Test'}], 'max_tokens': 10, 'temperature': 0.2}
for path in paths:
    url = base + path
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        print('GROQ POST', url, '=>', r.status_code, r.text[:300].replace('\n',' '))
    except Exception as e:
        print('GROQ POST', url, 'ERROR', e)
