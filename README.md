# Guia: Integração WhatsApp com Twilio

## 📱 O que vai funcionar?

Quando um cliente agendar um corte, ele receberá uma mensagem no WhatsApp confirmando:
- Data e hora do agendamento
- Nome do barbeiro
- Tipo de serviço

---

## 🚀 Passo a Passo de Configuração

### 1️⃣ Crie uma Conta Twilio Gratuita

1. Acesse: **https://www.twilio.com/try-twilio**
2. Preencha o formulário:
   - Email
   - Senha
   - Nome completo
   - Código do país (Brasil)
3. Confirme o email
4. Responda as perguntas sobre seu uso

### 2️⃣ Ative o WhatsApp Sandbox

Na dashboard Twilio:

1. Clique em **Products** (menu esquerdo)
2. Procure por **Programmable Messaging**
3. Clique em **Settings → WhatsApp Sandbox**
4. Você verá algo como:
   ```
   Join this WhatsApp chat:
   https://wa.me/14155238886?text=join%20furry-lamp
   ```

5. Abra este link no seu celular (com WhatsApp instalado)
6. Envie a mensagem sugerida
7. Você receberá uma confirmação

### 3️⃣ Obtenha suas Credenciais

Na dashboard Twilio:

1. Clique em **Account** (canto superior direito)
2. Copie:
   - **Account SID**
   - **Auth Token**
3. Clique em **Programmable Messaging → Settings → General**
4. Copie o **WhatsApp Sandbox Number** (começa com `whatsapp:+`)

### 4️⃣ Configure o Projeto Localmente

1. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

2. **Crie o arquivo `.env`** na raiz do projeto:
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

⚠️ **Importante:** Não compartilhe essas credenciais no GitHub!

### 5️⃣ Execute o Aplicativo

```bash
python app.py
```

### 6️⃣ Teste o Sistema

1. Acesse: **http://localhost:5000**
2. Preencha o formulário com:
   - **Nome:** Seu nome
   - **WhatsApp:** Seu número com DDD (ex: 11 98765-4321)
   - **Barbeiro:** Escolha um
   - **Data:** Uma data futura
   - **Horário:** Escolha um horário
   - **Serviço:** Escolha um

3. Clique em **Agendar**
4. Você receberá uma mensagem no WhatsApp! 🎉

---

## 📝 Próximos Passos (Versão Paga)

Quando estiver pronto para usar em produção:

1. **Upgrade da Conta Twilio** - Plano pago
2. **Verificar Número Real** - Usar seu número de telefone
3. **Deploy** - Colocar em um servidor (Heroku, PythonAnywhere, etc)

---

## 🔧 Troubleshooting

### Mensagem não está sendo enviada

- Verifique se as credenciais no `.env` estão corretas
- Confirme que você entrou no WhatsApp Sandbox
- Verifique o console Python para mensagens de erro

### Erro "Invalid 'From' number"

- Certifique-se de que o `TWILIO_WHATSAPP_NUMBER` está no formato correto: `whatsapp:+14155238886`

### Número de WhatsApp inválido

- Deve ter DDD + 8 ou 9 dígitos
- Exemplo: `11987654321` (com código 55 do Brasil)

---

## 💡 Dicas

- **Teste localmente primeiro** antes de colocar em produção
- **Salve as credenciais em um local seguro**
- **Nunca compartilhe o Auth Token** no GitHub
- **Use `.gitignore`** para não fazer push do `.env`

