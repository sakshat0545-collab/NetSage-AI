from cisco_intelligence import (
    analyze_command,
    analyze_commands,
    recommend_next_command,
)


print("=" * 60)
print("NETSAGE AI - CISCO COMMAND INTELLIGENCE TEST")
print("=" * 60)


# ---------------------------------------------------------
# Test 1
# ---------------------------------------------------------

print("\nTEST 1: show ip route")

result = analyze_command(
    "show ip route"
)

print("Recognized :", result["recognized"])
print("Category   :", result["category"])
print("OSI Layer  :", result["osi_layer"])
print("Priority   :", result["priority"])


# ---------------------------------------------------------
# Test 2
# ---------------------------------------------------------

print("\nTEST 2: show vlan brief")

result = analyze_command(
    "show vlan brief"
)

print("Recognized :", result["recognized"])
print("Category   :", result["category"])
print("OSI Layer  :", result["osi_layer"])


# ---------------------------------------------------------
# Test 3
# ---------------------------------------------------------

print("\nTEST 3: Multiple commands")

commands = [

    "show ip route",

    "show vlan brief",

    "show interfaces",

]

results = analyze_commands(
    commands
)

for result in results:

    print(
        f"{result['command']} "
        f"-> {result['category']}"
    )


# ---------------------------------------------------------
# Test 4
# ---------------------------------------------------------

print("\nTEST 4: Next command recommendation")

next_command = recommend_next_command(
    issue_type="Routing"
)

print(
    "Routing issue ->",
    next_command
)


# ---------------------------------------------------------
# Test 5
# ---------------------------------------------------------

print("\nTEST 5: Unknown command")

result = analyze_command(
    "show something"
)

print("Recognized :", result["recognized"])
print("Category   :", result["category"])


print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)