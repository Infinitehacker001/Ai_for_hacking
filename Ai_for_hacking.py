import socket
import os
import openai

# Load OpenAI API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this in your environment

def scan_ports(target):
    open_ports = []
    for port in range(1, 2000):  # You can increase this range
        try:
            with socket.socket() as s:
                s.settimeout(0.5)
                s.connect((target, port))
                open_ports.append(port)
        except:
            continue
    return open_ports

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
    print(f"\n[+] Scanning target: {target}")
    ports = scan_ports(target)
    
    if ports:
        print(f"\n[+] Open ports found on {target}:")
        for port in ports:
            print(f"    - Port {port}")
        print("\n[+] Analyzing with Cipher AI...")
        analysis = analyze_with_ai(target, ports)
        print(f"\n[AI Report for {target}]:\n{analysis}")
    else:
        print("[-] No open ports found.")

if __name__ == "__main__":
    target = input("Enter the target domain or IP: ")
    run_cipher_recon(target)
