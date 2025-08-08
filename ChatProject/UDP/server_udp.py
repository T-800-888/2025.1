# Importação as bibliotecas necessárias
import socket  # Para comunicação em rede
import threading  # Para executar várias tarefas ao mesmo tempo
from datetime import datetime  # Para trabalhar com datas e horas

# Classe principal do servidor UDP
class UDPServer:
    def __init__(self, host='127.0.0.1', port=12346): # Construtor da inicialização
        self.host = host  # Endereço IP do servidor
        self.port = port  # Porta de comunicação
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Cria um socket UDP
        self.server_socket.bind((self.host, self.port)) # Associa o socket ao endereço e porta
        self.clients = {}  # Para armazenar clientes conectados
        self.lock = threading.Lock()  # Lock para evitar conflitos entre threads
        self.running = True  # Flag para controlar se o servidor está ativo

    # Inicialização do servidor
    def start(self):
        print(f"[{self.get_timestamp()}] Servidor UDP iniciado em {self.host}:{self.port}") # Mensagem de inicialização com data e hora
        try:
            # Loop principal do servidor
            while self.running:
                try:
                    # Recebe dados de um cliente (máx 1024 bytes)
                    data, addr = self.server_socket.recvfrom(1024)
                    threading.Thread( # Cria uma nova thread para processar a mensagem
                        target=self.process_client_message,  # Função que será executada
                        args=(data, addr),  # Argumentos para a função
                        daemon=True  # Thread termina com o término do programa principal
                    ).start()
                except OSError:  # Erro se o socket for fechado
                    break
        except KeyboardInterrupt:  # Se usuário pressionar Ctrl+C
            self.stop()  # Para o servidor
        finally:
            self.server_socket.close()  # Garante que o socket será fechado

    # Processamento de mensagens dos clientes
    def process_client_message(self, data, addr):
        try:
            message = data.decode('utf-8').strip() # Converte os dados recebidos em texto

            # Se for um novo cliente
            if addr not in self.clients:
                with self.lock: # Bloqueia acesso ao dicionário de clientes para evitar conflitos
                    self.clients[addr] = message  # Armazena o nome do cliente
                print(f"[{self.get_timestamp()}] {message} conectado de {addr}.") # Mostra mensagem de conexão
                self.broadcast(f"{message} entrou no chat.", exclude_addr=addr) # Mensagem de aviso da nova conexão
                return  # Termina a execução
            
            name = self.clients.get(addr, "Anônimo") # Pega o nome do cliente
            
            # Se a mensagem for comando de sair
            '''Critério 5: Quando o cliente envia /sair, 
            o servidor remove seu endereço de self.clients e notifica os outros (process_client_message()).'''
            if message.lower() == '/sair':
                with self.lock:
                    if addr in self.clients:
                        del self.clients[addr]  # Remove o cliente
                print(f"[{self.get_timestamp()}] {name} desconectado.")
                self.broadcast(f"{name} saiu do chat.") # Avisa todos sobre a saída
                return
            
            self.broadcast(f"{name}: {message}") # Se não for mensagem de saída, envia para todos
            
        except Exception as e:  # Trata erros
            print(f"[{self.get_timestamp()}] Erro ao processar mensagem: {e}")

    # Envia mensagem para todos os clientes
    '''Critério 3: O método broadcast() envia mensagens para todos os clientes registrados em self.clients usando sendto().'''
    def broadcast(self, message, exclude_addr=None):
        # Adiciona timestamp à mensagem
        full_message = f"[{self.get_timestamp()}] {message}"
        # Cria cópia segura da lista de clientes
        with self.lock:
            clients_copy = list(self.clients.items())
        # Para cada cliente conectado
        for client_addr, client_name in clients_copy:
            # Pula o cliente que não deve receber a mensagem
            if exclude_addr and client_addr == exclude_addr:
                continue
            try:
                # Envia a mensagem codificada para o cliente
                self.server_socket.sendto(full_message.encode('utf-8'), client_addr)
            except Exception as e:
                # Se houver erro, mostra mensagem e remove cliente
                print(f"[{self.get_timestamp()}] Erro ao enviar para {client_name} ({client_addr}): {e}")
                if client_addr in self.clients:
                    with self.lock:
                        if client_addr in self.clients:
                            del self.clients[client_addr]

    # Método para parar o servidor
    def stop(self):
        self.running = False  # Altera flag para sair do loop
        self.server_socket.close()  # Fecha o socket
        print(f"[{self.get_timestamp()}] Encerrando servidor UDP...")
        print("[PROJETO CHAT UDP] - CRIADO POR:\n— LETÍCIA MINIUK\n— RAYSSA GRAFETTI\n— VICTOR BITTENCOURT")

    # Método estático para obter data/hora formatada
    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Se executado diretamente (não importado)
if __name__ == "__main__":
    print("[SERVIDOR UDP]")
    server = UDPServer()  # Cria instância do servidor
    server.start()  # Inicia o servidor

'''Critério 7: Try-except para erros de socket e desconexões'''
