from flask import Flask, render_template
import webbrowser
import socket
# import subprocess

class PageDisplayer:
    app = Flask(__name__)
    port = 5000
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_ip_address():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address

    @staticmethod
    def open_url_in_chromium(url, kiosk=True, maximized=True):
        options = "--kiosk" if kiosk else ""
        options += " --start-maximized" if maximized else ""
        options += " --enable-chrome-browser-cloud-management" if maximized else ""
        webbrowser.get(f'/usr/bin/chromium-browser {options} %s').open_new_tab(url)

    
    @app.route('/')
    def home():
        return render_template('index.html')

    @staticmethod
    def run():
        # Autoriser le port 5000 dans le pare-feu
        # subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--dport", str(PageDisplayer.port), "-j", "ACCEPT"])
        
        ip_address = PageDisplayer.get_ip_address()
        url = f"http://{ip_address}:{PageDisplayer.port}"
        PageDisplayer.open_url_in_chromium(url, kiosk=True, maximized=True)
        PageDisplayer.app.run(host='0.0.0.0', port=PageDisplayer.port, debug=True)



PageDisplayer.run()
