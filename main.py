"""
Lê até 3 contatos do Supabase e envia via Z-API:
"Olá {nome}, tudo bem com você?"
"""

from dotenv import load_dotenv
import os
import time
import requests
from supabase import create_client

# Carrega variáveis do arquivo .env na raiz do projeto
load_dotenv()

# ----- Config do Supabase -----
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
CONTACTS_TABLE = os.getenv("CONTACTS_TABLE", "contacts")
NAME_COL = os.getenv("NAME_COLUMN", "name")
PHONE_COL = os.getenv("PHONE_COLUMN", "phone")

# ----- Config da Z-API -----
ZAPI_INSTANCE = os.getenv("ZAPI_INSTANCE")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")

# Validação mínima
campos_obrigatorios = [
    ("SUPABASE_URL", SUPABASE_URL),
    ("SUPABASE_KEY", SUPABASE_KEY),
    ("ZAPI_INSTANCE", ZAPI_INSTANCE),
    ("ZAPI_TOKEN", ZAPI_TOKEN),
    ("ZAPI_CLIENT_TOKEN", ZAPI_CLIENT_TOKEN),
]
faltando = [k for k, v in campos_obrigatorios if not v]
if faltando:
    raise SystemExit(f"Preencha estas variáveis no .env: {', '.join(faltando)}")

# Cliente Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_contacts(limit=3):
    """Busca até 'limit' contatos da tabela configurada."""
    resp = supabase.table(CONTACTS_TABLE).select(f"{NAME_COL},{PHONE_COL}").limit(limit).execute()
    data = None
    if hasattr(resp, "data"):
        data = resp.data
    elif isinstance(resp, dict) and resp.get("data") is not None:
        data = resp.get("data")
    else:
        data = resp
    return data or []


def format_phone(raw):
    """Mantém apenas dígitos (formato internacional, ex.: 5511999999999)."""
    if raw is None:
        return ""
    return ''.join(ch for ch in str(raw) if ch.isdigit())


def send_message(phone: str, message: str):
    """Envia texto via Z-API."""
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}/send-text"
    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN,
    }
    payload = {
        "phone": phone,
        "message": message,
        "delayMessage": 2,  # opcional: pequena espera entre mensagens
    }
    return requests.post(url, json=payload, headers=headers, timeout=15)


def main():
    contatos = get_contacts(limit=3)
    if not contatos:
        print("Nenhum contato encontrado. Verifique tabela, colunas, RLS e chaves.")
        return

    for c in contatos:
        nome = c.get(NAME_COL)
        telefone_raw = c.get(PHONE_COL)
        telefone = format_phone(telefone_raw)

        if not telefone:
            print(f"Pulando contato sem telefone válido: {nome} / {telefone_raw}")
            continue

        msg = f"Olá {nome}, tudo bem com você?"
        print(f"Enviando para {telefone}: {msg}")
        r = send_message(telefone, msg)

        if r.status_code == 200:
            try:
                print("Enviado", r.json())
            except Exception:
                print("Enviado (sem JSON)")
        else:
            print("Falha ao enviar", r.status_code, r.text)

        time.sleep(2)


if __name__ == "__main__":
    main()