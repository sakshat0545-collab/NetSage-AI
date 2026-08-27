# =========================================================
# NETSAGE AI
# AI DIAGNOSIS ENGINE TEST
# =========================================================

from diagnosis_engine import generate_diagnosis


print("=" * 60)
print("NETSAGE AI - AI DIAGNOSIS ENGINE TEST")
print("=" * 60)


# ---------------------------------------------------------
# Sample symptom
# ---------------------------------------------------------

symptom = (
    "PC in VLAN 30 cannot reach the server."
)


# ---------------------------------------------------------
# Sample topology
# ---------------------------------------------------------

topology = (
    "PC is connected to GigabitEthernet0/1. "
    "PC IP address is 192.168.10.10. "
    "Default gateway is 192.168.10.1. "
    "PC belongs to VLAN 30. "
    "Server network is 192.168.30.0/24."
)


# ---------------------------------------------------------
# Sample parsed evidence
# ---------------------------------------------------------

parsed_evidence = {

    "all_ip_addresses": [

        "192.168.10.10",

        "255.255.255.0",

        "192.168.10.1",

        "192.168.30.0",

    ],

    "host_ips": [

        "192.168.10.10",

    ],

    "subnet_masks": [

        "255.255.255.0",

    ],

    "gateway": "192.168.10.1",

    "vlan_ids": [

        30,

    ],

    "networks": [

        "192.168.30.0/24",

    ],

}


# ---------------------------------------------------------
# Sample rule checker result
# ---------------------------------------------------------

rule_checker = {

    "total_checks": 6,

    "issues_found": 1,

    "overall_status": "ISSUES_DETECTED",

    "results": [

        {

            "check": "Interface Status",

            "status": "ISSUE",

            "details": (
                "Down interface detected: "
                "GigabitEthernet0/1"
            ),

            "evidence": [

                "GigabitEthernet0/1",

            ],

        },

        {

            "check": "Subnet Mask",

            "status": "PASS",

            "details": (
                "192.168.10.10 with mask "
                "255.255.255.0 is valid."
            ),

            "evidence": [],

        },

        {

            "check": "Gateway",

            "status": "PASS",

            "details": (
                "Gateway 192.168.10.1 belongs "
                "to the subnet."
            ),

            "evidence": [],

        },

    ],

}


# ---------------------------------------------------------
# Sample Cisco intelligence
# ---------------------------------------------------------

command_intelligence = {

    "recommended_next_command":
        "show interfaces status",

}


# ---------------------------------------------------------
# Generate diagnosis
# ---------------------------------------------------------

result = generate_diagnosis(

    symptom=symptom,

    topology=topology,

    parsed_evidence=parsed_evidence,

    rule_checker=rule_checker,

    command_intelligence=command_intelligence,

)


# ---------------------------------------------------------
# Display result
# ---------------------------------------------------------

print("\nROOT CAUSE")
print("-" * 40)

print(
    result["root_cause"]
)


print("\nISSUE TYPE")
print("-" * 40)

print(
    result["issue_type"]
)


print("\nCONFIDENCE")
print("-" * 40)

print(
    result["confidence"]
)


print("\nTECHNICAL REASON")
print("-" * 40)

print(
    result["technical_reason"]
)


print("\nRECOMMENDED ACTION")
print("-" * 40)

print(
    result["recommended_action"]
)


print("\nRECOMMENDED NEXT COMMAND")
print("-" * 40)

print(
    result["recommended_next_command"]
)


print("\nEXPLANATION")
print("-" * 40)

print(
    result["explanation"]
)


print("\nVALIDATION")
print("-" * 40)

print(
    result["validation_summary"]
)


print("\nHUMAN REVIEW")
print("-" * 40)

print(
    result["human_review"]
)


print("\n" + "=" * 60)
print("AI DIAGNOSIS TEST COMPLETED")
print("=" * 60)