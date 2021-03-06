from client import ChatClient
import threading
import socket
import sys
import random


PORT = random.randint(9000, 9009) # IT'S OVER 9000!!!!


class ChatServer(threading.Thread):
    def __init__(self, port, host='localhost'):
        super().__init__(daemon=True)
        self.port = port
        self.host = host
        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP
        )
        self.client_pool = []

        try:
            self.server.bind((self.host, self.port))
        except socket.error:
            print('Bind failed {}'.format(socket.error))
            sys.exit()

        self.server.listen(10)

    def parser(self, id, nick, conn, message):
        if message.decode().startswith('@'):
            data = message.decode().split(maxsplit=1)

            if data[0] == '@quit':
                conn.sendall(b'You have left the chat.')
                reply = nick.encode() + b'has left the channel.\n'
                print(str(nick.encode()) + 'has left the channel.')
                [c.conn.sendall(reply) for c in self.client_pool if len(self.client_pool)]
                self.client_pool = [c for c in self.client_pool if c.id != id]
                del id
                conn.close()

            elif data[0] == '@list':  
                for users in range(0, len(self.client_pool)):
                    # print(self.client_pool[users].nick.encode())
                    conn.sendall(self.client_pool[users].nick.encode())
                    new_line = b'\n'
                    conn.send(new_line)

            elif data[0] == '@nickname':
                print('User changed name from : ' + nick + '  to: ' + str(data[1]))
                # print(self.client_pool[0].nick)
                for users in range(0, len(self.client_pool)):
                    if self.client_pool[users].nick == nick:
                        self.client_pool[users].nick = data[1]

            elif data[0] == '@dm':
                to_user = data[1]
                message = data[2:]
                print('from: ' + str(nick) + '| to: ' + str(to_user) + ': ' + str(message))
                for users in range(0, len(self.client_pool)):
                    print('address:' + self.client_pool[users].addr)
                    if self.client_pool[users].nick == to_user:
                        print(self.client_pool[users].nick + 'found!')
                        print('address:' + self.client_pool[users].addr)
                        conn.sendto(message, self.client_pool[users].addr)

            else:
                conn.sendall(b'Invalid command. Please try again.\n')

        else:
            reply = nick.encode() + b': ' + message
            [c.conn.sendall(reply) for c in self.client_pool if len(self.client_pool)]

    def run_thread(self, id, nick, conn, addr):
        print('{} connected with {}:{}'.format(nick, addr[0], str(addr[1])))
        try:
            while True:
                data = conn.recv(4096)
                self.parser(id, nick, conn, data)
        except (ConnectionResetError, BrokenPipeError, OSError):
            conn.close()

    def run(self):
        print('Server running on {}'.format(PORT))
        while True:
            conn, addr = self.server.accept()
            client = ChatClient(conn, addr)
            self.client_pool.append(client)
            threading.Thread(
                target=self.run_thread,
                args=(client.id, client.nick, client.conn, client.addr),
                daemon=True
            ).start()

    def exit(self):
        self.server.close()


if __name__ == '__main__':
    server = ChatServer(PORT)
    try:
        server.run()
    except KeyboardInterrupt:
        [c.conn.close() for c in server.client_pool if len(server.client_pool)]
        server.exit()