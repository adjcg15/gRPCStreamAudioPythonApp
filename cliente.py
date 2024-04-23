import grpc
import audio_pb2
import audio_pb2_grpc
import pyaudio

def streamAudio(stub, file_name):
    response = stub.downloadAudio(
        audio_pb2.DownloadFileRequest(nombre=file_name)
    )

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=2, rate=48000, output=True)

    print("Reproduciendo el archivo: " + file_name)
    for audio_chunk in response:
        print(".", end="", flush=True)
        stream.write(audio_chunk.data)

    print("\nRecepción de datos correcta.")
    print("Reproducción terminada.", end="\n\n")

def run():
    port = "8080"

    channel = grpc.insecure_channel("localhost:" + port)
    stub = audio_pb2_grpc.AudioServiceStub(channel)
    file_name = ""

    try:
        file_name = "anyma.wav"
        streamAudio(stub, file_name)
    except KeyboardInterrupt:
        pass
    finally:
        channel.close()

if __name__ == "__main__":
    run()