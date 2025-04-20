import socket

def scan_ports(target):
    open_ports = []
    for port in range(1, 2000):  # You can increase this range
        try:
            s = socket.socket()
            s.settimeout(0.5)
            s.connect((target, port))
            open_ports.append(port)
            s.close()
        except:
            continue
    return open_ports


import openai
# enter your api here 
openai.api_key = "YOUR_API_KEY"

def analyze_with_ai(target, open_ports):
    ports_str = ", ".join(map(str, open_ports))
    prompt = f"""
    I scanned {target} and found these open ports: {ports_str}.
    Can you analyze possible vulnerabilities or services running on these ports?
    Filter the results by risk level and explain each one.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def run_cipher_recon(target):
    print(f"[+] Scanning target: {target}")
    ports = scan_ports(target)
    if ports:
        print(f"[+] Open ports found: {ports}")
        print("[+] Analyzing with Cipher AI...")
        analysis = analyze_with_ai(target, ports)
        print(f"\n[AI Report for {target}]:\n{analysis}")
    else:
        print("[-] No open ports found.")

# Example usage
# change this Example.com to you site 
run_cipher_recon("Example.com")
