import ipaddress
import re


# =========================================================
# NETSAGE AI - INTELLIGENT EVIDENCE PARSER
# =========================================================


# ---------------------------------------------------------
# Helper: validate IPv4
# ---------------------------------------------------------

def is_valid_ipv4(value):
    try:
        ipaddress.IPv4Address(value)
        return True
    except ValueError:
        return False


# ---------------------------------------------------------
# Extract all IPv4 addresses
# ---------------------------------------------------------

def extract_all_ipv4(text):
    """
    Extract every valid IPv4 address from text.
    """

    if not text:
        return []

    pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

    candidates = re.findall(pattern, text)

    addresses = []

    for candidate in candidates:

        if is_valid_ipv4(candidate):

            if candidate not in addresses:
                addresses.append(candidate)

    return addresses


# ---------------------------------------------------------
# Extract subnet masks
# ---------------------------------------------------------

def extract_subnet_masks(text):
    """
    Detect dotted-decimal subnet masks.
    """

    if not text:
        return []

    masks = []

    # Common Cisco mask forms
    pattern = (
        r"\b(?:"
        r"255\.(?:0|128|192|224|240|248|252|254|255)\."
        r"(?:0|128|192|224|240|248|252|254|255)\."
        r"(?:0|128|192|224|240|248|252|254|255)"
        r")\b"
    )

    candidates = re.findall(
        pattern,
        text
    )

    for candidate in candidates:

        try:

            ipaddress.IPv4Network(
                f"0.0.0.0/{candidate}"
            )

            if candidate not in masks:
                masks.append(candidate)

        except ValueError:
            pass

    return masks


# ---------------------------------------------------------
# Extract CIDR networks
# ---------------------------------------------------------

def extract_networks(text):
    """
    Extract CIDR networks such as:

    192.168.10.0/24
    192.168.30.0/24
    10.0.0.0/8
    """

    if not text:
        return []

    pattern = (
        r"\b(?:\d{1,3}\.){3}\d{1,3}"
        r"/(?:3[0-2]|[12]?\d)\b"
    )

    candidates = re.findall(
        pattern,
        text
    )

    networks = []

    for candidate in candidates:

        try:

            network = ipaddress.IPv4Network(
                candidate,
                strict=False
            )

            normalized = str(network)

            if normalized not in networks:
                networks.append(normalized)

        except ValueError:
            pass

    return networks


# ---------------------------------------------------------
# Extract gateway
# ---------------------------------------------------------

