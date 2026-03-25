import subprocess

def get_interfaces(ip, community):
    try:
        cmd = [
            "snmpwalk",
            "-v2c",
            "-c", community,
            ip,
            "1.3.6.1.2.1.31.1.1.1.1"
        ]

        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode()

        interfaces = []

        for line in output.splitlines():
            if "=" not in line:
                continue

            value = line.split("=", 1)[1].strip()

            if ":" in value:
                value = value.split(":", 1)[1].strip()

            if value:
                interfaces.append({
                    "name": value,
                    "description": value,
                    "status": "unknown"
                })

        print(f"[SNMP] Interfaces found: {len(interfaces)}")

        return interfaces

    except Exception as e:
        print("[SNMP ERROR]", str(e))
        return []
