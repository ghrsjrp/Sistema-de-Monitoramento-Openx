import subprocess

def snmp_walk(ip, community, oid):
    try:
        cmd = [
            "snmpwalk",
            "-v2c",
            "-c", community,
            ip,
            oid
        ]

        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode()
        return output.splitlines()

    except Exception as e:
        print("[LLDP ERROR]", str(e))
        return []


def get_lldp_neighbors(ip, community):
    oid_sysname = "1.0.8802.1.1.2.1.4.1.1.9"
    oid_portid  = "1.0.8802.1.1.2.1.4.1.1.7"
    oid_local   = "1.0.8802.1.1.2.1.3.7.1.3"

    sysnames = snmp_walk(ip, community, oid_sysname)
    ports    = snmp_walk(ip, community, oid_portid)
    locals   = snmp_walk(ip, community, oid_local)

    neighbors = []

    for i in range(min(len(sysnames), len(ports))):
        try:
            remote_device = sysnames[i].split("=", 1)[1].split(":",1)[1].strip()
            remote_port   = ports[i].split("=", 1)[1].split(":",1)[1].strip()
            local_port    = locals[i].split("=", 1)[1].split(":",1)[1].strip()

            neighbors.append({
                "local_port": local_port,
                "remote_device": remote_device,
                "remote_port": remote_port
            })

        except:
            continue

    print(f"[LLDP] neighbors found: {len(neighbors)}")

    return neighbors
