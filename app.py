from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Liste des serveurs (on garde les 30 derniers)
servers = []

@app.route('/')
def home():
    return "✅ Roblox Discord Joiner Proxy - En ligne !"

@app.route('/add_server', methods=['POST'])
def add_server():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Pas de données"}), 400

    servers.append({
        "name": data.get("name", "Unknown"),
        "rate": data.get("rate", ""),
        "join_url": data.get("url", ""),
        "timestamp": time.time()
    })

    # Garde seulement les 30 derniers
    if len(servers) > 30:
        servers.pop(0)

    print(f"✅ Serveur ajouté → {data.get('name')} | {data.get('rate')}")
    return jsonify({"status": "ok", "total": len(servers)})

@app.route('/get_servers', methods=['GET'])
def get_servers():
    return jsonify(servers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)