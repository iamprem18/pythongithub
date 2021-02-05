import ssl
from datetime import datetime
import OpenSSL
import socket
import getpass
from datetime import timedelta
from flask import Flask,render_template

app = Flask(__name__) 
cur_date = datetime.utcnow()

ssl_dict={}
ssl_list= list()

ipfile=open('/pythongithub/server_ip.txt')	
@app.route('/')
def file():
	for ip in ipfile:
		try:
			host = ip.strip().split(":")[0]
			port = ip.strip().split(":")[1]
			ctx = OpenSSL.SSL.Context(ssl.PROTOCOL_TLSv1)
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((host, int(port)))
			cnx = OpenSSL.SSL.Connection(ctx, s)
			cnx.set_connect_state()
			cnx.do_handshake()
			cert=cnx.get_peer_certificate()
			s.close()
			server_name = cert.get_subject().commonName
			edate=cert.get_notAfter()
			edate=edate.decode()
			exp_date = datetime.strptime(edate,'%Y%m%d%H%M%SZ')
			exp = datetime.strftime(exp_date,'%d %B, %Y')
			days_to_expire = int((exp_date - cur_date).days)
			ssl_dict={'Name': host,'Date': exp,'Days': days_to_expire}
			ssl_list.append(ssl_dict)
		except:
			return ("Error on connection to server")
	return render_template("index.html",ssl_list=ssl_list)

@app.route('/<message>') 
def domainParameter(message):
	try:
		host = message.strip().split(":")[0]
		port = message.strip().split(":")[1]
		#Declare empty dictionary and list
		ssl_dict={}
		ssl_list= list()	
		ctx = OpenSSL.SSL.Context(ssl.PROTOCOL_TLSv1)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, int(port)))
		cnx = OpenSSL.SSL.Connection(ctx, s)
		cnx.set_connect_state()
		cnx.do_handshake()
		cert=cnx.get_peer_certificate()
		s.close()
		server_name = cert.get_subject().commonName
		edate=cert.get_notAfter()
		edate=edate.decode()
		exp_date = datetime.strptime(edate,'%Y%m%d%H%M%SZ')
		exp = datetime.strftime(exp_date,'%d %B, %Y')
		days_to_expire = int((exp_date - cur_date).days)
		ssl_dict={'Name': host,'Date': exp,'Days': days_to_expire}
		ssl_list.append(ssl_dict)
		return render_template("index.html",ssl_list=ssl_list)
	except:
		return ("Error on connection to server")

if __name__ == '__main__': 
   app.run(host='0.0.0.0', port=7000, debug=True) 