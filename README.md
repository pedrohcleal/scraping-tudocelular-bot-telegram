# 📘 **Documentação – Monitoramento Automático de Preços (Galaxy S24/S25)**

Este projeto realiza scraping contínuo do site **TudoCelular**, monitorando os menores preços de vários modelos da linha Samsung Galaxy S24 e S25 e enviando alertas via **Telegram** sempre que um novo menor preço é encontrado.

---

# 🚀 **Funcionalidades**

* ✅ Monitoramento automático dos modelos:

  * Galaxy S25 Ultra
  * Galaxy S25 Plus
  * Galaxy S25 Base
  * Galaxy S25 Edge
  * Galaxy S24 Ultra
* ✅ Scraping utilizando **Playwright**
* ✅ Envio de mensagens direto para o seu Telegram
* ✅ Alerta quando encontra novo menor preço
* ✅ Tratamento básico de erros (sem link / sem preço)
* ✅ Variáveis de ambiente com dotenv

---

# 📁 **Estrutura sugerida do projeto**

```
scraper-precos/
├── main.py
├── .env
├── requirements.txt
└── README.md
```

---

# 🧩 **Dependências**

Este projeto utiliza:

* Python 3.10+
* Playwright
* Requests
* Dotenv

Instale o Playwright após instalar as libs:

```bash
playwright install
```

---

# ⚙️ **Configuração do ambiente**

Você pode configurar com **venv** ou **uv**.

---

## ✅ **Usando venv (ambiente virtual nativo do Python)**

### Criar o ambiente:

```bash
python -m venv venv
```

### Ativar:

Windows:

```bash
venv\Scripts\activate.bat
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Instalar dependências:

```bash
pip install -r requirements.txt
playwright install
```

---

### Instalar dependências:

```bash
uv pip install -r requirements.txt
playwright install chromium
```

---

# 🤖 **Configuração do Bot do Telegram (Tutorial Completo)**

## 1️⃣ Criar o bot no Telegram

1. Abra o Telegram
2. Pesquise: **@BotFather**
3. Envie:

   ```
   /start
   ```
4. Envie:

   ```
   /newbot
   ```
5. Escolha nome e username (deve terminar com `bot`)
6. O BotFather vai te entregar o TOKEN.

Guarde o token.

---

## 2️⃣ Ativar o bot

* Abra o link do bot enviado pelo BotFather
* Clique em **Start**

---

## 3️⃣ Criar arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

```
TOKEN_TELEGRAM=seu_token_que_recebeu_do_botfather
```

---

## 4️⃣ Descobrir seu `chat_id`

Rode esta função no Python:

```python
def get_chat_id():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    r = requests.get(url)
    r.raise_for_status()
    json_response = r.json()
    chat_id = json_response['result'][-1]['message']['chat']['id']
    username_ = json_response['result'][-1]['message']['chat']['username']
    print(f"Chat ID última mensagem: '{chat_id}', Username: '{username_}'")
```

⚠️ Antes disso, envie uma mensagem qualquer para o seu bot.

---

## 5️⃣ Inserir o chat_id no código

```python
CHAT_ID = "5442998287"
```

Substitua pelo seu.

---

# 🔍 **Como o scraping funciona**

A função principal é:

```python
busca_precos_min(page, model_key, precos_lista)
```

Ela faz:

1. Acessa a página de preços do modelo
2. Itera sobre todos os blocos da tabela
3. Extrai preço e link
4. Converte o texto em float
5. Identifica o menor preço
6. Compara com o último preço registrado
7. Se for menor → envia alerta Telegram

---

# 📤 **Envio de mensagens pelo Telegram**

A função:

```python
def send_text_message(msg, chat_id=CHAT_ID):
```

Responsável por mandar alertas com:

* preço
* link
* mensagem de erro (caso falhe scraping)

---

# 🏃 **Executando o projeto**

Com ambiente ativado:

```bash
python main.py
```

O bot enviará no chat ao iniciar:

```
Bot de monitoramento de preços iniciado.
```
