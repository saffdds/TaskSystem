import psutil
import os
import time
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_task_system():
    message = "" # Per mostrare l'esito del comando
    try:
        while True:
            clear_screen()
            print(f"=== TASK SYSTEM===")
            print(f"Data/Ora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            if message: print(f"[NOTIFICA]: {message}")
            print("-" * 60)
            print(f"{'PID':<8} | {'NOME':<25} | {'RAM (MB)':<10} | {'CPU %':<8}")
            print("-" * 60)

            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
                try:
                    info = proc.info
                    ram = info['memory_info'].rss / (1024 * 1024)
                    processes.append({'pid': info['pid'], 'name': info['name'], 'ram': ram, 'cpu': info['cpu_percent']})
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            top_processes = sorted(processes, key=lambda x: x['ram'], reverse=True)[:15]
            for p in top_processes:
                print(f"{p['pid']:<8} | {p['name'][:25]:<25} | {p['ram']:<10.2f} | {p['cpu']:<8.1f}")

            print("-" * 60)
            print("Comandi: '/kill <PID>' per terminare | 'INVIO' per aggiornare | 'CTRL+C' per uscire")
            
            # Input dell'utente
            cmd = input("\nTaskSystem> ").strip()
            
            if cmd.startswith("/kill "):
                try:
                    pid_to_kill = int(cmd.split(" ")[1])
                    p_kill = psutil.Process(pid_to_kill)
                    name_killed = p_kill.name()
                    p_kill.terminate() # Il colpo di grazia!
                    message = f"Processo {name_killed} ({pid_to_kill}) rimosso dal mondo!"
                except Exception as e:
                    message = f"Errore: Impossibile usare /kill su questo bersaglio! ({e})"
            else:
                message = "" # Pulisce la notifica se non c'è comando

    except KeyboardInterrupt:
        print("\n[!] Task System!")

if __name__ == "__main__":
    run_task_system()