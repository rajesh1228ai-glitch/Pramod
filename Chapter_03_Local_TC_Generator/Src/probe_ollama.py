import requests
base='http://localhost:11434'
paths=['/','/v1','/v1/models','/v1/models/gemma3:1b','/v1/completions','/v1/chat/completions','/v1/responses']
for p in paths:
    url = base + p
    try:
        r = requests.get(url, timeout=10)
        print('GET', url, 'status', r.status_code, 'ct', r.headers.get('content-type'))
        print(r.text[:800])
    except Exception as e:
        print('GET', url, 'ERR', repr(e))
    print('-'*80)
