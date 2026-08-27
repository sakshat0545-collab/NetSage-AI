# =========================================================
# NETSAGE AI
# AI DIAGNOSIS ENGINE
# =========================================================

"""
NetSage AI Diagnosis Engine

This module converts:
    - network symptoms
    - topology information
    - parsed Cisco evidence
    - deterministic rule results
    - Cisco command intelligence

into an explainable network diagnosis.

The current implementation provides a reliable local
reasoning engine that can operate without an external
LLM/API.

An external LLM can be integrated later without changing
the overall application architecture.
"""


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def safe_list(value):

    if isinstance(value, list):
        return value

    return []


def get_rule_results(rule_checker):

    if not isinstance(rule_checker, dict):
        return []

    return safe_list(
        rule_checker.get("results", [])
    )


def get_issues(rule_checker):

    results = get_rule_results(
        rule_checker
    )

    return [
        result
        for result in results
        if result.get("status") == "ISSUE"
    ]


def get_passes(rule_checker):

    results = get_rule_results(
        rule_checker
    )

    return [
        result
        for result in results
        if result.get("status") == "PASS"
    ]


# =========================================================
# ISSUE PRIORITY
# =========================================================

ISSUE_PRIORITY = {

    "Interface Status": 100,

    "Duplicate IP": 95,

    "Gateway": 90,

    "VLAN": 85,

    "Routing": 85,

    "Subnet Mask": 80,

    "ARP": 70,

    "ACL": 70,

}


def issue_score(issue):

    check_name = issue.get(
        "check",
        ""
    )

    return ISSUE_PRIORITY.get(
        check_name,
        50
    )


# =========================================================
# ROOT CAUSE ANALYSIS
# =========================================================

def determine_root_cause(
    issues,
    symptom=""
):

    if not issues:

        return {

            "root_cause": (
                "No deterministic network "
                "configuration issue was identified."
            ),

            "issue_type": None,

            "confidence": "Low",

        }


    # Sort issues according to technical priority.

    ranked_issues = sorted(
        issues,
        key=issue_score,
        reverse=True
    )

    primary_issue = ranked_issues[0]

    issue_type = primary_issue.get(
        "check"
    )

    details = primary_issue.get(
        "details",
        ""
    )

    evidence = primary_issue.get(
        "evidence",
        []
    )


    # -----------------------------------------------------
    # Interface
    # -----------------------------------------------------

    if issue_type == "Interface Status":

        return {

            "root_cause": (
                "A network interface appears to be "
                "down or administratively disabled."
            ),

            "issue_type": issue_type,

            "confidence": "High",

            "technical_reason": (
                details
                or
                "The interface state is inconsistent "
                "with normal network operation."
            ),

            "evidence": evidence,

        }


    # -----------------------------------------------------
    # Duplicate IP
    # -----------------------------------------------------

    if issue_type == "Duplicate IP":

        return {

            "root_cause": (
                "A duplicate IP address was detected "
                "in the network."
            ),

            "issue_type": issue_type,

            "confidence": "High",

            "technical_reason": (
                details
                or
                "Multiple devices appear to use "
                "the same IP address."
            ),

            "evidence": evidence,

        }


    # -----------------------------------------------------
    # Gateway
    # -----------------------------------------------------

    if issue_type == "Gateway":

        return {

            "root_cause": (
                "The configured default gateway does "
                "not appear to belong to the expected "
                "IP subnet."
            ),

            "issue_type": issue_type,

            "confidence": "High",

            "technical_reason": (
                details
                or
                "The gateway configuration is "
                "inconsistent with the host subnet."
            ),

            "evidence": evidence,

        }


    # -----------------------------------------------------
    # VLAN
    # -----------------------------------------------------

    if issue_type == "VLAN":

        return {

            "root_cause": (
                "The required VLAN configuration appears "
                "to be missing or inconsistent."
            ),

            "issue_type": issue_type,

            "confidence": "High",

            "technical_reason": (
                details
                or
                "The expected VLAN was not found "
                "in the supplied evidence."
            ),

            "evidence": evidence,

        }


    # -----------------------------------------------------
    # Routing
    # -----------------------------------------------------

    if issue_type == "Routing":

        return {

            "root_cause": (
                "A required destination network does "
                "not appear to have a valid route."
            ),

            "issue_type": issue_type,

            "confidence": "High",

            "technical_reason": (
                details
                or
                "The routing evidence indicates that "
                "the destination network may be unreachable."
            ),

            "evidence": evidence,

        }


    # -----------------------------------------------------
    # Subnet Mask
    # -----------------------------------------------------

    if issue_type == "Subnet Mask":

        return {

            "root_cause": (
                "The host subnet mask appears to be "
                "incorrect or inconsistent."
            ),

            "issue_type": issue_type,

            "confidence": "High",

            "technical_reason": (
                details
                or
                "The supplied IP configuration does "
                "not match the expected subnet."
            ),

            "evidence": evidence,

        }


    # -----------------------------------------------------
    # Generic issue
    # -----------------------------------------------------

    return {

        "root_cause": (
            f"A potential {issue_type} issue "
            "was detected."
        ),

        "issue_type": issue_type,

        "confidence": "Medium",

        "technical_reason": (
            details
            or
            "The deterministic rule checker "
            "identified an inconsistency."
        ),

        "evidence": evidence,

    }


# =========================================================
# SOLUTION GENERATOR
# =========================================================

