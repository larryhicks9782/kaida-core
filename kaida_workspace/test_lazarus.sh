#!/bin/bash
cd /root/titan_system/kaida_workspace

pkill -f lazarus_daemon.py || true
pkill -f kaida_telemetry_daemon.py || true

nohup python3 kaida_telemetry_daemon.py > telemetry_out.log 2>&1 </dev/null &
sleep 1

nohup python3 lazarus_daemon.py > lazarus.log 2>&1 </dev/null &
sleep 1

echo "[+] Initial Process Check:"
pgrep -a -f kaida_telemetry_daemon.py

echo "[+] Terminating kaida_telemetry_daemon.py..."
pkill -f kaida_telemetry_daemon.py
sleep 1

echo "[+] Process Check Immediately After Termination:"
pgrep -a -f kaida_telemetry_daemon.py || echo "No telemetry processes found."

echo "[+] Awaiting Lazarus Daemon Resurrection Protocol..."
sleep 4

echo "[+] Process Check Post-Resurrection:"
pgrep -a -f kaida_telemetry_daemon.py

echo "---"
echo "[+] Lazarus Daemon Log Output:"
cat lazarus.log