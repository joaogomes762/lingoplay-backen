from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import uuid
import os

app = Flask(__name__)
CORS(app)

model = whisper.load_model("tiny")

@app.route("/avaliar-pronuncia", methods=["POST"])
def avaliar():
    if 'audio' not in request.files:
        return jsonify({'error': 'Nenhum áudio recebido'}), 400

    audio = request.files['audio']
    nome_arquivo = f"/tmp/{uuid.uuid4()}.mp3"
    audio.save(nome_arquivo)

    try:
        resultado = model.transcribe(nome_arquivo)
        texto = resultado['text'].strip()
        feedback = "Boa pronúncia!" if 'r' in texto.lower() else "Pratique mais o som do R"
        return jsonify({ "transcricao": texto, "feedback": feedback })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500
    finally:
        os.remove(nome_arquivo)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
