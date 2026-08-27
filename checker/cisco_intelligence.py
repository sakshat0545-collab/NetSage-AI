# =========================================================
# NETSAGE AI
# CISCO COMMAND INTELLIGENCE ENGINE
# =========================================================

"""
This module interprets Cisco show commands and maps them
to networking diagnostic purposes.

It does NOT directly modify network devices.

It provides:
    - command identification
    - diagnostic purpose
    - expected evidence
    - relevant OSI layer
    - troubleshooting priority
    - recommended next commands
"""


# =========================================================
# CISCO COMMAND KNOWLEDGE BASE
# =========================================================

COMMAND_KNOWLEDGE = {

    "show ip route": {

        "category": "Routing",

        "purpose": (
            "Displays the router's routing table and "
            "shows how destination networks are reached."
        ),

        "evidence": [
            "Connected routes",
            "Static routes",
            "Dynamic routes",
            "Next-hop addresses",
            "Missing destination networks",
        ],

        "osi_layer": "Layer 3 - Network",

        "priority": "High",

        "next_commands": [
            "show ip interface",
            "show running-config",
        ],
    },


    "show ip interface": {

        "category": "IP Interface",

        "purpose": (
            "Displays Layer 3 interface configuration "
            "including IP addressing and interface status."
        ),

        "evidence": [
            "IP address",
            "Subnet mask",
            "Interface status",
            "Line protocol",
            "Access restrictions",
        ],

        "osi_layer": "Layer 3 - Network",

        "priority": "High",

        "next_commands": [
            "show interfaces",
            "show running-config",
        ],
    },


    "show interfaces": {

        "category": "Interface Status",

        "purpose": (
            "Provides detailed physical and logical "
            "interface information."
        ),

        "evidence": [
            "Interface state",
            "Line protocol",
            "Errors",
            "Packet counters",
            "Duplex",
            "Speed",
        ],

        "osi_layer": "Layer 1/2",

        "priority": "High",

        "next_commands": [
            "show interfaces status",
            "show running-config",
        ],
    },


    "show interfaces status": {

        "category": "Interface Status",

        "purpose": (
            "Provides a compact status overview of "
            "switch interfaces."
        ),

        "evidence": [
            "Connected ports",
            "Disconnected ports",
            "Disabled ports",
            "Speed",
            "Duplex",
            "VLAN assignment",
        ],

        "osi_layer": "Layer 1/2",

        "priority": "High",

        "next_commands": [
            "show interfaces",
            "show vlan brief",
        ],
    },


    "show vlan brief": {

        "category": "VLAN",

        "purpose": (
            "Displays VLANs configured on the switch "
            "and their associated access ports."
        ),

        "evidence": [
            "VLAN IDs",
            "VLAN names",
            "Active VLANs",
            "Access-port assignments",
        ],

        "osi_layer": "Layer 2 - Data Link",

        "priority": "High",

        "next_commands": [
            "show interfaces trunk",
            "show running-config",
        ],
    },


    "show interfaces trunk": {

        "category": "VLAN Trunking",

        "purpose": (
            "Displays trunk ports and VLANs allowed "
            "across trunk links."
        ),

        "evidence": [
            "Trunk interfaces",
            "Native VLAN",
            "Allowed VLANs",
            "Active VLANs",
            "Encapsulation",
        ],

        "osi_layer": "Layer 2 - Data Link",

        "priority": "High",

        "next_commands": [
            "show vlan brief",
            "show running-config",
        ],
    },


    "show ip arp": {

        "category": "ARP",

        "purpose": (
            "Displays IP-to-MAC address mappings "
            "learned by the device."
        ),

        "evidence": [
            "IP address",
            "MAC address",
            "ARP type",
            "Interface",
        ],

        "osi_layer": "Layer 2/3",

        "priority": "Medium",

        "next_commands": [
            "show ip interface",
            "show interfaces",
        ],
    },


    "show mac address-table": {

        "category": "MAC Address Table",

        "purpose": (
            "Displays learned MAC addresses and the "
            "switch ports on which they were learned."
        ),

        "evidence": [
            "MAC address",
            "VLAN",
            "Port",
            "Dynamic/static entries",
        ],

        "osi_layer": "Layer 2 - Data Link",

        "priority": "Medium",

        "next_commands": [
            "show vlan brief",
            "show interfaces status",
        ],
    },


    "show access-lists": {

        "category": "Access Control",

        "purpose": (
            "Displays configured access control lists "
            "and their permit/deny rules."
        ),

        "evidence": [
            "ACL number/name",
            "Permit rules",
            "Deny rules",
            "Source addresses",
            "Destination addresses",
            "Protocol restrictions",
        ],

        "osi_layer": "Layer 3/4",

        "priority": "High",

        "next_commands": [
            "show running-config",
            "show ip interface",
        ],
    },


    "show running-config": {

        "category": "Configuration",

        "purpose": (
            "Displays the active running configuration "
            "of the Cisco device."
        ),

        "evidence": [
            "Interface configuration",
            "VLAN configuration",
            "Routing configuration",
            "ACL configuration",
            "IP addressing",
            "Trunk configuration",
        ],

        "osi_layer": "Multiple",

        "priority": "High",

        "next_commands": [
            "show ip route",
            "show vlan brief",
            "show interfaces",
        ],
    },
}


