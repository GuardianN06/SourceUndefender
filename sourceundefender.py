from pathlib import Path
import os, sys
import time
from colorama import init as clinit
from base64 import b85decode
from base64 import a85decode

import hashlib
import zlib
from tgcrypto import ctr256_decrypt
import msgpack
import marshal
import struct
from importlib.util import MAGIC_NUMBER
import random

def clear_console():
    os.system("cls" if os.name == 'nt' else "clear")
    
    
def random_color():
    return f"\033[1;3{random.randint(1, 7)}m"


class Unprotect:
    def __init__(self, pye_file: str | Path, key_hex: str, iv_hex: str, ciphertext_hex: str):
        self.key = bytes.fromhex(key_hex)
        self.iv = bytes.fromhex(iv_hex)
        self.ciphertext = bytes.fromhex(ciphertext_hex.replace("\n", "").replace(" ", ""))
        self.state = b"\x00"
        self.out_file = pye_file

    def verify_and_unmarshal(self, code_object_data: any):
        # Optional: verify it's a code object
        # code_obj = marshal.loads(code_object_data)
        
        # print(f"[ + ] Successfully loaded code object: {code_obj}")
        
        magic = MAGIC_NUMBER  
        flags = b'\x00\x00\x00\x00'
        timestamp = struct.pack('<I', int(time.time()))
        source_size = struct.pack('<I', 0)
        
        header = magic + flags + timestamp + source_size

        with open(self.out_file + ".pyc", "wb+") as f:
            f.write(header + code_object_data)
            
        print(f"[ + ] Exported pyc {self.out_file + '.pyc'}")

        

    # Main function
    def unprotect(self):
        plaintext = ctr256_decrypt(self.ciphertext, self.key, self.iv, self.state)
        # print(plaintext.hex())
        msg = msgpack.unpackb(plaintext)
        # for obj in msg:
        #     print(obj)
        data = msg.get(b'original_code') or msg.get('original_code') or msg.get('code') or msg.get(b'code') # STRING IF IT WAS OBFUCATED WITH FREE VERSION OF SOURCEDEFENDER CODE OBJECT IF PAID
        if isinstance(data, str):
            # FREE VERSION OF SOURCEDEFENDER
            print(f"""
            ---------------- [ SourceDefender Decrypt Info ] ----------------
            -> Product: FREE
            -> Key (HEX): {self.key.hex().upper()}
            -> IV (HEX): {self.iv.hex().upper()}
            -> CipherText length: {len(self.ciphertext.hex())}
            -> State (default) (HEX): {self.state.hex().upper()}
            -----------------------------------------------------------------
            """)
            with open(self.out_file + ".py", "w+", encoding='utf-8') as writer:
                writer.write(data)
                if debug == True:
                    print("            -> Decrypted Data: ")
                    print(msg)
                writer.close()
            print(f"[ + ] Source code written to {self.out_file + '.py'}")
                
        else:
            print(f"""
            ---------------- [ SourceDefender Decrypt Info ] ----------------
            -> Product: Bytecode
            -> Key (HEX): {self.key.hex().upper()}
            -> IV (HEX): {self.iv.hex().upper()}
            -> CipherText length: {len(self.ciphertext.hex())}
            -> State (default) (HEX): {self.state.hex().upper()}
            -----------------------------------------------------------------
            """)
            # PAID VERSION OF SOURCEDEFENDER
            if debug == True:
                print("            -> Decrypted Data: ")
                print(msg)
            self.verify_and_unmarshal(data)

class PYE_Processor:
    def __init__(self, pye_file: str | Path):
        self.fs = open(pye_file, "r+")
        self.lines = self.fs.readlines()
    
    def get_iv(self) -> str:
        return b85dectohex( self.lines[1] ) # First line is IV

    def get_ciphertext(self) -> str: # The rest is CipherText
        return b85dectohex( ''.join(self.lines[2 : len(self.lines) - 1]) )


clinit(autoreset=True)

def b85dectohex(text: str):
    prepared = text.replace("\n", "").replace(" ", "")
    try:
        result = b85decode(prepared).hex().upper()
    except Exception as e:
        # print(f"error: {e}, maybe zlib..")
        result = zlib.decompress(a85decode(prepared)).hex().upper()

    return result


def unprotect_sourcedefender_file(pye_file: str | Path, key_hex: str):
    pye = PYE_Processor(pye_file)
    iv_hex = pye.get_iv()
    ciphertext_hex = pye.get_ciphertext()
    
    unprotect_module = Unprotect(pye_file, key_hex, iv_hex, ciphertext_hex)
    unprotect_module.unprotect()

def derive_aes_key(password, presalt):
    key = hashlib.blake2b(password, digest_size=64).digest()
    salt = hashlib.blake2b(presalt, digest_size=16).digest()
    return hashlib.blake2b(key=key, salt=salt, digest_size=32).hexdigest()

def printascii():
    print(f'''
                {random_color()}╔══════════════════════════════════════════════════════════════════════════════════╗
                {random_color()}║                                                                                  ║
                {random_color()}║                                 ╔═╗╔═╗╦ ╦╦═╗╔═╗╔═╗                               ║
                {random_color()}║                                 ╚═╗║ ║║ ║╠╦╝║  ║╣                                ║
                {random_color()}║                                 ╚═╝╚═╝╚═╝╩╚═╚═╝╚═╝                               ║
                {random_color()}║                            ╦ ╦╔╗╔╔╦╗╔═╗╔═╗╔═╗╔╗╔╔╦╗╔═╗╦═╗                        ║
                {random_color()}║                            ║ ║║║║ ║║║╣ ╠╣ ║╣ ║║║ ║║║╣ ╠╦╝                        ║
                {random_color()}║                            ╚═╝╝╚╝═╩╝╚═╝╚  ╚═╝╝╚╝═╩╝╚═╝╩╚═                        ║
                {random_color()}║                                                                                  ║
                {random_color()}║                       {random_color()}Developed By: {random_color()}GuardianN06{random_color()} and {random_color()}vxnetrip {random_color()}                    ║
                {random_color()}║                       {random_color()}Telegram: {random_color()}@vxripdev {random_color()}Channel: {random_color()}@vxnetrip                     ║
                {random_color()}╚══════════════════════════════════════════════════════════════════════════════════╝
            ''')

if __name__ == "__main__":
    try:
        debug = False # switch to True to print all sourcedefender options like ttl_info, check_ntp, debug, eol_timestamp
        clear_console()
        printascii()

        if len(sys.argv) > 1:
            file_path = sys.argv[1]
        else:
            while True:
                file_path = input(f"       {random_color()}══> {random_color()}Enter PYE file path: ").strip()
                if os.path.exists(file_path):
                    break
                print(f"       {random_color()}File does not exist ;/")
                time.sleep(2)
                clear_console()

        if not os.path.exists(file_path):
            print(f"       {random_color()}File does not exist: {file_path}")
            sys.exit(1)

        base_name = os.path.splitext(os.path.basename(file_path))[0].encode()

        password = input(f"                {random_color()}Enter password (leave empty to use base password): ").strip()
        salt = input(f"                {random_color()}Enter salt (leave empty to use base salt): ").strip()

        password_bytes = password.encode() if password else base_name
        salt_bytes = salt.encode() if salt else base_name

        key_hex = derive_aes_key(password_bytes, salt_bytes)
        unprotect_sourcedefender_file(file_path, key_hex)

        input("\nPress any key to exit.")
        sys.exit(0)

    except KeyboardInterrupt:
        clear_console()
        sys.exit(0)
