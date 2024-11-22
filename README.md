# TTSVN

TTSVN is a Text-to-Speech (TTS) service that converts text into speech using pre-trained models. This project uses gRPC for communication and model inference.
linkmodel:https://drive.google.com/drive/folders/1Jr_kHl0Pe5K2oXSIg5gozMM4F8RHcRTe?usp=sharing
## Prerequisites

- Python 3.10
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:
    ```sh
    git clone <your-repository-url>
    cd TTSVN
    ```
2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```
3. Docker
    ```sh
    docker compose build 
    docker run -it  ttsvn_ttsvn
   or pull image from docker hubdocker:  docker pull  kanh164/ttsvn_ttsvn 
    ```
## Usage

### Running the gRPC Server

Start the gRPC server:
```sh
python main.py