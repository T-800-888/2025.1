import socket  # Para comunicação em rede
import threading  # Para executar várias tarefas ao mesmo tempo
from datetime import datetime  # Para trabalhar com datas e horas

# Classe principal do cliente UDP
class UDPClient:
    def __init__(self, host='127.0.0.1', port=12346): # Construtor de inicialização
        self.host = host  # Endereço IP do servidor
        self.port = port  # Porta do servidor
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (host, port)  # Tupla com endereço do servidor
        self.running = True  # Flag para controlar execução

    # Inicialização do cliente
    def start(self):
        
        name = input("Digite seu nome: ").strip() or "Anônimo" # Pede nome do usuário (ou usa "Anônimo" se vazio)
        '''Critério 4: O nome é enviado na primeira mensagem via sendto(name.encode())) 
        e armazenado no dicionário self.clients do servidor.'''
        self.client_socket.sendto(name.encode('utf-8'), self.server_addr) # Envia nome para o servidor
        threading.Thread(target=self.receive_messages, daemon=True).start() # Cria thread para receber mensagens em segundo plano
        self.send_messages() # Chama método para enviar mensagens

    # Método para enviar mensagens
    def send_messages(self):
        while self.running: # Loop principal
            try:
                message = input() # Lê mensagem do usuário
                '''Critério 5: Quando o cliente envia /sair, 
                o servidor remove seu endereço de self.clients e notifica os outros (process_client_message()).'''
                if message.lower() == '/sair' :# Se for comando de sair
                    self.client_socket.sendto(b'/sair', self.server_addr) # Envia comando para o servidor
                    break  # Sai do loop
                # Envia mensagem para o servidor
                self.client_socket.sendto(message.encode('utf-8'), self.server_addr)
            except (KeyboardInterrupt, EOFError):  # Se pressionar Ctrl+C ou EOF
                break
        self.stop()  # Para o cliente

    # Método para receber mensagens
    def receive_messages(self):
        # Loop de recebimento
        while self.running:
            try:
                # Recebe dados do servidor
                data, _ = self.client_socket.recvfrom(1024)
                # Mostra mensagem decodificada
                print(data.decode('utf-8'))
            except:
                # Se houver erro e o cliente estiver ativo
                if self.running:
                    print("Conexão perdida.")
                break

    # Método para parar o cliente
    def stop(self):
        self.running = False  # Altera flag
        self.client_socket.close()  # Fecha socket
        print("Desconectado.")

    # Método estático para obter hora formatada
    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%H:%M:%S")

# Se executado diretamente (não importado)
if __name__ == "__main__":
    # Mostra instruções
    print("[CHAT PRINCIPAL]\n" \
    "Para sair do chat, digite '/sair' a qualquer momento.")
    client = UDPClient()  # Cria cliente
    client.start()  # Inicia cliente