def extract_gateway(text):
    """
    Detect gateway/default gateway from natural language
    and Cisco-style routing output.
    """

    if not text:
        return None

    patterns = [

        # Default gateway: 192.168.1.1
        r"(?i)default\s+gateway\s*(?:is|:|=)?\s*"
        r"((?:\d{1,3}\.){3}\d{1,3})",

        # Gateway: 192.168.1.1
        r"(?i)\bgateway\s*(?:is|:|=)?\s*"
        r"((?:\d{1,3}\.){3}\d{1,3})",

        # via 192.168.1.1
        r"(?i)\bvia\s+"
        r"((?:\d{1,3}\.){3}\d{1,3})",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            candidate = match.group(1)

            if is_valid_ipv4(candidate):
                return candidate

    return None


# ---------------------------------------------------------
# Extract VLAN IDs
# ---------------------------------------------------------

def extract_vlan_ids(text):
    """
    Extract explicitly mentioned VLAN IDs.
    """

    if not text:
        return []

    matches = re.findall(
        r"(?i)\bvlan\s*(\d{1,4})\b",
        text
    )

    vlan_ids = []

    for value in matches:

        vlan = int(value)

        if 1 <= vlan <= 4094:

            if vlan not in vlan_ids:
                vlan_ids.append(vlan)

    return vlan_ids


# ---------------------------------------------------------
# Extract Cisco interfaces
# ---------------------------------------------------------

def extract_interfaces(text):
    """
    Detect common Cisco interface names.
    """

    if not text:
        return []

    pattern = (
        r"\b(?:"
        r"GigabitEthernet|"
        r"FastEthernet|"
        r"TenGigabitEthernet|"
        r"Ethernet|"
        r"Serial|"
        r"Loopback|"
        r"Vlan"
        r")"
        r"\d+(?:/\d+){0,3}\b"
    )

    matches = re.findall(
        pattern,
        text,
        flags=re.IGNORECASE
    )

    interfaces = []

    for interface in matches:

        # Normalize common capitalization
        interface = interface[0].upper() + interface[1:]

        if interface not in interfaces:
            interfaces.append(interface)

    return interfaces


# ---------------------------------------------------------
# Extract down interfaces
# ---------------------------------------------------------

def extract_down_interfaces(text):
    """
    Detect interfaces that are administratively down,
    down, or have a down line protocol.
    """

    if not text:
        return []

    down_interfaces = []

    # Example:
    # GigabitEthernet0/1 is administratively down
    pattern_1 = (
        r"(?i)\b("
        r"GigabitEthernet|"
        r"FastEthernet|"
        r"TenGigabitEthernet|"
        r"Ethernet|"
        r"Serial|"
        r"Loopback|"
        r"Vlan"
        r")"
        r"(\d+(?:/\d+){0,3})"
        r"\s+is\s+(?:administratively\s+)?down"
    )

    matches = re.findall(
        pattern_1,
        text
    )

    for prefix, number in matches:

        interface = prefix + number

        if interface not in down_interfaces:
            down_interfaces.append(interface)

    # Example:
    # GigabitEthernet0/1, line protocol is down
    pattern_2 = (
        r"(?i)\b("
        r"GigabitEthernet|"
        r"FastEthernet|"
        r"TenGigabitEthernet|"
        r"Ethernet|"
        r"Serial|"
        r"Loopback|"
        r"Vlan"
        r")"
        r"(\d+(?:/\d+){0,3})"
        r"[^\n]{0,100}?"
        r"line protocol is down"
    )

    matches = re.findall(
        pattern_2,
        text
    )

    for prefix, number in matches:

        interface = prefix + number

        if interface not in down_interfaces:
            down_interfaces.append(interface)

    return down_interfaces


# ---------------------------------------------------------
# Extract host IPs
# ---------------------------------------------------------

def extract_host_ips(
    text,
    all_ips=None,
    subnet_masks=None,
    gateway=None,
    networks=None
):
    """
    Identify likely host IP addresses while excluding:

    - subnet masks
    - gateway
    - network addresses
    - broadcast addresses
    """

    if not text:
        return []

    if all_ips is None:
        all_ips = extract_all_ipv4(text)

    if subnet_masks is None:
        subnet_masks = extract_subnet_masks(text)

    if networks is None:
        networks = extract_networks(text)

    host_ips = []

    excluded = set(subnet_masks)

    if gateway:
        excluded.add(gateway)

    # Exclude network and broadcast addresses
    for network in networks:

        try:

            net = ipaddress.IPv4Network(
                network,
                strict=False
            )

            excluded.add(str(net.network_address))
            excluded.add(str(net.broadcast_address))

        except ValueError:
            pass

    # Look for explicit host/IP/address wording first
    explicit_patterns = [

        r"(?i)(?:pc|host|client|device)"
        r"\s*(?:ip|address)"
        r"\s*(?:is|:|=)?\s*"
        r"((?:\d{1,3}\.){3}\d{1,3})",

        r"(?i)\bip\s+address\s*(?:is|:|=)?\s*"
        r"((?:\d{1,3}\.){3}\d{1,3})",

        r"(?i)\baddress\s*(?:is|:|=)?\s*"
        r"((?:\d{1,3}\.){3}\d{1,3})",
    ]

    explicit_ips = []

    for pattern in explicit_patterns:

        matches = re.findall(
            pattern,
            text
        )

        for candidate in matches:

            if is_valid_ipv4(candidate):

                if candidate not in explicit_ips:
                    explicit_ips.append(candidate)

    for ip in explicit_ips:

        if ip not in excluded:

            if ip not in host_ips:
                host_ips.append(ip)

    # Fallback: consider remaining valid IPs as candidates
    for ip in all_ips:

        if ip in excluded:
            continue

        if ip not in host_ips:
            host_ips.append(ip)

    return host_ips


# ---------------------------------------------------------
# Extract routing entries
# ---------------------------------------------------------

def extract_routes(text):
    """
    Extract simple Cisco routing entries.
    """

    if not text:
        return []

    routes = []

    # Example:
    # C 192.168.10.0/24 is directly connected
    pattern = (
        r"(?i)\b[CSOERL\*]?\s*"
        r"((?:\d{1,3}\.){3}\d{1,3}/"
        r"(?:3[0-2]|[12]?\d))"
    )

    matches = re.findall(
        pattern,
        text
    )

    for route in matches:

        try:

            network = str(
                ipaddress.IPv4Network(
                    route,
                    strict=False
                )
            )

            if network not in routes:
                routes.append(network)

        except ValueError:
            pass

    return routes


# ---------------------------------------------------------
# Detect command sections
# ---------------------------------------------------------

def detect_commands(text):
    """
    Detect common Cisco show commands contained in
    the supplied evidence.
    """

    if not text:
        return []

    commands = [

        "show ip route",
        "show ip interface",
        "show ip arp",
        "show vlan brief",
        "show interfaces",
        "show interfaces status",
        "show interfaces trunk",
        "show running-config",
        "show access-lists",
        "show mac address-table",
    ]

    detected = []

    lowered = text.lower()

    for command in commands:

        if command in lowered:

            detected.append(command)

    return detected


# ---------------------------------------------------------
# Complete parser
# ---------------------------------------------------------

def parse_evidence(
    symptom="",
    topology="",
    show_output=""
):
    """
    Parse the user's complete network evidence.

    The parser keeps different network entities separate
    so downstream diagnostic logic can reason correctly.
    """

    combined_text = "\n".join([
        symptom or "",
        topology or "",
        show_output or "",
    ])

    all_ips = extract_all_ipv4(
        combined_text
    )

    subnet_masks = extract_subnet_masks(
        combined_text
    )

    networks = extract_networks(
        combined_text
    )

    gateway = extract_gateway(
        combined_text
    )

    vlan_ids = extract_vlan_ids(
        combined_text
    )

    interfaces = extract_interfaces(
        combined_text
    )

    down_interfaces = extract_down_interfaces(
        show_output
    )

    host_ips = extract_host_ips(
        combined_text,
        all_ips=all_ips,
        subnet_masks=subnet_masks,
        gateway=gateway,
        networks=networks,
    )

    routes = extract_routes(
        show_output
    )

    commands = detect_commands(
        show_output
    )

    return {

        # All raw IPs found
        "all_ip_addresses": all_ips,

        # Only likely host/device IPs
        "host_ips": host_ips,

        # Backward-compatible field
        "ip_addresses": host_ips,

        # Network configuration
        "subnet_masks": subnet_masks,

        "gateway": gateway,

        "networks": networks,

        # VLAN information
        "vlan_ids": vlan_ids,

        # Interface information
        "interfaces": interfaces,

        "down_interfaces": down_interfaces,

        # Routing information
        "routes": routes,

        # Detected Cisco commands
        "commands": commands,

        # Preserve original evidence
        "raw_evidence": {

            "symptom": symptom,

            "topology": topology,

            "show_output": show_output,

        },
    }