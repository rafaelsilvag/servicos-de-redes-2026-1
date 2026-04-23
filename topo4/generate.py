import os

base_dir = "/home/rafael/Documents/Github/Ifes/administracao-redes-2026/topo4"

# (name, id, {eth_id: (mac_suffix, local_port, remote_port)})
routers = {
    'r1': (1, [('0001', 26011, 26021), ('0002', 26012, 26031), ('0003', 26013, 26001)]),
    'r2': (2, [('0001', 26021, 26011), ('0002', 26022, 26091), ('0003', 26023, 26041)]),
    'r3': (3, [('0001', 26031, 26012), ('0002', 26032, 26042), ('0003', 26033, 26051), ('0004', 26034, 26061)]),
    'r4': (4, [('0001', 26041, 26023), ('0002', 26042, 26032), ('0003', 26043, 26062)]),
    'r5': (5, [('0001', 26051, 26033), ('0002', 26052, 26063), ('0003', 26053, 26002)]),
    'r6': (6, [('0001', 26061, 26034), ('0002', 26062, 26043), ('0003', 26063, 26052), ('0004', 26064, 26081), ('0005', 26065, 26071)]),
    'r7': (7, [('0001', 26071, 26065)]),
    'r8': (8, [('0001', 26081, 26064), ('0002', 26082, 26004)]),
    'r9': (9, [('0001', 26091, 26022), ('0002', 26092, 26003)])
}

hosts = {
    'h1': (1, [('0001', 26001, 26013)]),
    'h2': (2, [('0001', 26002, 26053)]),
    'h3': (3, [('0001', 26003, 26092)]),
    'h4': (4, [('0001', 26004, 26082)])
}

for r_name, (r_id, ifaces) in routers.items():
    # hw.txt
    hw_text = ""
    for idx, (mac_suf, lp, rp) in enumerate(ifaces, 1):
        hw_text += f"int eth{idx} ethernet 0000.111{r_id}.{mac_suf} 127.0.0.1 {lp} 127.0.0.1 {rp}\n"
    hw_text += f"tcp2vrf {10000 + r_id} v1 23\n"
    with open(os.path.join(base_dir, f"{r_name}-hw.txt"), 'w') as f:
        f.write(hw_text)

    # sw.txt
    sw_text = f"hostname {r_name}\nbuggy\n!\nlogging file debug ./logs/{r_name}-log.run\n!\nvrf definition v1\n exit\n!\n"
    for idx in range(1, len(ifaces)+1):
        sw_text += f"interface ethernet{idx}\n vrf for v1\n no log-link-change\n exit\n!\n"
    sw_text += "server telnet tester\n security protocol telnet\n no exec authorization\n no login authentication\n vrf v1\n exit\n!\n!\nend\n"
    with open(os.path.join(base_dir, f"{r_name}-sw.txt"), 'w') as f:
        f.write(sw_text)

for h_name, (h_id, ifaces) in hosts.items():
    # hw.txt
    hw_text = ""
    for idx, (mac_suf, lp, rp) in enumerate(ifaces, 1):
        hw_text += f"int eth{idx} ethernet 0000.aaaa.000{h_id} 127.0.0.1 {lp} 127.0.0.1 {rp}\n"
    hw_text += f"tcp2vrf {20000 + h_id} v1 23\n"
    with open(os.path.join(base_dir, f"{h_name}-hw.txt"), 'w') as f:
        f.write(hw_text)

    # sw.txt
    sw_text = f"hostname {h_name}\nbuggy\n!\nlogging file debug ./logs/{h_name}-log.run\n!\nvrf definition v1\n exit\n!\n"
    for idx in range(1, len(ifaces)+1):
        sw_text += f"interface ethernet{idx}\n vrf forwarding v1\n no shutdown\n no log-link-change\n exit\n!\n"
    sw_text += "console0\n no exec authorization\n no login authentication\n exit\n!\n!\n"
    sw_text += "server telnet tester\n security protocol telnet\n no exec authorization\n no login authentication\n vrf v1\n exit\n!\n!\nend\n"
    with open(os.path.join(base_dir, f"{h_name}-sw.txt"), 'w') as f:
        f.write(sw_text)
