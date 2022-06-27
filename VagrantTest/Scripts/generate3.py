import subprocess as sp
import os
from OpenSSL import crypto
import os
import sys
import datetime

# check if folder "ca-cert" exists
# if not, create it
# if yes, delete it
if os.path.exists("ca-cert"):
    sp.call(["rm", "-rf", "ca-cert"])
sp.call(["mkdir", "ca-cert"])

# 0. create config file
open ("ca-cert/ca.cnf", "w").write(
"""
[req]
default_bits = 2048
prompt = no
default_md = sha256
encrypt_key = no
distinguished_name = dn

[dn]
C = ID
O = Local Digital Cert Authority
OU = www.ca.local
CN = Self-Signed Root CA
"""
)
# 1. generate a root CA certificate and private key
sp.call(['openssl', 'genrsa', '-out', 'ca-cert/ca.key', '2048'])
# 2. generate CSR with config file
sp.call(['openssl', 'req', '-new', '-key', 'ca-cert/ca.key', '-out', 'ca-cert/ca.csr', '-config', 'ca-cert/ca.cnf'])
# 3. create a self-signed CA certificate
validDate = '3650'
sp.call(['openssl', 'x509', '-req', '-days', validDate, '-in', 'ca-cert/ca.csr', '-signkey', 'ca-cert/ca.key', '-out', 'ca-cert/ca.crt'])
print("CA certificate and private key generated")

# check ca-cert/ca.crt and ca-cert/ca.key
if os.path.exists("ca-cert/ca.crt") and os.path.exists("ca-cert/ca.key"):
    print ("CA is ready")
else:
    print("CA is not ready, generate it first")
    print("Run generate-ca.py")
    exit()
path = os.getcwd()
TYPE_RSA = crypto.TYPE_RSA
TYPE_DSA = crypto.TYPE_DSA
HOME = os.getenv("HOME")
now = datetime.datetime.now()
d = now.date()
cn = "assignment.local"
key = crypto.PKey()
keypath = r"newkey.key"
csrpath = r"newcsr.csr"
crtpath = r"crt"

def generatekey():

    if os.path.exists(keypath):
        print("Certificate file exists, aborting.")
        print(keypath)
        sys.exit(1)
    #Else write the key to the keyfile
    else:
        with open(keypath, "w") as file:
            key.generate_key(TYPE_RSA, 4096)
            file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode("utf-8"))


generatekey()

# if sans_list:
    # x509_extensions.append(crypto.X509Extension("subjectAltName".encode('ascii'), False, ['a','s','s','i','g','n','m','e','n','t','.','l','o','c','a','l']))
def generatecsr():
    req = crypto.X509Req()
    req.get_subject().CN = cn
    req.get_subject().C = "US"
    req.get_subject().ST = "IL"
    req.get_subject().L = "telavbiv"
    req.get_subject().O = "CQB"
    req.get_subject().OU = "BYNETDATA"
    req.set_pubkey(key)
    req.sign(key, "sha256")

    with open(csrpath, "w") as file:
        file.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, req).decode("utf-8"))
generatecsr()

# input csr file
csrFile = 'newcsr.csr'


# print csr information
#print("CSR information:")
# csr decoder and return the subject
#csrInfo = sp.check_output(['openssl', 'req', '-in', csrFile, '-noout','-subject'])
#print("".join(csrInfo.decode('utf-8').split("subject=")[1].replace(", ", "\n")))
# validate csr


# input expiration days
validDate = '3650'

# openssl x509 -req -in fabrikam.csr -CA  contoso.crt -CAkey contoso.key -CAcreateserial -out fabrikam.crt -days 365 -sha256
sp.call(['openssl', 'x509', '-req', '-in', csrFile, '-CA', 'ca-cert/ca.crt', '-CAkey', 'ca-cert/ca.key', '-CAcreateserial', '-out', 'server.crt', '-days', validDate, '-sha256'])


