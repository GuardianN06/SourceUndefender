# SourceUndefender
Python script to decrypt sourcedefender files.

Works on latest version 15.0.12 and some older versions.

Star if you like it :p

For other decryption services join us on our [Discord](https://discord.gg/N9CEjF6ArT)!

# 🧷 Usage
```
python sourceundefender.py
```
# Preview
<div align="center">
  <img src="cli.png" alt="slice" title="slice">
</div>


# 🔑 How Key Derivation Works
```
base_name = os.path.splitext(os.path.basename(file_path))[0].encode()
key = hashlib.blake2b(base_name, digest_size=64).digest()
salt = hashlib.blake2b(base_name, digest_size=16).digest()
aes_key = hashlib.blake2b(key=key, salt=salt, digest_size=32).hexdigest()
```
That’s literally what they use.
Rename the file, and the key breaks, 10/10 security 🥴

# 🔓 How Decryption Works

Takes the above blake2b hash as the AES256 key and takes the first line of the pye file for the IV encoded in base85 or zlib compressed for older versions.
The rest of the cipher is base85 decoded and gets decrypted by the tgcrypto aes256 in CTR mode. This then gets fed into msgpack which loads it and checks for sourcedefender settings.



For educational reasons only, don't steal code that isn't yours :)
