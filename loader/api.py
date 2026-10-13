"""API HTTP interne exposant le loader à n8n (specs/04-n8n-workflow.md).

L'image n8n utilisée est durcie (pas d'interpréteur Python disponible pour un
nœud "Execute Command"), ce service enveloppe donc `load_file` du module
`load` pour qu'un nœud HTTP Request n8n puisse déclencher le chargement et
recevoir le succès/échec par code HTTP. Aucune logique métier/KPI ici,
uniquement le wrapper HTTP autour de la spec 02.
"""

from pathlib import Path

import psycopg
from flask import Flask, jsonify, request

from load import LoadError, load_file

app = Flask(__name__)


@app.post("/load")
def load():
    payload = request.get_json(silent=True) or {}
    file_path = payload.get("file")
    if not file_path:
        return jsonify(status="error", reason="parametre 'file' manquant"), 400

    try:
        count = load_file(Path(file_path))
    except LoadError as exc:
        return jsonify(status="error", reason=str(exc)), 422
    except psycopg.Error as exc:
        return jsonify(status="error", reason=f"erreur base de donnees : {exc}"), 500

    return jsonify(status="ok", rows=count)


@app.get("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
