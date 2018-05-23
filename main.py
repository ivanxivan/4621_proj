from Web import *

def shutdown(sig, unused):
    server.shutdown()
    sys.exit(1)

signal.signal(signal.SIGINT, shutdown)
server = Web(4621)
server.start()
print("server start")