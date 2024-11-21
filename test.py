import grpc
from concurrent import futures
from vietTTS.hifigan.mel2wave import mel2wave
from vietTTS.nat.text2mel import text2mel
from vietTTS import nat_normalize_text
import numpy as np
import json
import tts_pb2
import tts_pb2_grpc


class TextToSpeechServicer(tts_pb2_grpc.TextToSpeechServiceServicer):
    def text_to_speech(self, text):
        if len(text) > 500:
            text = text[:500]
        text = nat_normalize_text(text)
        mel = text2mel(
            text,
            "lexicon.txt",
            0.2,
            "acoustic_latest_ckpt.pickle",
            "duration_latest_ckpt.pickle",
        )
        wave_data = mel2wave(mel, "config.json", "hk_hifi.pickle")
        return (wave_data * (2 ** 15)).astype(np.int16)

    def ConvertTextFileToSpeech(self, request, context):
        # Load JSON content from request
        data = json.loads(request.json_content)
        text = data.get("text", "")

        # Convert text to speech
        audio_data = self.text_to_speech(text)
        return tts_pb2.AudioFileResponse(audio=audio_data.tobytes())


def serve():
    # Load TLS credentials
    with open("server.crt", "rb") as f:
        certificate_chain = f.read()
    with open("server.key", "rb") as f:
        private_key = f.read()

    # Create SSL server credentials
    server_credentials = grpc.ssl_server_credentials(
        [(private_key, certificate_chain)]
    )

    # Create gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tts_pb2_grpc.add_TextToSpeechServiceServicer_to_server(TextToSpeechServicer(), server)

    # Add secure port with domain
    server.add_secure_port("text-to-speech.hyratek.io:50055", server_credentials)
    print("gRPC server is running securely on https://text-to-speech.hyratek.io:50055")

    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
