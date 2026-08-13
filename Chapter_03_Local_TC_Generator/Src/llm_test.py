from config_store import load_config
from llm_client import OllamaClient, GroqClient
config = load_config()
print('OLLAMA_URL', config.get('ollama_url'))
print('OLLAMA_MODEL', config.get('ollama_model'))
print('GROQ_KEY_PRESENT', bool(config.get('groq_api_key')))

ollama = OllamaClient(config.get('ollama_url'), config.get('ollama_model'))
groq = GroqClient(config.get('groq_api_key'))
prompt = 'Test connection from app.'
try:
    print('OLLAMA RESULT START')
    out = ollama.generate(prompt)
    print('OLLAMA SUCCESS:', out[:400])
except Exception as e:
    print('OLLAMA ERROR:', e)

try:
    print('GROQ RESULT START')
    out = groq.generate(prompt)
    print('GROQ SUCCESS:', out[:400])
except Exception as e:
    print('GROQ ERROR:', e)
