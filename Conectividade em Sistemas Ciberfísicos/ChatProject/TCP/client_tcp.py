# Importa bibliotecas necessárias
import socket  # Para comunicação em rede
import threading  # Para executar várias tarefas ao mesmo tempo
from datetime import datetime  # Para trabalhar com datas e horas

# Classe principal do cliente TCP
class TCPClient:
    def __init__(self, host='127.0.0.1', port=12345): # Construtor da inicialização
        self.host = host  # Endereço do servidor
        self.port = port  # Porta do servidor
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria socket TCP
        self.running = False  # Flag para controlar execução
        self.name = ""  # Nome do usuário

    # Método principal do cliente
    def start(self):
        try:
            self.client_socket.connect((self.host, self.port)) # Conecta ao servidor
            self.name = input("Digite seu nome: ").strip() or "Anônimo" # Pede nome do usuário (ou usa "Anônimo" se vazio)
            '''Critério 3: O nome é enviado na conexão inicial (client_socket.send(self.name.encode('utf-8')) 
            e usado no formato das mensagens (f"{name}: {message}").'''
            self.client_socket.send(self.name.encode('utf-8')) # Envia nome para o servidor
            self.running = True  # Ativa flag
            receive_thread = threading.Thread(target=self.receive_messages) # Cria thread para receber mensagens
            receive_thread.daemon = True  # Thread morre com programa principal
            receive_thread.start()  # Inicia thread
            self.send_messages() # Chama método para enviar mensagens
            
        except (ConnectionRefusedError, socket.error) as e:  # Se não conectar
            print(f"[{self.get_timestamp()}] Erro ao conectar ao servidor: {e}") 
        finally:
            self.stop()  # Encerra cliente

    # Método para enviar mensagens
    def send_messages(self):
        while self.running:
            try:
                message = input() # Lê mensagem do usuário
                '''Critério 4: O servidor remove o cliente do dicionário self.clients e notifica os outros.'''
                if message.lower() == '/sair': # Se for comando de sair
                    self.client_socket.send(message.encode('utf-8')) # Envia comando e para o cliente
                    self.stop()
                    break
                self.client_socket.send(message.encode('utf-8')) # Envia mensagem normal
            except (KeyboardInterrupt, EOFError):  # Se pressionar Ctrl+C ou EOF
                self.stop()
                break

    # Método para receber mensagens
    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8') # Recebe mensagem do servidor
                if not message:  # Se vazio, servidor fecha
                    self.stop()
                    break
                print(message)  # Mostra mensagem
            except (ConnectionResetError, socket.error):  # Erros de conexão
                self.stop()
                break

    # Método para parar o cliente
    def stop(self):
        if self.running:
            self.running = False  # Altera flag
            print(f"[{self.get_timestamp()}] Desconectando do servidor TCP...")
            self.client_socket.close()  # Fecha socket

    # Método estático para obter data/hora formatada
    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Se executado diretamente
if __name__ == "__main__":
    # Mostra instruções
    print("[CHAT PRINCIPAL]\n" \
    "Para sair do chat, digite '/sair' a qualquer momento.")
    client = TCPClient()  # Cria cliente
    client.start()  # Inicia cliente
