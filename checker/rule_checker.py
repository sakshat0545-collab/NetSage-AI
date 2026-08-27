import ipaddress
import re


# =========================================================
# DUPLICATE IP CHECK
# =========================================================

def check_duplicate_ips(ip_addresses):
    """
    Detect duplicate IPv4 addresses.
    """

    if not isinstance(ip_addresses, list):
        ip_addresses = []

    normalized = [
        str(ip).strip()
        for ip in ip_addresses
        if str(ip).strip()
    ]

    duplicates = []

    for ip in set(normalized):
        if normalized.count(ip) > 1:
            duplicates.append(ip)

    return {
        "check": "Duplicate IP",
        "status": "ISSUE" if duplicates else "PASS",
        "details": (
            f"Duplicate IP addresses found: "
            f"{', '.join(duplicates)}"
            if duplicates
            else "No duplicate IP addresses detected."
        ),
        "evidence": duplicates,
    }


# =========================================================
# SUBNET MASK CHECK
# =========================================================

def check_subnet_mask(ip_address, subnet_mask):
    """
    Validate IPv4 address and subnet mask.
    """

    try:

        ipaddress.IPv4Network(
            f"{ip_address}/{subnet_mask}",
            strict=False
        )

        return {
            "check": "Subnet Mask",
            "status": "PASS",
            "details": (
                f"{ip_address} with mask "
                f"{subnet_mask} is valid."
            ),
            "evidence": [],
        }

    except ValueError as error:

        return {
            "check": "Subnet Mask",
            "status": "ISSUE",
            "details": (
                f"Invalid subnet mask or IP: "
                f"{ip_address}/{subnet_mask}. "
                f"{error}"
            ),
            "evidence": [
                f"{ip_address}/{subnet_mask}"
            ],
        }


# =========================================================
# GATEWAY CHECK
# =========================================================

def check_gateway(
    ip_address,
    subnet_mask,
    gateway
):
    """
    Check whether the default gateway
    belongs to the same subnet as the host.
    """

    try:

        network = ipaddress.IPv4Network(
            f"{ip_address}/{subnet_mask}",
            strict=False
        )

        gateway_ip = ipaddress.IPv4Address(
            gateway
        )

        if gateway_ip in network:

            return {
                "check": "Gateway",
                "status": "PASS",
                "details": (
                    f"Gateway {gateway} belongs "
                    f"to the subnet {network}."
                ),
                "evidence": [],
            }

        return {
            "check": "Gateway",
            "status": "ISSUE",
            "details": (
                f"Gateway {gateway} does not belong "
                f"to host subnet {network}."
            ),
            "evidence": [gateway],
        }

    except ValueError as error:

        return {
            "check": "Gateway",
            "status": "ISSUE",
            "details": (
                f"Invalid network configuration: "
                f"{error}"
            ),
            "evidence": [],
        }


# =========================================================
# INTERFACE STATUS CHECK
# =========================================================

def check_interface_status(show_output):
    """
    Detect interfaces that are:

    1. Administratively down
    2. Operationally down
    3. Have line protocol down

    Supports both:

    Raw Cisco output:
        GigabitEthernet0/1 is administratively down

    Parsed list:
        ["GigabitEthernet0/1"]
    """

    down_interfaces = []

    # -----------------------------------------------------
    # Case 1: Parser already supplied a list
    # -----------------------------------------------------

    if isinstance(show_output, list):

        for interface in show_output:

            if interface:

                interface = str(interface).strip()

                if interface and interface not in down_interfaces:
                    down_interfaces.append(interface)

    # -----------------------------------------------------
    # Case 2: Raw Cisco show-command output
    # -----------------------------------------------------

    elif isinstance(show_output, str):

        text = show_output.strip()

        if text:

            patterns = [

                # Example:
                # GigabitEthernet0/1 is administratively down
                r"(?im)^\s*"
                r"(GigabitEthernet|"
                r"FastEthernet|"
                r"TenGigabitEthernet|"
                r"Ethernet|"
                r"Serial|"
                r"Loopback|"
                r"Vlan)"
                r"(\d+(?:/\d+){0,3})"
                r"\s+is\s+administratively\s+down\b",

                # Example:
                # GigabitEthernet0/1 is down
                r"(?im)^\s*"
                r"(GigabitEthernet|"
                r"FastEthernet|"
                r"TenGigabitEthernet|"
                r"Ethernet|"
                r"Serial|"
                r"Loopback|"
                r"Vlan)"
                r"(\d+(?:/\d+){0,3})"
                r"\s+is\s+down\b",

                # Example:
                # GigabitEthernet0/1, line protocol is down
                r"(?im)^\s*"
                r"(GigabitEthernet|"
                r"FastEthernet|"
                r"TenGigabitEthernet|"
                r"Ethernet|"
                r"Serial|"
                r"Loopback|"
                r"Vlan)"
                r"(\d+(?:/\d+){0,3})"
                r"[^\n]{0,150}?"
                r"line protocol is down\b",
            ]

            for pattern in patterns:

                matches = re.findall(
                    pattern,
                    text
                )

                for match in matches:

                    if isinstance(match, tuple):

                        interface = (
                            match[0]
                            + match[1]
                        )

                    else:

                        interface = match

                    if interface not in down_interfaces:

                        down_interfaces.append(
                            interface
                        )

    # -----------------------------------------------------
    # Final result
    # -----------------------------------------------------

    return {
        "check": "Interface Status",

        "status": (
            "ISSUE"
            if down_interfaces
            else "PASS"
        ),

        "details": (
            "Down interfaces detected: "
            + ", ".join(down_interfaces)
            if down_interfaces
            else
            "No down interfaces detected."
        ),

        "evidence": down_interfaces,
    }


