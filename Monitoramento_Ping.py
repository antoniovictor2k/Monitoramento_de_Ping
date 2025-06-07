import subprocess
import platform
import re
import time
import pyttsx3
from colorama import init, Fore

init(autoreset=True)

inicial_voz_ativa = pyttsx3.init()
inicial_voz_ativa.setProperty("rate", 175)
inicial_voz_ativa.setProperty("volume", 1)

def obter_comando_ping(host: str) -> list:
    """Retorna o comando de ping apropriado para o sistema operacional."""
    sistema = platform.system().lower()
    if sistema == 'windows':
        return ['ping', host, '-n', '1']
    return ['ping', '-c', '1', host]

def extrair_latencia(saida: str) -> float | None:
    """Extrai o valor da latência (em ms) da saída do comando ping."""
    sistema = platform.system().lower()
    if sistema == 'windows':
        padrao = r'(Tempo|Time)[=<]?\s*([\d,\.]+)\s*ms'
        match = re.search(padrao, saida, re.IGNORECASE)
    else:
        padrao = r'time[=<]?\s*([\d\.]+)\s*ms'
        match = re.search(padrao, saida)
    if match:
        valor = match.group(2 if sistema == 'windows' else 1).replace(',', '.')
        try:
            return float(valor)
        except ValueError:
            return None
    return None

def houve_perda(saida: str) -> bool:
    """Verifica se houve perda de pacote na saída do ping."""
    palavras_chave = [
        "Esgotado", "Request timed out", "100% packet loss",
        "Destination host unreachable", "General failure"
    ]
    if any(palavra in saida for palavra in palavras_chave):
        return True
    # Verifica por "0 received" em linhas de estatísticas
    if re.search(r'(\d+)\s+received', saida, re.IGNORECASE):
        if re.search(r'0\s+received', saida, re.IGNORECASE):
            return True
    return False

def notificar_perda(google, host: str):
    """Exibe e fala mensagem de perda de pacote."""
    print(Fore.RED + f"[PERDA]{google} Sem resposta de {host}")
    inicial_voz_ativa.say("Perda de pacotes detectada!")
    inicial_voz_ativa.runAndWait()

def ping_continuo(host: str = '8.8.8.8') -> None:
    """Executa pings contínuos para o host informado e exibe o resultado."""
    print(Fore.CYAN + f"🔁 Iniciando ping contínuo para {host} (CTRL+C para parar)\n")

    google = " - Google: "

    try:
        while True:
            comando = obter_comando_ping(host)
            resultado = subprocess.run(
                comando,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                timeout=5
            )
            saida = resultado.stdout + resultado.stderr

            if houve_perda(saida):
                notificar_perda(google,host)
            else:
                latencia = extrair_latencia(saida)
                if latencia is not None:
                    cor = Fore.GREEN if latencia < 40 else Fore.YELLOW
                    status = "[OK]" if latencia < 40 else "[ALTO]"
                    print(cor + f"{status}{google} {host} respondeu em {latencia:.1f} ms")
                else:
                    # Trata erro de latência como perda de pacote
                    notificar_perda(google,host)
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.CYAN + "\n⛔ Ping interrompido pelo usuário.")

if __name__ == "__main__":
    ping_continuo('8.8.8.8')
