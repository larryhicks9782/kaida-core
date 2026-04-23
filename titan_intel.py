import subprocess, json
class TitanIntel:
    def get_stats(self):
        try:
            batt = json.loads(subprocess.check_output(['termux-battery-status']).decode('utf-8'))
            loc = json.loads(subprocess.check_output(['termux-location', '-p', 'last']).decode('utf-8'))
            return f"[Phone Intel] Battery: {batt['percentage']}% | Location: {loc['latitude']}, {loc['longitude']}"
        except:
            return "[Phone Intel] Sensors offline. Check Termux:API permissions."
