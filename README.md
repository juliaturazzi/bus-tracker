# Bus Tracker (BT) 🚍✨

Bem-vindo ao **Bus Tracker (BT)**! Este projeto é um sistema super completo para rastrear linhas e pontos de ônibus em tempo real, enviar alertas via email e proporcionar uma experiência incrível para usuários cadastrados e visitantes. Aqui você encontra o código-fonte do _backend_ e _frontend_, além de todas as informações para rodar o projeto na sua máquina.

---

## 🚀 Funcionalidades Principais

- 💡 **Consulta de ônibus em tempo real** via API Data Rio
- 📑 **Registro de alertas personalizados**
- 📧 **Notificações automáticas por email** quando um ônibus está próximo
- 📊 **Visualização interativa de mapas**
- 🏢 **Gerenciamento de usuários** com autenticação segura
- 🌀 **Interface responsiva e tema escuro**

## 🏗️ Arquitetura do Sistema

O **Bus Tracker** segue um modelo monolítico com os seguintes componentes principais:

### 🔹 Backend (FastAPI)

- 🔎 **FastAPI** - Framework moderno para construção de APIs
- 🛠️ **Uvicorn** - Servidor de aplicação ASGI
- 🏢 **MySQL** - Banco de dados relacional
- 🐝 **Python-Jose** e **bcrypt** - Autenticação e segurança
- 📧 **smtplib e email-validator** - Envio de emails
- 🌍 **OpenRouteService** - Cálculo de distância e roteamento
- 📝 **Pandas** - Manipulação de dados
- 🔧 **Pytest** - Testes automatizados

### 🔹 Frontend (React)

- 🎨 **React + TypeScript** - Desenvolvimento da interface
- 🔮 **Redux Toolkit** - Gerenciamento de estado global
- 🌟 **TailwindCSS & Material-UI** - Estilização e componentes visuais
- 🌐 **OpenLayers.js** - Exibição de mapas interativos
- 📄 **Zod** - Validação de dados
- 🌀 **ShadCN** - Componentes acessíveis e reutilizáveis

### 🔹 Infraestrutura

- 🛠️ **Docker & Docker Compose** - Containerização da aplicação
- 🔍 **Caddy** - Gerenciamento de HTTPS
- 🏢 **Vultr** - Hospedagem em nuvem
- 📧 **Zoho Mail** - Emails transacionais
- 🌐 **Registro.br + Cloudflare** - Gerenciamento de domínio e DNS


## Configuração do Ambiente (.env) 🔧

Antes de rodar o projeto, crie um arquivo `.env` na raiz com as variáveis necessárias:

```dotenv
# Chave de acesso para a API do OpenRouteService
OPENROUTE_KEY=your_openrouteservice_api_key

# Salt para segurança de senhas (usado com bcrypt)
SECURITY_PASSWORD_SALT=your_security_password_salt

# Alias do email que enviará notificações
EMAIL_SENDER_ALIAS=your_email_sender_alias

# Senha do email remetente para envio de notificações
EMAIL_SENDER_PASSWORD=your_email_sender_password

# Chave secreta para criação de tokens (JWT, etc.)
SECRET_KEY=your_secret_key

# URL do website (ex.: https://bustracker.com.br/)
WEBSITE_URL=your_website_url
```


## 🛠️ Como Rodar o Projeto

### 1. Clone o Repositório

```sh
 git clone https://github.com/juliaturazzi/bus-tracker.git
 cd bus-tracker
```


### 2. Configuração do Backend

```sh
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```


### 3. Configuração do Frontend

```sh
cd frontend
npm install
npm run dev
```


### 4. Usando Docker (Alternativa)

```sh
docker-compose up --build
```
