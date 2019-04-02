'''
Created on Mar 8, 2019

@author: Ambrish.Ambekar
'''
from OpenSSL import crypto
# Enter certificate file name and password in XXXX and YYYYY respectively
p12= crypto.load_pkcs12(file("C:\\Certificates\\XXXX.pfx", 'rb').read(),"YYYY")
# PEM formatted private key
pemfile= crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())
with open("C:\\Certificates\\key.pem", "w") as text_file:
                                text_file.write(format(pemfile))

# PEM formatted certificate
certfile = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())
with open("C:\\Certificates\\key.pem", "a+") as text_file:
                                text_file.write(format(certfile))
