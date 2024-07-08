import os
import json
import platform
import subprocess
import shutil

def get_ip_address():
    ip = ""
    try:
        if platform.system() == "Linux":
            ip = subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
        elif platform.system() == "Darwin":  # macOS
            ip = subprocess.check_output(["ipconfig", "getifaddr", "en0"]).decode().strip()
            if not ip:
                ip = subprocess.check_output(["ipconfig", "getifaddr", "en1"]).decode().strip()
        elif platform.system() == "Windows":
            ip = subprocess.check_output(
                "ipconfig | findstr /i \"IPv4 Address\"", shell=True
            ).decode().strip().split(":")[-1].strip()
    except Exception as e:
        print(f"Error getting IP address: {e}")
    return ip

def update_config(config_path):
    config_dir = os.path.dirname(config_path)
    template_json_path = os.path.join(config_dir, "config.template.json")

    if not os.path.exists(config_path):
        if os.path.exists(template_json_path):
            shutil.copy(template_json_path, config_path)
            print(f"config.json did not exist. Copied config.template.json to config.json.")
        else:
            raise FileNotFoundError(f"Both {config_path} and {template_json_path} are missing. "
                                    "Please ensure one of these files exists.")

    with open(config_path, 'r') as file:
        config = json.load(file)
    
    ip_address = get_ip_address()
    print(f"Detected IP address: {ip_address}")
    
    if ip_address:
        custom_config = {"ip": ip_address, "port": 3000}
        config["CUSTOM"] = custom_config
        
        with open(config_path, 'w') as file:
            json.dump(config, file, indent=4)
        
        print("IP address and port added to config.json.")
    else:
        print("Unable to determine IP address. CUSTOM section not added to config.json.")

def main():
    if "SMARTPHONE_ROBOT_CONFIG_PATH" in os.environ:
        config_dir = os.environ["SMARTPHONE_ROBOT_CONFIG_PATH"]
        config_path = os.path.join(config_dir, "config.json")
    else:
        print(
        """
        SMARTPHONE_ROBOT_CONFIG_PATH is not set.
        This environmental variable should be set to a local copy of
        https://github.com/oist/smartphone-robot-android as a means
        to tie the android client to the python server. If this is
        the first time you are trying to set this up, please either
        download or clone that repo, and set the
        SMARTPHONE_ROBOT_CONFIG_PATH to the path of the
        the local repo
        """
        )
        exit(1)

    if not os.path.exists(config_dir):
        raise FileNotFoundError(f"The directory {config_dir} does not exist.")
    else:
        update_config(config_path)

if __name__ == "__main__":
    main()
