from flask import Flask, request, jsonify, render_template_string
import time
import threading

app = Flask(__name__)

servers = []
logs = []
active_users = {}  # username: {avatar, timestamp}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Roblox Joiner Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <meta http-equiv="refresh" content="8">
</head>
<body class="bg-zinc-950 text-white">
<div class="max-w-6xl mx-auto p-6">
    <h1 class="text-4xl font-bold text-green-400 mb-2">ROBLOX JOINER</h1>
    <p class="text-zinc-400 mb-8">Live Dashboard • Mise à jour toutes les 8 secondes</p>

    <!-- Active Users -->
    <div class="mb-8">
        <h2 class="text-xl font-semibold mb-3">👥 Personnes actives</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4" id="active">
            <!-- Rempli par JS -->
        </div>
    </div>

    <!-- Recent Servers -->
    <div class="mb-8">
        <h2 class="text-xl font-semibold mb-3">📡 Serveurs détectés</h2>
        <div id="servers" class="space-y-3"></div>
    </div>

    <!-- Logs -->
    <div>
        <h2 class="text-xl font-semibold mb-3">📜 Logs récents</h2>
        <div id="logs" class="bg-zinc-900 p-4 rounded-xl text-sm font-mono text-green-300 overflow-auto max-h-64"></div>
    </div>
</div>

<script>
function updateDashboard() {
    fetch('/get_servers').then(r => r.json()).then(data => {
        let html = '';
        data.forEach(s => {
            html += `
            <div class="bg-zinc-900 p-4 rounded-xl flex justify-between items-center">
                <div>
                    <div class="font-bold">${s.name}</div>
                    <div class="text-green-400">${s.rate}</div>
                </div>
                <a href="${s.url}" target="_blank" class="bg-green-500 hover:bg-green-600 px-6 py-2 rounded-lg text-sm font-bold">JOIN</a>
            </div>`;
        });
        document.getElementById('servers').innerHTML = html || '<p class="text-zinc-500">Aucun serveur pour l’instant...</p>';
    });

    // Active users (simulé pour l’instant)
    // On peut l'améliorer plus tard avec /ping
}
setInterval(updateDashboard, 8000);
updateDashboard();
</script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(HTML)

@app.route('/add_server', methods=['POST'])
def add_server():
    data = request.get_json()
    if data:
        data["timestamp"] = time.time()
        servers.append(data)
        if len(servers) > 30:
            servers.pop(0)
        logs.append(f"[{time.strftime('%H:%M:%S')}] + {data.get('name')} | {data.get('rate')}")
        if len(logs) > 20:
            logs.pop(0)
        print(f"✅ Serveur ajouté : {data.get('name')} | {data.get('rate')}")
    return jsonify({"status": "ok"})

@app.route('/get_servers')
def get_servers():
    return jsonify(servers[-20:])

@app.route('/ping', methods=['POST'])
def ping():
    data = request.get_json()
    if data and data.get('username'):
        username = data['username']
        masked = username[:3] + "******"
        active_users[username] = {
            "masked": masked,
            "avatar": f"https://www.roblox.com/headshot-thumbnail/image?userId={data.get('userId', 1)}&width=48&height=48&format=Png",
            "time": time.time()
        }
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
