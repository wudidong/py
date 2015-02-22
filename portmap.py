import socket, select, SocketServer, time

class ThreadingTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer): pass

class PortServer(SocketServer.StreamRequestHandler):
	def handle_tcp(self, sock, client):
		fdset = [sock, client]
		while True:
			r, w, e = select.select(fdset, [], [])
			if sock in r:
				if client.send(sock.recv(4096)) <= 0:
					break
			if client in r:
				if sock.send(client.recv(4096)) <= 0:
					break
	def handle(self):
		try:
			print 'socks connection from', self.client_address
			remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			remote.bind(('', 9900))
			remote.listen(5)
			print 'Listen Port 9900, Waiting Client Connection.....'
			client, addr = remote.accept()
			print 'client connection from %s:%d' % (addr[0], addr[1])
			sock = self.request
			self.handle_tcp(sock, client)

		except socket.error:
			print 'socket error'


def main():
	server = ThreadingTCPServer(('', 1080), PortServer)
	server.serve_forever()

if __name__=='__main__':
	main()