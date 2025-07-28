import argparse
from utils.entropy import calculate_entropy
from zxcvbn import zxcvbn
import hashlib
import requests

def check_hibp(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    res = requests.get(url)
    hashes = (line.split(':') for line in res.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)
    return 0

def main():
    parser = argparse.ArgumentParser(description="Password Strength Checker")
    parser.add_argument('--password', required=True, help='Password to check')
    args = parser.parse_args()
    password = args.password

    print(f"\n🔐 Checking password: {password}\n")

    entropy = calculate_entropy(password)
    print(f"🧠 Entropy: {entropy:.2f} bits")

    strength = zxcvbn(password)
    score = strength['score']
    feedback = [
        "🟥 Very weak",
        "🟧 Weak",
        "🟨 Moderate",
        "🟩 Strong",
        "🟦 Very strong"
    ]
    print(f"📊 Strength: {feedback[score]}")

    breaches = check_hibp(password)
    if breaches:
        print(f"❌ Found in {breaches} breaches!")
    else:
        print("✅ Not found in known breaches.")

if __name__ == '__main__':
    main()
