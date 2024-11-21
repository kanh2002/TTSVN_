import grpc
import tts_pb2
import tts_pb2_grpc
import json
import wave

def save_audio(audio_data, output_file="output.wav"):
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio_data)

def main():
    # Load JSON data from file
    input_file = 'input.json'
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            json_content = f.read()
            json_data = json.loads(json_content)  # Validate JSON format
            if not isinstance(json_data, dict):
                raise ValueError("JSON content must be a dictionary")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Invalid JSON format: {e}")
        return

    # Connect to gRPC server
    with grpc.insecure_channel('localhost:50056') as channel:
        stub = tts_pb2_grpc.TextToSpeechServiceStub(channel)
        try:
            response = stub.ConvertTextFileToSpeech(tts_pb2.TextFileRequest(json_content=json_content))
            # Save the audio file from the response
            save_audio(response.audio)
            print("Audio has been saved to output.wav")
        except grpc.RpcError as e:
            print(f"gRPC error: {e}")

if __name__ == "__main__":
    main()