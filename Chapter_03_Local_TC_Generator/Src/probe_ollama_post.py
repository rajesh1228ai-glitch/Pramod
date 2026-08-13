import requests, json
base='http://localhost:11434'
endpoints = [
    '/v1/completions',
    '/v1/chat/completions',
    '/v1/responses',
    '/v1/models/gemma3:1b/complete',
    '/v1/models/gemma3:1b/outputs'
]
payloads = [
    {'model': 'gemma3:1b', 'prompt': 'Test connection from app.', 'max_tokens': 64, 'temperature': 0.2},
    {'model': 'gemma3:1b', 'messages': [{'role': 'user', 'content': 'Test connection from app.'}], 'max_tokens': 64, 'temperature': 0.2},
    {'model': 'gemma3:1b', 'input': 'Test connection from app.', 'max_tokens': 64, 'temperature': 0.2},
    {'input': 'Test connection from app.', 'max_tokens': 64, 'temperature': 0.2},
]
for endpoint in endpoints:
    url = base + endpoint
    print('===', endpoint)
    for payload in payloads:
        try:
            r = requests.post(url, json=payload, timeout=20)
            print('POST', url, 'payload keys', list(payload.keys()), 'status', r.status_code, 'ct', r.headers.get('content-type'))
            print('TEXT', r.text[:800])
        except Exception as e:
            print('ERR', repr(e))
        print('---')
