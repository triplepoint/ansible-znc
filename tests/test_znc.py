def test_service_running(Service):
    service = Service('znc')
    assert service.is_running

def test_socket_listening(Socket):
    socket = Socket('tcp://127.0.0.1:6666')
    assert socket.is_listening
