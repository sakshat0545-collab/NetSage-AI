from rule_checker import run_all_checks


def main():

    print("=" * 60)
    print("NETSAGE AI - DETERMINISTIC RULE CHECKER")
    print("=" * 60)

    result = run_all_checks(

        # Duplicate IP test
        ip_addresses=[
            "192.168.10.10",
            "192.168.10.11",
            "192.168.10.10",
            "192.168.20.10",
        ],

        # IP + subnet test
        ip_address="192.168.10.10",
        subnet_mask="255.255.255.0",

        # Gateway test
        gateway="192.168.10.1",

        # Interface test
        show_interfaces="""
GigabitEthernet0/0 is up, line protocol is up
GigabitEthernet0/1 is administratively down, line protocol is down
GigabitEthernet0/2 is up, line protocol is up
""",

        # VLAN test
        show_vlan="""
10   USERS
20   SERVERS
30   GUEST
""",

        required_vlans=[
            10,
            20,
            30,
            40,
        ],

        # Routing test
        show_routes="""
C    192.168.10.0/24 is directly connected
C    192.168.20.0/24 is directly connected
S    10.0.0.0/8 [1/0] via 192.168.10.1
""",

        required_networks=[
            "192.168.10.0/24",
            "192.168.20.0/24",
            "192.168.30.0/24",
        ],
    )

    print()
    print(f"Total Checks : {result['total_checks']}")
    print(f"Issues Found : {result['issues_found']}")
    print(f"Status       : {result['overall_status']}")
    print()

    print("-" * 60)

    for item in result["results"]:

        print(f"\nCheck   : {item['check']}")
        print(f"Status  : {item['status']}")
        print(f"Details : {item['details']}")

        if item["evidence"]:
            print(
                f"Evidence: {', '.join(item['evidence'])}"
            )

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()