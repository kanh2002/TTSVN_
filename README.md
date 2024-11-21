
TTSVN
TTSVN is a Text-to-Speech (TTS) service that converts text into speech using pre-trained models. This project uses gRPC for communication and  model inference.

Prerequisites
Python 3.10
Docker (optional, for containerized deployment)

Installation
Clone the repository:
git clone <your-repository-url>
cd TTSVN
Install the required Python packages:
pip install -r requirements.txt

Usage
Running the gRPC Server
Start the gRPC server:
python main.py

Testing the TTS Service
Run the test script:
python test.py
The generated audio will be saved as output.wav

Docker Deployment
Build the Docker image:
sudo docker build -t ttsvn .
Run the Docker container:
sudo docker run -it ttsvn

File Structure
main.py: The main entry point for the gRPC server.
tts.proto: The gRPC service definition.
test.py: A test script to interact with the gRPC server.
requirements.txt: Python dependencies.

# TTSVN_
