import sys, os
import marshal
import hashlib
import threading
from . import pkcrypt

def protected():
    passw = 'qwerty123'
    if input('pass: ') == passw:
        input('OK!')

def loader(funcenc: bytes, path: str, key: bytes):
    if len([thread.name for thread in threading.enumerate()]) > 1:print('thread',[thread.name for thread in threading.enumerate()]);sys.exit(1)
    if not 'chash' in __import__('builtins').globals().keys():chash=getattr(hashlib,pkcrypt.xor(b'\\VD',b'12qq').decode())(open(path,'rb').read()).hexdigest()
    if getattr(hashlib,pkcrypt.xor(b'\\VD',b'12qq').decode())(open(path,'rb').read()).hexdigest()!=chash:print('hash');sys.exit(1)
    globals,locals,exec,eval=None,None,None,None
    pglobals={'exec':None,'eval':None,'globals':None,'locals':None,'chash':chash}
    getattr(__import__(pkcrypt.xor(b'SGZ\x1c\x1b\x00_A',b'123poi123hghjfhgf').decode()),pkcrypt.xor(b'TJV\x13',b'123poi123hghjfhgf').decode())(marshal.loads(getattr(pkcrypt,'rox'[::-1])(funcenc,getattr(pkcrypt,'rox'[::-1])(pkcrypt.l1l1l1l1l1l1l1l1l1l1l1l1l11111111,key))),pglobals)


def _protect(code: str):
    testobf = marshal.dumps(compile(code, '<string>', 'exec'));nb = os.urandom(32)
    testobf = getattr(pkcrypt, 'rox'[::-1])(testobf, getattr(pkcrypt, 'rox'[::-1])(pkcrypt.l1l1l1l1l1l1l1l1l1l1l1l1l11111111,nb))
    return (f"__import__('paketlib').protect.loader({testobf}, __import__('os').path.abspath(__file__), {nb})")

def protect(code: str):
    for _ in range(3):obf=_protect(code)
    return obf