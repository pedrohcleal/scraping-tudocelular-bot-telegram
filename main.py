from playwright.sync_api._generated import Page
from playwright.sync_api import sync_playwright
import requests
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()


TOKEN = os.getenv("TOKEN_TELEGRAM")
if TOKEN is None:
    raise ValueError("TOKEN_TELEGRAM não encontrada nas variáveis de ambiente")

# Substitua pelo seu chat ID do Telegram, caso não saiba, utilize a função check_chat_id() abaixo para descobrir
CHAT_ID = "5442998287"

def get_chat_id():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    r = requests.get(url)
    r.raise_for_status()
    json_response = r.json()
    chat_id = json_response['result'][-1]['message']['chat']['id']
    username_ = json_response['result'][-1]['message']['chat']['username']
    print(f"Chat ID última mensagem: '{chat_id}', Username: '{username_}'")
    

def send_text_message(msg, chat_id=CHAT_ID):
    sleep(1.1)
    TOKEN = "8207948976:AAEh9JeCx5yORuzFBa3eFcs3cSP3mjFbhA8"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    params = {
        "chat_id": chat_id,
        "text": msg,
    }

    r = requests.get(url, params=params)
    r.raise_for_status()

# https://www.tudocelular.com/Samsung/fichas-tecnicas/n9846/Samsung-Galaxy-S25-Plus.html 
#                                                       ↳ model_id = 9846
model_ids = {
    "s25_edge": 9847,
    "s25_base": 9845,
    "s25_plus": 9846,
    "s25_ultra": 9755,
    "s24_ultra": 9107
}
base_url = 'https://www.tudocelular.com/new_files/ajax/pricelist.php?modelid='


def busca_precos_min(page: Page, model_key: str, precos_lista: list[dict]):
    preco_min = 999999
    page.goto(base_url + str(model_ids[model_key]), wait_until="domcontentloaded")
    blocos = page.locator('#table1 > *')
    for i in range(blocos.count()):
        bloco = blocos.nth(i)
        preco_str = bloco.get_by_role("link", name="R$").inner_text()
        
        try:
            preco = float(preco_str.replace("R$", "").replace(".", "").replace(",", ".").strip())
        except ValueError:
            send_text_message("Erro: Preço não encontrado no bloco de preço - Script parado")
            raise ValueError("Preço não encontrado no bloco de preço")
        
        if preco < preco_min:
            link = bloco.locator(".img").get_attribute("href")
            if link is None:
                send_text_message("Erro: Link não encontrado no bloco de preço - Script parado")
                raise ValueError("Link não encontrado no bloco de preço")
            preco_min = preco
    
    base_url_link = 'https://www.tudocelular.com'
    if preco_min not in [x['preco'] for x in precos_lista]:
        print(f"Novo menor preço encontrado: R$ {preco_min:.2f}")
        txt_msg = f"Novo menor preço para o modelo {model_key.replace('_', ' ').title()}: R$ {preco_min:.2f}\nLink: {base_url_link + link}"
        send_text_message(f"Novo menor preço para o modelo {txt_msg}")
    else:
        print(f"Menor preço atual permanece: R$ {preco_min:.2f}")

    return {'preco': preco_min,'link': link}
        

if __name__ == "__main__":
    precos_s25_ultra: list[dict] = []
    precos_s25_plus: list[dict] = []
    precos_s25_base: list[dict] = []
    precos_s25_edge: list[dict] = []
    precos_s24_ultra: list[dict] = []
    
    send_text_message("Bot de monitoramento de preços iniciado.")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page: Page = browser.new_page()
            while True: 
                sleep(5)
                modelos_cel = ['s25_ultra', 's25_plus', 's25_base', 's25_edge', 's24_ultra']
                for model_key in modelos_cel:
                    if model_key == 's25_ultra':
                        precos_s25_ultra.append(busca_precos_min(page, model_key, precos_s25_ultra))
                    elif model_key == 's25_plus':
                        precos_s25_plus.append(busca_precos_min(page, model_key, precos_s25_plus))
                    elif model_key == 's25_base':
                        precos_s25_base.append(busca_precos_min(page, model_key, precos_s25_base))
                    elif model_key == 's25_edge':
                        precos_s25_edge.append(busca_precos_min(page, model_key, precos_s25_edge))
                    elif model_key == 's24_ultra':
                        precos_s24_ultra.append(busca_precos_min(page, model_key, precos_s24_ultra))
    except:
        send_text_message('ocorreu algum erro no bot.')