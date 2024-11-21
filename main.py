import grpc
from concurrent import futures
from vietTTS.hifigan.mel2wave import mel2wave
from vietTTS.nat.text2mel import text2mel
from vietTTS import nat_normalize_text
import numpy as np
import json
import tts_pb2
import tts_pb2_grpc
import time
class TextToSpeechServicer(tts_pb2_grpc.TextToSpeechServiceServicer):
    def text_to_speech(self, text):
        # if len(text) > 500:
        #     text = text[:500]
        text = nat_normalize_text(text)

        mel = text2mel(
            text,
            "lexicon.txt",
            0.2,
            "acoustic_latest_ckpt.pickle",
            "duration_latest_ckpt.pickle",
        )
        wave_data = mel2wave(mel, "config.json", "hk_hifi.pickle")
        return (wave_data * (2**15)).astype(np.int16)

    def ConvertTextFileToSpeech(self, request, context):
        # Load JSON content from request
        data = json.loads(request.json_content)
        text = data.get("text", "")
        start_time = time.time()
        # Convert text to speech
        audio_data = self.text_to_speech(text)
        end_time = time.time()
        inference_time = end_time - start_time
        print(f"Inference time: {inference_time:.4f} seconds")
        return tts_pb2.AudioFileResponse(audio=audio_data.tobytes())

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tts_pb2_grpc.add_TextToSpeechServiceServicer_to_server(TextToSpeechServicer(), server)
    server.add_insecure_port('[::]:50056')

    server.start()
    print("gRPC server is running on port 50056.")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