def generate_solution(
    issue_type,
    root_cause
):

    solutions = {

        "Interface Status": {

            "recommended_action": (
                "Verify the affected interface and "
                "enable it if it is intentionally disabled."
            ),

            "recommended_commands": [

                "show interfaces status",

                "show interfaces",

                "show running-config",

            ],

        },


        "Duplicate IP": {

            "recommended_action": (
                "Identify the devices using the duplicate "
                "IP address and assign unique addresses."
            ),

            "recommended_commands": [

                "show ip arp",

                "show ip interface",

                "show running-config",

            ],

        },


        "Gateway": {

            "recommended_action": (
                "Verify that the default gateway belongs "
                "to the same subnet as the host."
            ),

            "recommended_commands": [

                "show ip interface",

                "show running-config",

            ],

        },


        "VLAN": {

            "recommended_action": (
                "Verify that the required VLAN exists and "
                "that the relevant switch port is assigned "
                "to the correct VLAN."
            ),

            "recommended_commands": [

                "show vlan brief",

                "show interfaces status",

                "show interfaces trunk",

            ],

        },


        "Routing": {

            "recommended_action": (
                "Verify that a route exists toward the "
                "destination network and confirm the "
                "next-hop configuration."
            ),

            "recommended_commands": [

                "show ip route",

                "show ip interface",

                "show running-config",

            ],

        },


        "Subnet Mask": {

            "recommended_action": (
                "Verify the host subnet mask and ensure "
                "that it matches the intended network."
            ),

            "recommended_commands": [

                "show ip interface",

                "show running-config",

            ],

        },

    }


    solution = solutions.get(
        issue_type
    )


    if solution:

        return solution


    return {

        "recommended_action": (
            "Inspect the supplied network evidence "
            "and verify the affected configuration."
        ),

        "recommended_commands": [

            "show running-config",

            "show interfaces",

        ],

    }


# =========================================================
# EXPLANATION GENERATOR
# =========================================================

def generate_explanation(
    root_cause,
    solution,
    evidence
):

    root = root_cause.get(
        "root_cause",
        ""
    )

    technical_reason = root_cause.get(
        "technical_reason",
        ""
    )

    action = solution.get(
        "recommended_action",
        ""
    )

    explanation = (

        f"NetSage AI identified the primary issue as: "
        f"{root} "

        f"This conclusion is supported by the supplied "
        f"network evidence. {technical_reason} "

        f"Recommended action: {action}"

    )

    return explanation


# =========================================================
# MAIN DIAGNOSIS FUNCTION
# =========================================================

def generate_diagnosis(
    symptom,
    topology,
    parsed_evidence,
    rule_checker,
    command_intelligence
):

    issues = get_issues(
        rule_checker
    )

    passes = get_passes(
        rule_checker
    )


    # -----------------------------------------------------
    # Determine root cause
    # -----------------------------------------------------

    root_cause = determine_root_cause(
        issues,
        symptom
    )


    issue_type = root_cause.get(
        "issue_type"
    )


    # -----------------------------------------------------
    # Generate solution
    # -----------------------------------------------------

    solution = generate_solution(
        issue_type,
        root_cause
    )


    # -----------------------------------------------------
    # Collect evidence
    # -----------------------------------------------------

    evidence = root_cause.get(
        "evidence",
        []
    )


    # If the primary rule does not provide evidence,
    # use parsed evidence as supporting context.

    if not evidence:

        evidence = (
            parsed_evidence
            if isinstance(
                parsed_evidence,
                dict
            )
            else {}
        )


    # -----------------------------------------------------
    # Explanation
    # -----------------------------------------------------

    explanation = generate_explanation(
        root_cause,
        solution,
        evidence
    )


    # -----------------------------------------------------
    # Recommended command
    # -----------------------------------------------------

    recommended_command = ""

    if isinstance(
        command_intelligence,
        dict
    ):

        recommended_command = (
            command_intelligence.get(
                "recommended_next_command",
                ""
            )
        )


    if not recommended_command:

        commands = solution.get(
            "recommended_commands",
            []
        )

        if commands:

            recommended_command = commands[0]


    # -----------------------------------------------------
    # Confidence
    # -----------------------------------------------------

    confidence = root_cause.get(
        "confidence",
        "Low"
    )


    # -----------------------------------------------------
    # Final diagnosis
    # -----------------------------------------------------

    return {

        "diagnosis_status": "completed",

        "analysis_mode": "local_reasoning",

        "root_cause": (
            root_cause.get(
                "root_cause"
            )
        ),

        "issue_type": issue_type,

        "confidence": confidence,

        "technical_reason": (
            root_cause.get(
                "technical_reason",
                ""
            )
        ),

        "evidence": evidence,

        "recommended_action": (
            solution.get(
                "recommended_action",
                ""
            )
        ),

        "recommended_commands": (
            solution.get(
                "recommended_commands",
                []
            )
        ),

        "recommended_next_command": (
            recommended_command
        ),

        "explanation": explanation,

        "validation_summary": {

            "issues_detected": len(
                issues
            ),

            "checks_passed": len(
                passes
            ),

            "overall_status": (
                rule_checker.get(
                    "overall_status",
                    "UNKNOWN"
                )
                if isinstance(
                    rule_checker,
                    dict
                )
                else "UNKNOWN"
            ),

        },

        "human_review": {

            "required": True,

            "reason": (
                "Network configuration changes should "
                "not be performed solely from automated "
                "recommendations."
            ),

        },

    }