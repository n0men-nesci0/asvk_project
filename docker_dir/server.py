from xmlrpc.server import SimpleXMLRPCServer
import main

server = SimpleXMLRPCServer(('', 80))
server.register_function(main.main, "main")
server.serve_forever()