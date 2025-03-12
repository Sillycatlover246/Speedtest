import speedtest
import json
import os
from datetime import datetime

RECORD_FILE = "speed_records.json"

def test_internet_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    
    download_speed = st.download()
    upload_speed = st.upload()

    download_mbps = download_speed / 1_000_000
    upload_mbps = upload_speed / 1_000_000

    ping_result = st.results.ping

    return download_mbps, upload_mbps, ping_result

def load_records(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    else:
        return []

def save_record(record, filename):
    records = load_records(filename)
    records.append(record)
    with open(filename, "w") as f:
        json.dump(records, f, indent=4)

def main():
    download, upload, ping = test_internet_speed()

    download = round(download)
    upload = round(upload)
    ping = round(ping)
    
    print(f"Download speed: {download} Mbps")
    print(f"Upload speed: {upload} Mbps")
    print(f"Ping: {ping} ms")

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # image being american and doing %m %d %y or whatever they do
        "download_mbps": download,
        "upload_mbps": upload,
        "ping_ms": ping
    }
    
    save_record(record, RECORD_FILE)
    print(f"Record saved to {RECORD_FILE}")

if __name__ == "__main__":
    main()
