# Importa bibliotecas necessárias
import socket  # Para comunicação em rede
import threading  # Para executar várias tarefas ao mesmo tempo
from datetime import datetime  # Para trabalhar com datas e horas

# Classe principal do servidor TCP
class TCPServer:
    def __init__(self, host='127.0.0.1', port=12345):# Construtor da inicialização
        self.host = host  # Endereço IP do servidor
        self.port = port  # Porta de comunicação
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria socket TCP
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Permite reutilizar o endereço
        self.clients = {} # Dicionário para armazenar clientes
        self.lock = threading.Lock()  # Lock para evitar conflitos
        self.running = False  # Flag para controlar execução
        
    # Inicialização do servidor
    def start(self):
        try:
            '''Critério 1: O parâmetro listen(5) permite até 5 conexões simultâneas (linha 22).'''
            self.server_socket.bind((self.host, self.port)) # Associa socket ao endereço e porta
            self.server_socket.listen(5) # Habilita servidor para aceitar até 5 conexões, resto na fila
            self.running = True  # Ativa flag
            print(f"[{self.get_timestamp()}] Servidor TCP iniciado em {self.host}:{self.port}")
            accept_thread = threading.Thread(target=self.accept_connections) # Cria thread para aceitar conexões
            accept_thread.daemon = True  # Thread morre com programa principal
            accept_thread.start()  # Inicia thread
            
            accept_thread.join()  # Espera thread terminar
            
        except Exception as e:  # Trata erros
            print(f"[{self.get_timestamp()}] Erro ao iniciar servidor: {e}")
        finally:
            self.shutdown()  # Encerra servidor

    # Método para aceitar conexões de clientes
    def accept_connections(self):
        while self.running:
            '''Critério 1: O servidor usa threading.Thread para cada cliente (handle_client)(linhas 40 a 46).'''
            try:
                client_socket, client_address = self.server_socket.accept() # Aceita nova conexão
                '''Critério 5: Cada cliente é tratado em uma thread separada (threading.Thread(target=self.handle_client))'''
                client_thread = threading.Thread( # Cria thread para lidar com o cliente
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()  # Inicia thread
            except OSError:  # Se socket fechado
                break
            except Exception as e:  # Outros erros
                print(f"[{self.get_timestamp()}] Erro ao aceitar conexão: {e}")

    def handle_client(self, client_socket, client_address): # Método para lidar com um cliente específico
        try:
            name = client_socket.recv(1024).decode('utf-8').strip() # Recebe nome do cliente
            
            with self.lock: # Armazena cliente com thread-safe
                self.clients[client_socket] = {'name': name, 'address': client_address}

            print(f"[{self.get_timestamp()}] {name} conectado de {client_address}") # Mostra mensagem de conexão
            self.broadcast(f"[{self.get_timestamp()}] {name} entrou no chat.", None) # Avisa todos sobre novo cliente

            while self.running: # Loop para receber mensagens do cliente
                try:
                    message = client_socket.recv(1024).decode('utf-8').strip() # Recebe mensagem
                    if not message:  # Se vazio, conexão fechada
                        break
                    
                    '''Critério 4: O servidor remove o cliente do dicionário self.clients e notifica os outros.'''
                    if message.lower() == '/sair':  # Comando de saída
                        break
                    
                    formatted_msg = f"[{self.get_timestamp()}] {name}: {message}" # Formata mensagem com timestamp
                    self.broadcast(formatted_msg, client_socket) # Envia para todos (exceto remetente)

                except (ConnectionResetError, socket.error):  # Erros de conexão
                    break
                except UnicodeDecodeError:  # Mensagem inválida
                    print(f"[{self.get_timestamp()}] Mensagem inválida de {name}.")
                    continue

        except Exception as e:  # Outros erros
            print(f"[{self.get_timestamp()}] Erro com cliente {client_address}: {e}")
        finally:
            self.safe_remove_client(client_socket) # Remove cliente com segurança

        '''Critério 2: Atendido pelo método broadcast(), que envia mensagens para todos os clientes (exceto o remetente).'''
    def broadcast(self, message, sender_socket=None): # Método para enviar mensagem para todos os clientes
        with self.lock:  # Thread-safe
            clients_to_remove = []  # Lista de clientes com problemas
            for client in list(self.clients.keys()): # Para cada cliente
                if client != sender_socket:  # Não envia para o remetente
                    try:
                        client.send(message.encode('utf-8')) # Envia mensagem
                    except (ConnectionResetError, BrokenPipeError, socket.error) as e:
                        print(f"[{self.get_timestamp()}] Erro ao enviar para {self.clients[client]['name']}: {e}") # Em caso de erro, marca para remoção
                        clients_to_remove.append(client)
            
            # Remove clientes com problemas
            for client in clients_to_remove:
                self.safe_remove_client(client)

    # Remove cliente com segurança
    def safe_remove_client(self, client_socket):
        try:
            if client_socket in self.clients:
                name = self.clients[client_socket]['name']
                print(f"[{self.get_timestamp()}] {name} saiu do chat.")
                
                # Remove do dicionário com thread-safe
                with self.lock:
                    del self.clients[client_socket]
                
                # Avisa todos sobre a saída
                self.broadcast(f"[{self.get_timestamp()}] {name} saiu do chat.", None)
                
                try:
                    client_socket.close()  # Fecha socket
                except:
                    pass
        except Exception as e:
            print(f"[{self.get_timestamp()}] Erro ao remover cliente: {e}.")

    # Encerramento do servidor
    def shutdown(self):
        if self.running:
            self.running = False  # Altera flag
            print(f"[{self.get_timestamp()}] Encerrando servidor TCP...")
            print("[PROJETO CHAT TCP] - CRIADO POR:\n— LETÍCIA MINIUK\n— RAYSSA GRAFETTI\n— VICTOR BITTENCOURT")
            
            # Remove todos os clientes com thread-safe
            with self.lock:
                for client in list(self.clients.keys()):
                    self.safe_remove_client(client)
            
            try:
                self.server_socket.close()  # Fecha socket principal
            except:
                pass

    # Método estático para obter data/hora formatada
    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Se executado diretamente
if __name__ == "__main__":
    print("[SERVIDOR TCP]")
    server = TCPServer()  # Cria servidor
    try:
        server.start()  # Inicia servidor
    except KeyboardInterrupt:  # Se pressionar Ctrl+C
        server.shutdown()  # Encerra corretamente

'''Critério 7: Inclui try-except para ConnectionResetError, socket.error, 
e outros (ex: safe_remove_client lida com desconexões inesperadas).'''