# =========================================================
# VLAN CHECK
# =========================================================

def check_missing_vlans(
    show_vlan_output,
    required_vlans
):
    """
    Check whether required VLANs appear
    in 'show vlan brief' output.
    """

    if not isinstance(show_vlan_output, str):
        show_vlan_output = ""

    if not isinstance(required_vlans, list):
        required_vlans = []

    missing_vlans = []

    for vlan in required_vlans:

        pattern = (
            rf"(?m)^\s*"
            rf"{re.escape(str(vlan))}"
            rf"\s+"
        )

        if not re.search(
            pattern,
            show_vlan_output
        ):

            missing_vlans.append(
                str(vlan)
            )

    return {
        "check": "VLAN",

        "status": (
            "ISSUE"
            if missing_vlans
            else "PASS"
        ),

        "details": (
            f"Missing VLANs: "
            f"{', '.join(missing_vlans)}"
            if missing_vlans
            else
            "All required VLANs are present."
        ),

        "evidence": missing_vlans,
    }


# =========================================================
# ROUTING CHECK
# =========================================================

def check_missing_routes(
    show_route_output,
    required_networks
):
    """
    Check whether required networks appear
    in 'show ip route' output.
    """

    if not isinstance(show_route_output, str):
        show_route_output = ""

    if not isinstance(required_networks, list):
        required_networks = []

    missing_routes = []

    for network in required_networks:

        try:

            network_obj = ipaddress.IPv4Network(
                network,
                strict=False
            )

            network_address = str(
                network_obj.network_address
            )

            if network_address not in show_route_output:

                missing_routes.append(
                    network
                )

        except ValueError:

            missing_routes.append(
                network
            )

    return {
        "check": "Routing",

        "status": (
            "ISSUE"
            if missing_routes
            else "PASS"
        ),

        "details": (
            f"Missing routes: "
            f"{', '.join(missing_routes)}"
            if missing_routes
            else
            "All required routes are present."
        ),

        "evidence": missing_routes,
    }


# =========================================================
# RUN ALL CHECKS
# =========================================================

def run_all_checks(
    ip_addresses=None,
    ip_address=None,
    subnet_mask=None,
    gateway=None,

    show_interfaces="",
    down_interfaces=None,

    show_vlan="",
    required_vlans=None,

    show_routes="",
    required_networks=None,
):
    """
    Run all available deterministic network checks.

    Interface status supports both:

        show_interfaces = raw Cisco output

    and:

        down_interfaces = parser result
    """

    results = []

    # -----------------------------------------------------
    # Duplicate IP
    # -----------------------------------------------------

    if ip_addresses:

        results.append(
            check_duplicate_ips(
                ip_addresses
            )
        )

    # -----------------------------------------------------
    # Subnet Mask
    # -----------------------------------------------------

    if (
        ip_address
        and subnet_mask
    ):

        results.append(
            check_subnet_mask(
                ip_address,
                subnet_mask
            )
        )

    # -----------------------------------------------------
    # Gateway
    # -----------------------------------------------------

    if (
        ip_address
        and subnet_mask
        and gateway
    ):

        results.append(
            check_gateway(
                ip_address,
                subnet_mask,
                gateway
            )
        )

    # -----------------------------------------------------
    # Interface Status
    # -----------------------------------------------------

    interface_evidence = None

    if down_interfaces:

        interface_evidence = down_interfaces

    elif show_interfaces:

        interface_evidence = show_interfaces

    if interface_evidence:

        results.append(
            check_interface_status(
                interface_evidence
            )
        )

    # -----------------------------------------------------
    # VLAN
    # -----------------------------------------------------

    if (
        show_vlan
        and required_vlans
    ):

        results.append(
            check_missing_vlans(
                show_vlan,
                required_vlans
            )
        )

    # -----------------------------------------------------
    # Routing
    # -----------------------------------------------------

    if (
        show_routes
        and required_networks
    ):

        results.append(
            check_missing_routes(
                show_routes,
                required_networks
            )
        )

    # -----------------------------------------------------
    # Find issues
    # -----------------------------------------------------

    issues = [
        result
        for result in results
        if result.get("status") == "ISSUE"
    ]

    # -----------------------------------------------------
    # Final result
    # -----------------------------------------------------

    return {

        "total_checks": len(results),

        "issues_found": len(issues),

        "overall_status": (
            "ISSUES_DETECTED"
            if issues
            else
            "NO_ISSUES_DETECTED"
        ),

        "results": results,
    }