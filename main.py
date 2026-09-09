import json
import uuid
import base64
import urllib.parse
from pathlib import Path
from datetime import datetime

CONFIG_DIR = Path("configs")
CONFIG_DIR.mkdir(exist_ok=True)

Colors

R = "\033[91m"
G = "\033[92m"
C = "\033[96m"
Y = "\033[93m"
M = "\033[95m"
B = "\033[94m"
W = "\033[97m"
RESET = "\033[0m"
BOLD = "\033[1m"

def banner():
print("\033c", end="")
print(f"""
{C}{BOLD}╔══════════════════════════════════════════╗
║                                          ║
║        {Y}⚡ CONFIG MAKER ⚡{C}                 ║
║                                          ║
║        {M}V2Ray / Xray Generator{C}            ║
║        {G}Developer: {W}Sakraton{C}               ║
║                                          ║
╚══════════════════════════════════════════╝{RESET}
""")

def ask(text, default=""):
if default:
value = input(f"{C}{text}{W} [{default}]: {RESET}").strip()
return value or default
return input(f"{C}{text}: {RESET}").strip()

def save_config(name, data, uri):
safe = "".join(c for c in name if c.isalnum() or c in "-_ ").strip()
if not safe:
safe = "config"
filename = CONFIG_DIR / f"{safe}.json"

data["_share_link"] = uri  
data["_created_at"] = datetime.now().isoformat(timespec="seconds")  

filename.write_text(  
    json.dumps(data, indent=2, ensure_ascii=False),  
    encoding="utf-8"  
)  

return filename

def transport():
print(f"""
{Y}1){W} TCP
{Y}2){W} WebSocket
{Y}3){W} gRPC
""")
choice = ask("Transport", "1")

if choice == "2":  
    return "ws"  
if choice == "3":  
    return "grpc"  
return "tcp"

def create_vless():
print(f"\n{M}--- VLESS ---{RESET}")

name = ask("Config name", "Sakraton-VLESS")  
address = ask("Server address")  
port = ask("Port", "443")  
client_id = ask("UUID", str(uuid.uuid4()))  

net = transport()  
security = ask("Security", "tls")  

params = {  
    "encryption": "none",  
    "security": security,  
    "type": net  
}  

sni = ""  
host = ""  
path = ""  

if security == "tls":  
    sni = ask("SNI", address)  
    params["sni"] = sni  

if net == "ws":  
    path = ask("WebSocket path", "/")  
    host = ask("WebSocket Host", address)  
    params["host"] = host  
    params["path"] = path  

elif net == "grpc":  
    service = ask("gRPC service name", "grpc")  
    params["serviceName"] = service  

query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)  
uri = f"vless://{client_id}@{address}:{port}?{query}#{urllib.parse.quote(name)}"  

data = {  
    "protocol": "vless",  
    "name": name,  
    "address": address,  
    "port": int(port),  
    "id": client_id,  
    "network": net,  
    "security": security  
}  

if sni:  
    data["sni"] = sni  
if host:  
    data["host"] = host  
if path:  
    data["path"] = path  

file = save_config(name, data, uri)  

print(f"\n{G}✓ VLESS config created!{RESET}")  
print(f"{Y}Share Link:{RESET}\n{W}{uri}{RESET}")  
print(f"\n{C}Saved:{RESET} {file}")

def create_vmess():
print(f"\n{M}--- VMESS ---{RESET}")

name = ask("Config name", "Sakraton-VMESS")  
address = ask("Server address")  
port = ask("Port", "443")  
client_id = ask("UUID", str(uuid.uuid4()))  
net = transport()  
tls = ask("TLS", "tls")  

host = ""  
path = ""  

if net == "ws":  
    path = ask("WebSocket path", "/")  
    host = ask("WebSocket Host", address)  

vmess = {  
    "v": "2",  
    "ps": name,  
    "add": address,  
    "port": str(port),  
    "id": client_id,  
    "aid": "0",  
    "scy": "auto",  
    "net": net,  
    "type": "none",  
    "host": host,  
    "path": path,  
    "tls": tls  
}  

raw = json.dumps(vmess, separators=(",", ":"))  
encoded = base64.b64encode(raw.encode()).decode()  
uri = f"vmess://{encoded}"  

data = {  
    "protocol": "vmess",  
    "name": name,  
    "config": vmess  
}  

file = save_config(name, data, uri)  

print(f"\n{G}✓ VMESS config created!{RESET}")  
print(f"{Y}Share Link:{RESET}\n{W}{uri}{RESET}")  
print(f"\n{C}Saved:{RESET} {file}")

def create_trojan():
print(f"\n{M}--- TROJAN ---{RESET}")

name = ask("Config name", "Sakraton-Trojan")  
address = ask("Server address")  
port = ask("Port", "443")  
password = ask("Password")  
security = ask("Security", "tls")  
net = transport()  

params = {  
    "security": security,  
    "type": net  
}  

if security == "tls":  
    params["sni"] = ask("SNI", address)  

if net == "ws":  
    params["host"] = ask("WebSocket Host", address)  
    params["path"] = ask("WebSocket path", "/")  

elif net == "grpc":  
    params["serviceName"] = ask("gRPC service name", "grpc")  

query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)  
uri = f"trojan://{urllib.parse.quote(password)}@{address}:{port}?{query}#{urllib.parse.quote(name)}"  

data = {  
    "protocol": "trojan",  
    "name": name,  
    "address": address,  
    "port": int(port),  
    "network": net,  
    "security": security  
}  

file = save_config(name, data, uri)  

print(f"\n{G}✓ Trojan config created!{RESET}")  
print(f"{Y}Share Link:{RESET}\n{W}{uri}{RESET}")  
print(f"\n{C}Saved:{RESET} {file}")

def list_configs():
files = list(CONFIG_DIR.glob("*.json"))

if not files:  
    print(f"\n{Y}No configs saved.{RESET}")  
    return  

print(f"\n{C}{BOLD}Saved Configs:{RESET}\n")  

for i, file in enumerate(files, 1):  
    print(f"{G}{i}){W} {file.name}")

def delete_config():
files = list(CONFIG_DIR.glob("*.json"))

if not files:  
    print(f"\n{Y}No configs to delete.{RESET}")  
    return  

list_configs()  

choice = ask("Select number")  
try:  
    index = int(choice) - 1  
    file = files[index]  
    file.unlink()  
    print(f"{G}✓ Deleted: {file.name}{RESET}")  
except (ValueError, IndexError):  
    print(f"{R}Invalid selection.{RESET}")

def menu():
while True:
banner()

print(f"""

{G}1){W} Create VLESS
{G}2){W} Create VMESS
{G}3){W} Create Trojan
{G}4){W} List configs
{G}5){W} Delete config
{R}0){W} Exit
""")

choice = input(f"{Y}Sakraton@ConfigMaker > {W}").strip()  

    try:  
        if choice == "1":  
            create_vless()  
        elif choice == "2":  
            create_vmess()  
        elif choice == "3":  
            create_trojan()  
        elif choice == "4":  
            list_configs()  
        elif choice == "5":  
            delete_config()  
        elif choice == "0":  
            print(f"\n{G}Goodbye 👋{RESET}")  
            break  
        else:  
            print(f"{R}Invalid option.{RESET}")  
    except KeyboardInterrupt:  
        print(f"\n{Y}Cancelled.{RESET}")  
    except Exception as e:  
        print(f"\n{R}Error: {e}{RESET}")  

    input(f"\n{C}Press Enter to continue...{RESET}")

if name == "main":
menu()
