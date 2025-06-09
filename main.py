from flask import Flask, request, jsonify
import whisper
import os

app = Flask(__name__)

# Carrega o modelo Whisper mais leve
model = whisper.load_model("tiny")

@app.route('/')
def home():
    return 'Lingoplay API - Online ✅'

@app.route('/avaliar-pronuncia', methods=['POST'])
def avaliar_pronuncia():
    if 'audio' not in request.files:
        return jsonify({'erro': 'Arquivo de áudio não encontrado.'}), 400

    audio_file = request.files['audio']
    audio_path = 'temp_audio.mp3'
    audio_file.save(audio_path)

    try:
        resultado = model.transcribe(audio_path)
        texto = resultado['text'].strip()

        feedback = "Boa tentativa!" if "r" in texto.lower() else "Pratique mais a pronúncia do R"

        return jsonify({
            'transcricao': texto,
            'feedback': feedback
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
