from abcvlib.abcvlibserver import (
    Message,
    Server,
    Response,
    ContentEncoding,
    ContentType,
)
from smartphone_robot_flatbuffers import Episode


class MyMessage(Message):
    def _on_episode_received(self, episode: Episode):
        pass

    def _on_response_request(self) -> dict:
        response = Response()
        response.add_bytes("Hello World".encode('utf-8'))
        response.set_content_encoding(ContentEncoding.UTF_8)
        response.set_content_type(ContentType.STRING)
        return response.to_dict()


server = Server(MyMessage)
server.start()
