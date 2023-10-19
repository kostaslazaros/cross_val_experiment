import requests


def notify(msg: str, channel: str, okv=True):
    """Push notifications using ntfy.com"""
    if okv:
        mes = f"🚀 {msg}".encode(encoding="utf-8")
    else:
        mes = f"❌ {msg}".encode(encoding="utf-8")
    url = f"https://ntfy.sh/{channel}"
    requests.post(url, data=mes, timeout=10)


if __name__ == "__main__":
    notify("wake up you fool ...", "lamia-box", True)
