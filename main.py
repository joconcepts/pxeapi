from flask import Flask, render_template, request, send_from_directory
import os.path
import dns.resolver, dns.reversename

app = Flask(__name__)

nextboot_entries = {}

@app.route("/autoinstall/<filename>")
def index(filename):
    if not os.path.isfile("templates/"+filename):
        abort(404)

    ip = request.remote_addr
    try:
        raddrs = dns.reversename.from_address(ip)
        hostname = str(dns.resolver.resolve(raddrs, "PTR")[0])
    except:
        hostname = "empty"
    return render_template(filename, hostname=hostname)

@app.route("/nextboot", methods=['POST'])
def nextboot():
    ip = request.args.get('ip')
    nextboot = request.args.get('nextboot')
    nextboot_entries[ip] = nextboot
    return 'set {} for {}'.format(nextboot, ip)

@app.route("/ipxe")
def ipxe():
    ip = request.remote_addr
    nextboot = None
    if nextboot_entries.get(ip):
        nextboot = nextboot_entries.pop(ip)

    return render_template("ipxe_menu.txt", nextboot=nextboot)

@app.route("/pxeboot/<path:name>")
def pxeboot(name):
    return send_from_directory("/srv/storage/pxeboot", name, as_attachment=True)
