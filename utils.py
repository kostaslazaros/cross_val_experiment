"""Varius utilities for the project"""
import requests
import parameters as prm


def notify(msg: str, okv=True):
    """Push notifications using ntfy.com"""
    if okv:
        mes = f"🚀 {msg}".encode(encoding="utf-8")
    else:
        mes = f"❌ {msg}".encode(encoding="utf-8")
    url = f"https://ntfy.sh/{prm.NOTIFY_CHANNEL}"
    requests.post(url, data=mes, timeout=10)


def msg(message: str, okv=True, toall=False):
    """Messaging system"""
    if okv:
        print(f"[INFO] {message}")
    else:
        print(f"[ERROR] {message}")

    if toall:
        notify(message, okv)


def show_parameters():
    """Parameters as text for logging"""
    txt = (
        f"DATA_PATH = {prm.DATA_PATH} \n"
        f"SAVE_PATH = {prm.SAVE_PATH} \n"
        f"KEEP_FIRST_FEATURES = {prm.KEEP_FIRST_FEATURES} \n"
        f"REPEATS = {prm.REPEATS} \n"
        f"FOLDS = {prm.FOLDS} \n"
        f"ROUND_DECIMALS = {prm.ROUND_DECIMALS} \n"
        f"F1_AVERAGE = {prm.F1_AVERAGE} \n"
        f"NOTIFY_CHANNEL = {prm.NOTIFY_CHANNEL} \n"
    )
    return txt
