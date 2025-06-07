import requests
import sqlite3

def connect_db():
    return sqlite3.connect("Cookies.db")

def retrieve_domains():
    conn = connect_db()
    cur = conn.cursor()

    domains = cur.execute("SELECT host_key FROM cookies").fetchall()

    return [domain[0] for domain in domains]

def domain_frequency(domains: list[str]):
    freq = {}
    for domain in domains:
        if domain not in freq:
            freq[domain] = 1
        else:
            freq[domain] = freq[domain] + 1
    return freq

domains = retrieve_domains()
freq = domain_frequency(domains)
