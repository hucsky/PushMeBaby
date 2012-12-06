"""
Apple Push Notification Sample
"""
#haizi rTFHLUgjb7gWZN5LLdSDqX0KyCK0iMIbYE4jM67Xks0=
#Chuan iPod R19yjScgfmWJ5axNylSBy/zZDGw/C2CVhb0zTrd7zCY=

token_dict = {"chuan_ipod":"R19yjScgfmWJ5axNylSBy/zZDGw/C2CVhb0zTrd7zCY=",
              "haizi":"rTFHLUgjb7gWZN5LLdSDqX0KyCK0iMIbYE4jM67Xks0="}

class AppNotifyer:
    def __init__(self, cert=None, token=None):
        self.sock = None
        self.certfile = cert
        self.token = token
    
    def _payload(self, alert, badge=None, sound=None):
        msg = {"alert":alert}
        if badge is not None:
            msg["badge"] = badge
        if sound is not None:
            msg["sound"] = sound
        payload = {"aps":msg}
        import json
        print json.dumps(payload, indent=4)
        return json.dumps(payload, indent=4)
    
    def sendMessage(self, alert, badge=None, sound=None, token=None):
        if self.sock is None:
            return
        payload = self._payload(alert, badge, sound)
        import base64
        if token is not None:
            tokenData = base64.decodestring(token)
        else:
            tokenData = base64.decodestring(self.token)
        fmt = ('!bH%dsH%ds')%(len(tokenData), len(payload))
        import struct
        msg = struct.pack(fmt, 0, len(tokenData), tokenData, len(payload), payload)
        self.sock.write(msg)
        pass
    
    def connetWithDev(self):
        if self.certfile is None:
            self.sock = None
            return
        import socket, ssl
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = ssl.wrap_socket(s, 
                                        certfile = self.certfile, 
                                        ssl_version = ssl.PROTOCOL_TLSv1)
            self.sock.connect(("gateway.sandbox.push.apple.com", 2195))
        except ssl.SSLError as err:
            print err
            self.sock =None
    
    def connectWithProd(self):
        if self.certfile is None:
            self.sock = None
            return
        import socket, ssl
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = ssl.wrap_socket(s, 
                                        certfile = self.certfile, 
                                        ssl_version = ssl.PROTOCOL_TLSv1)
            self.sock.connect(("gateway.push.apple.com", 2195))
        except ssl.SSLError as err:
            print err
            self.sock =None

if __name__ == "__main__":
    try:
        notifyer = AppNotifyer()
        notifyer.certfile = "/Users/quanzhen/Documents/Push/guillotine.pem"
        notifyer.token = token_dict["chuan_ipod"]
        notifyer.connetWithDev()
        notifyer.sendMessage("Hello Baby", 20, "default")
    except:
        import sys
        print sys.exc_info()