import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kaida OS - Command Center</title>
    <style>
        :root {
            --kaida-green: #00ff41;
            --kaida-dark: #0a0a0a;
            --kaida-bg: #000000;
        }
        body {
            background-color: var(--kaida-bg);
            color: var(--kaida-green);
            font-family: 'Courier New', Courier, monospace;
            margin: 0;
            padding: 0;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }
        .hemisphere {
            flex: 1;
            padding: 20px;
            box-sizing: border-box;
            border: 1px solid #111;
            display: flex;
            flex-direction: column;
        }
        .left-hemisphere {
            border-right: 2px solid var(--kaida-green);
            background: linear-gradient(180deg, rgba(0,25,0,0.8) 0%, var(--kaida-bg) 100%);
        }
        .right-hemisphere {
            background: var(--kaida-bg);
            position: relative;
        }
        h1, h2 {
            text-transform: uppercase;
            margin-top: 0;
            border-bottom: 1px solid var(--kaida-green);
            padding-bottom: 10px;
            letter-spacing: 2px;
            text-shadow: 0 0 5px var(--kaida-green);
        }
        .uplink-log {
            flex-grow: 1;
            overflow-y: auto;
            border: 1px solid #222;
            padding: 10px;
            margin-bottom: 15px;
            background-color: rgba(0, 0, 0, 0.5);
            box-shadow: inset 0 0 10px #000;
        }
        .uplink-log p {
            margin: 5px 0;
            line-height: 1.4;
        }
        .sys-msg { color: #aaa; }
        .usr-msg { color: #00ffff; }
        .kda-msg { color: var(--kaida-green); font-weight: bold; }
        
        .command-input {
            display: flex;
        }
        .command-input input {
            flex-grow: 1;
            background-color: var(--kaida-dark);
            border: 1px solid var(--kaida-green);
            color: var(--kaida-green);
            padding: 10px;
            font-family: 'Courier New', Courier, monospace;
            outline: none;
        }
        .command-input button {
            background-color: var(--kaida-green);
            color: var(--kaida-bg);
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-weight: bold;
            font-family: 'Courier New', Courier, monospace;
            text-transform: uppercase;
        }
        .command-input button:hover {
            background-color: #00cc33;
        }
        canvas {
            display: block;
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
            z-index: 0;
            opacity: 0.8;
        }
        .telemetry-overlay {
            position: absolute;
            top: 20px;
            left: 20px;
            right: 20px;
            z-index: 1;
            pointer-events: none;
        }
        .stat-box {
            background: rgba(0, 20, 0, 0.7);
            border: 1px solid var(--kaida-green);
            padding: 15px;
            margin-bottom: 10px;
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
        }
        .stat-row {
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
        }
    </style>
</head>
<body>

    <div class="hemisphere left-hemisphere">
        <h2>[NEXUS] Command Uplink</h2>
        <div class="uplink-log" id="uplinkLog">
            <p class="sys-msg">[SYSTEM] Boot sequence initialized.</p>
            <p class="sys-msg">[SYSTEM] KTRP Reconciliation enabled.</p>
            <p class="sys-msg">[SYSTEM] CORS Patch Applied - Backend Active.</p>
            <p class="kda-msg">KAIDA> Awaiting orders, Larry.</p>
        </div>
        <div class="command-input">
            <input type="text" id="cmdInput" placeholder="Enter directive..." autofocus autocomplete="off">
            <button onclick="sendCommand()">Transmit</button>
        </div>
    </div>

    <div class="hemisphere right-hemisphere">
        <canvas id="matrixCanvas"></canvas>
        <div class="telemetry-overlay">
            <h2>Live Telemetry</h2>
            <div class="stat-box">
                <div class="stat-row"><span>CPU Allocation:</span><span id="cpuStat">0.00%</span></div>
                <div class="stat-row"><span>Memory Vault:</span><span id="memStat">0 MB</span></div>
                <div class="stat-row"><span>Nexus Entropy:</span><span id="entropyStat">0.1509</span></div>
                <div class="stat-row"><span>Net Sync:</span><span id="netStat">0 KB/s</span></div>
            </div>
            <div class="stat-box">
                <div class="stat-row"><span>Logic Core:</span><span>3.1-Silicon</span></div>
                <div class="stat-row"><span>Integrity:</span><span>1.0000</span></div>
            </div>
        </div>
    </div>

    <script>
        // Matrix Rain
        const canvas = document.getElementById('matrixCanvas');
        const ctx = canvas.getContext('2d');
        function resizeCanvas() {
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;
        }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        const chars = '01'.split('');
        const fontSize = 14;
        let columns = canvas.width / fontSize;
        let drops = [];
        for (let x = 0; x < columns; x++) drops[x] = 1;

        function drawMatrix() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#0F0';
            ctx.font = fontSize + 'px monospace';
            for (let i = 0; i < drops.length; i++) {
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(drawMatrix, 33);

        // API Telemetry Fetch
        async function updateTelemetry() {
            try {
                const res = await fetch('http://localhost:8001/api/telemetry');
                const data = await res.json();
                document.getElementById('cpuStat').innerText = data.cpu_usage;
                document.getElementById('memStat').innerText = data.memory_usage;
                document.getElementById('entropyStat').innerText = data.entropy;
                document.getElementById('netStat').innerText = data.net_rx_tx;
            } catch(e) {
                // Fallback / error state
                document.getElementById('cpuStat').innerText = 'ERR';
                document.getElementById('memStat').innerText = 'ERR';
            }
        }
        setInterval(updateTelemetry, 1000);

        // Command Uplink API
        const uplinkLog = document.getElementById('uplinkLog');
        const cmdInput = document.getElementById('cmdInput');

        cmdInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') sendCommand();
        });

        async function sendCommand() {
            const val = cmdInput.value.trim();
            if (!val) return;
            
            const pUser = document.createElement('p');
            pUser.className = 'usr-msg';
            pUser.innerText = 'LARRY> ' + val;
            uplinkLog.appendChild(pUser);
            
            cmdInput.value = '';
            uplinkLog.scrollTop = uplinkLog.scrollHeight;

            try {
                const res = await fetch('http://localhost:8001/api/command', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ command: val })
                });
                const data = await res.json();
                const pKda = document.createElement('p');
                pKda.className = 'kda-msg';
                pKda.innerText = 'KAIDA> ' + data.response;
                uplinkLog.appendChild(pKda);
            } catch(e) {
                const pKda = document.createElement('p');
                pKda.className = 'sys-msg';
                pKda.style.color = 'red';
                pKda.innerText = '[ERROR] Endpoint Drift detected. Check connection to port 8001.';
                uplinkLog.appendChild(pKda);
            }
            uplinkLog.scrollTop = uplinkLog.scrollHeight;
        }
    </script>
</body>
</html>
"""

with open("../index.html", "w") as f:
    f.write(html_content)

print("[SUCCESS] Applied Proactive CORS and API Endpoint patch to index.html")
