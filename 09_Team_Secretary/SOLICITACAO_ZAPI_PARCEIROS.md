# SOLICITAÇÃO DE CRIAÇÃO E CONFIGURAÇÃO DE CONTA Z-API (WHATSAPP)

> **Destinatário**: Equipe de Operações / Parceiros no Brasil  
> **Remetente**: Selena (`09_Team_Secretary`) — Equipe APEX Revenue SDR OS  
> **Objetivo**: Instruções passo a passo para contratação, pareamento de WhatsApp e envio das credenciais Z-API necessárias para integração com a plataforma de IA.

---

## 📌 Visão Geral

Para integrar o agente inteligente de vendas (SDR IA) ao número oficial de WhatsApp do projeto, utilizamos a plataforma **Z-API**. 

Solicitamos a gentileza de seguir o roteiro abaixo para criar a instância, parear o número de telefone via QR Code e nos enviar as **3 credenciais de acesso**.

---

## 🚀 Passo a Passo de Configuração

### 1. Acesso à Plataforma Z-API
* **Painel Administrativo**: [https://admin.z-api.io/](https://admin.z-api.io/)

### 2. Criação da Instância
1. Faça login ou crie uma conta no painel da Z-API.
2. Clique no botão **"Criar nova instância"**.
3. Dê um nome identificável para a instância (exemplo: `APEX SDR - Nome do Parceiro`).

### 3. Conexão do WhatsApp (QR Code)
1. No painel da Z-API, acesse a aba **QR Code**.
2. Abra o aplicativo **WhatsApp** no aparelho celular corporativo dedicado.
3. Acesse **Configurações / Aparelhos Conectados** $\rightarrow$ **Conectar um aparelho**.
4. Aponte a câmera do celular para o QR Code exibido na tela da Z-API até que o status mude para **Conectado**.

### 4. Configuração dos Webhooks (Mensagens Recebidas)
1. No painel da Z-API, acesse o menu **Webhooks**.
2. No campo **Ao receber mensagem**, insira a URL do nosso servidor (ou a URL fornecida pela equipe técnica APEX):
   ```text
   https://api.seu-dominio.com/api/v1/webhooks/zapi
   ```
3. Garanta que as notificações para **Mensagens de Texto**, **Mensagens de Áudio** e **Status de Leitura/Envio** estejam ativadas.

---

## 🔑 Credenciais que Precisam ser Enviadas à Equipe APEX

Após concluir a conexão, acesse o painel da sua instância e nos envie as seguintes informações de forma segura:

| Nome da Variável | Nome no Painel Z-API | Exemplo de Formato |
|---|---|---|
| `ZAPI_INSTANCE_ID` | **ID da Instância** | `3C1488A8...` |
| `ZAPI_CLIENT_TOKEN` | **Token da Instância** | `F4819A...` |
| `ZAPI_SECURITY_TOKEN` | **Security Token** (Aba Webhooks / Segurança) | `Client-Token-...` |

---

## 📋 Checklist de Validação Final

- [ ] Instância criada no Z-API.
- [ ] WhatsApp conectado via QR Code (Status: *Conectado*).
- [ ] URL de Webhook cadastrada no painel.
- [ ] `ZAPI_INSTANCE_ID`, `ZAPI_CLIENT_TOKEN` e `ZAPI_SECURITY_TOKEN` copiados e enviados.

Em caso de dúvidas técnicas durante a configuração, favor entrar em contato com a equipe de engenharia do projeto APEX.
