import re
from sys import argv

import dpkt


def get_pcap_file():
    pcap_file = argv[1] if len(argv) > 1 else ""

    if not pcap_file:
        from tkinter.filedialog import askopenfilename
        pcap_file = askopenfilename(
            defaultextension="pcap", filetypes=[("Pcap", ".pcap")])

    # User cancellation
    if not pcap_file:
        exit(0)

    return pcap_file


def extract_urls(pcap_file: str):
    urls = {}

    with open(pcap_file, "rb") as f:
        pcap = dpkt.pcap.Reader(f)
        rtmp_url_re = b"rtmp://.*/live"
        token_re = rb"\d+\?token=[\w\d]+&t=\d+"

        base = None
        for t, buf in pcap:
            if b"rtmp://" in buf:
                r = re.search(rtmp_url_re, buf)
                base = f"{r.group().decode("ascii")}"
            if b"FCSubscribe" in buf:
                r = re.search(token_re, buf)
                if r is not None and base is not None:
                    auth = r.group().decode("ascii")
                    url = f"{base}/{auth}"
                    room, _ = auth.split("?")
                    urls[room] = url
                    base = None

    result = "\n".join(urls.values())
    with open("urls.txt", "w", encoding="utf-8") as f:
        f.write(result)


def main():
    pcap_file = get_pcap_file()
    extract_urls(pcap_file=pcap_file)
