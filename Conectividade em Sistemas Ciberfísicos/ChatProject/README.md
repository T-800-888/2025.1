# Chat TCP/UDP em Linha de Comando

## 📌 Descrição

Este projeto implementa um sistema de **comunicação cliente-servidor com suporte a múltiplos clientes**, utilizando os protocolos **TCP** e **UDP**. Desenvolvido como parte do Trabalho Final da disciplina **Conectividade de Sistemas Ciberfísicos** do curso de Engenharia de Software e Ciência da Computação da PUCPR, o sistema simula um ambiente de bate-papo via terminal.

## 🧠 Tecnologias e Conceitos Aplicados

- Python 3
- Sockets TCP e UDP
- Multithreading no servidor TCP
- Comunicação terminal (sem GUI)

## 📂 Estrutura do Projeto

```
chat_project/
├── tcp/
│   ├── server_tcp.py
│   └── client_tcp.py
├── udp/
│   ├── server_udp.py
│   └── client_udp.py
```

## ⚙️ Como Executar

### TCP

1. Inicie o servidor TCP:

```bash
python3 server_tcp.py
```

2. Em outros terminais, inicie clientes TCP:

```bash
python3 client_tcp.py
```

3. Insira um apelido e envie mensagens. Use `/sair` para encerrar.

### UDP

1. Inicie o servidor UDP:

```bash
python3 server_udp.py
```

2. Em outros terminais, inicie clientes UDP:

```bash
python3 client_udp.py
```

3. Insira um apelido e envie mensagens. Use `/sair` para encerrar.

## ✅ Funcionalidades

- Múltiplos clientes simultâneos
- Apelido visível nas mensagens
- Servidor multithread no TCP
- Encerramento com `/sair`
- Terminal como interface

## 🧪 Testes Recomendados

1. Iniciar o servidor (TCP ou UDP).
2. Conectar pelo menos 3 clientes.
3. Enviar e receber mensagens entre clientes.
4. Testar `/sair` para sair do chat.

## 👥 Autores(as)

Letícia Miniuk Rosa Pereira
Rayssa Gaievicz Grafetti
Victor Willian Rodrigues Bittencourt

PUCPR - Ciência da Computação 
Disciplina: Conectividade de Sistemas Ciberfísicos