# =========================================================
# NORMALIZE COMMAND
# =========================================================

def normalize_command(command):

    if not command:
        return ""

    command = command.strip().lower()

    # Remove unnecessary whitespace
    command = " ".join(command.split())

    return command


# =========================================================
# IDENTIFY COMMAND
# =========================================================

def identify_command(command):

    normalized = normalize_command(command)

    if normalized in COMMAND_KNOWLEDGE:

        return COMMAND_KNOWLEDGE[normalized]

    return None


# =========================================================
# ANALYZE SINGLE COMMAND
# =========================================================

def analyze_command(command):

    normalized = normalize_command(command)

    knowledge = identify_command(normalized)

    if knowledge is None:

        return {

            "command": command,

            "recognized": False,

            "category": "Unknown",

            "purpose": (
                "The supplied command is not currently "
                "available in the NetSage command knowledge base."
            ),

            "evidence": [],

            "osi_layer": "Unknown",

            "priority": "Low",

            "next_commands": [],

        }

    return {

        "command": normalized,

        "recognized": True,

        "category": knowledge["category"],

        "purpose": knowledge["purpose"],

        "evidence": knowledge["evidence"],

        "osi_layer": knowledge["osi_layer"],

        "priority": knowledge["priority"],

        "next_commands": knowledge["next_commands"],

    }


# =========================================================
# ANALYZE MULTIPLE COMMANDS
# =========================================================

def analyze_commands(commands):

    if not commands:

        return []

    results = []

    for command in commands:

        result = analyze_command(command)

        results.append(result)

    return results


# =========================================================
# FIND BEST NEXT COMMAND
# =========================================================

def recommend_next_command(
    issue_type=None,
    detected_commands=None
):
    """
    Recommend the most useful Cisco command based on
    the detected problem category.
    """

    issue_map = {

        "Duplicate IP": "show ip arp",

        "Subnet Mask": "show ip interface",

        "Gateway": "show ip interface",

        "Interface Status":
            "show interfaces status",

        "VLAN":
            "show vlan brief",

        "Routing":
            "show ip route",

        "ACL":
            "show access-lists",

        "ARP":
            "show ip arp",

    }

    if issue_type in issue_map:

        return issue_map[issue_type]


    # If we already have commands, suggest a related
    # command that has not already been supplied.

    supplied = set()

    if detected_commands:

        supplied = {
            normalize_command(command)
            for command in detected_commands
        }


    fallback_priority = [

        "show ip route",

        "show ip interface",

        "show interfaces status",

        "show vlan brief",

        "show interfaces trunk",

        "show ip arp",

        "show running-config",

    ]


    for command in fallback_priority:

        if command not in supplied:

            return command


    return "show running-config"


# =========================================================
# BUILD COMMAND INTELLIGENCE
# =========================================================

def build_command_intelligence(
    commands,
    issue_type=None
):

    command_analysis = analyze_commands(
        commands
    )

    next_command = recommend_next_command(
        issue_type=issue_type,
        detected_commands=commands,
    )

    return {

        "commands_analyzed": len(
            command_analysis
        ),

        "recognized_commands": sum(
            1
            for item in command_analysis
            if item["recognized"]
        ),

        "command_analysis": command_analysis,

        "recommended_next_command": next_command,

    }