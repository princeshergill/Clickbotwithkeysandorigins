import subprocess
import time
from pathlib import Path
import random

# Directory containing your Proton VPN WireGuard config files
WG_DIR = Path("/home/prince/proton-vpn-configs")
configs = list(WG_DIR.glob("*.conf"))

if not configs:
    print("❌ No WireGuard configs found.")
    exit(1)

def connect(conf_path):
    print(f"🔄 Connecting using: {Path(conf_path).name}")
    try:
        subprocess.run(["sudo", "wg-quick", "up", conf_path], check=True)
        time.sleep(2)

        # Fetch external IP
        result = subprocess.run(["curl", "-s", "https://ipinfo.io/ip"], capture_output=True, text=True)
        ip = result.stdout.strip()
        if ip:
            print(f"✅ Connected. IP: {ip}")
        else:
            print("⚠️ Could not retrieve external IP.")

    except subprocess.CalledProcessError as e:
        print(f"❌ VPN failed to connect: {e}")
    finally:
        print("🔌 Disconnecting VPN...")
        subprocess.run(["sudo", "wg-quick", "down", conf_path])
        print("✅ VPN disconnected.")

# Pick a random config and run test
conf = random.choice(configs)
connect(str(conf))
