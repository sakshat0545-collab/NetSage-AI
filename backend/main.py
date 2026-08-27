# =========================================================
# NETSAGE AI
# BACKEND API
# =========================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import sys
import os
import ipaddress
import uuid


# =========================================================
# PROJECT PATH CONFIGURATION
# =========================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    CURRENT_DIR
)

CHECKER_DIR = os.path.join(
    PROJECT_ROOT,
    "checker"
)

AI_DIR = os.path.join(
    PROJECT_ROOT,
    "ai"
)

REVIEW_DIR = os.path.join(
    PROJECT_ROOT,
    "review"
)


if CHECKER_DIR not in sys.path:
    sys.path.append(CHECKER_DIR)

if AI_DIR not in sys.path:
    sys.path.append(AI_DIR)

if REVIEW_DIR not in sys.path:
    sys.path.append(REVIEW_DIR)


# =========================================================
# IMPORT PROJECT MODULES
# =========================================================

from evidence_parser import parse_evidence

from rule_checker import run_all_checks

from cisco_intelligence import (
    build_command_intelligence
)

from diagnosis_engine import (
    generate_diagnosis
)

from review_manager import (
    load_reviews,
    create_review,
    get_review_statistics,
    get_corrected_reviews
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="NetSage AI",
    description=(
        "AI-assisted network troubleshooting "
        "and Cisco diagnostic intelligence platform."
    ),
    version="1.0.0"
)


# =========================================================
# CORS CONFIGURATION
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# REQUEST MODEL
# =========================================================

class DiagnosisRequest(BaseModel):

    symptom: str

    topology: str

    show_output: str


# =========================================================
# HUMAN REVIEW REQUEST MODEL
# =========================================================

class ReviewRequest(BaseModel):

    case_id: str

    ai_issue: str

    ai_root_cause: str

    ai_action: str

    human_decision: str

    human_issue: str | None = None

    human_root_cause: str | None = None

    human_action: str | None = None

    reviewer_note: str = ""


# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
def root():

    return {
        "status": "online",

        "project": "NetSage AI",

        "message": (
            "Network Troubleshooting "
            "Assistant is running"
        ),
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",

        "service": "NetSage AI Backend",

        "components": {

            "evidence_parser": "online",

            "rule_checker": "online",

            "cisco_intelligence": "online",

            "diagnosis_engine": "online",

            "review_manager": "online",

        },
    }


# =========================================================
# DIAGNOSIS ENDPOINT
# =========================================================

@app.post("/api/diagnose")
def diagnose(
    request: DiagnosisRequest
):

    # -----------------------------------------------------
    # STEP 1
    # Create unique case ID
    # -----------------------------------------------------

    case_id = (
        f"CASE-"
        f"{uuid.uuid4().hex[:12].upper()}"
    )


    # -----------------------------------------------------
    # STEP 2
    # Build complete network case
    # -----------------------------------------------------

    case = {

        "case_id": case_id,

        "symptom": request.symptom,

        "topology": request.topology,

        "show_output": request.show_output,

    }


    # -----------------------------------------------------
    # STEP 3
    # Parse complete network evidence
    # -----------------------------------------------------

    parsed_evidence = parse_evidence(

        request.symptom,

        request.topology,

        request.show_output

    )


    # -----------------------------------------------------
    # STEP 4
    # Prepare host IP information
    # -----------------------------------------------------

    host_ips = (

        parsed_evidence.get(
            "host_ips"
        )

        or

        parsed_evidence.get(
            "ip_addresses"
        )

        or []

    )


    ip_address = (

        host_ips[0]

        if host_ips

        else None

    )


    subnet_masks = (

        parsed_evidence.get(
            "subnet_masks"
        )

        or []

    )


    subnet_mask = (

        subnet_masks[0]

        if subnet_masks

        else None

    )


    gateway = parsed_evidence.get(
        "gateway"
    )


    vlan_ids = (

        parsed_evidence.get(
            "vlan_ids"
        )

        or []

    )


    # -----------------------------------------------------
    # STEP 5
    # Determine required networks
    # -----------------------------------------------------

    networks = (

        parsed_evidence.get(
            "networks"
        )

        or []

    )


    required_networks = list(
        networks
    )


    if (
        ip_address
        and subnet_mask
    ):

        try:

            host_network = str(
                ipaddress.IPv4Network(
                    f"{ip_address}/{subnet_mask}",
                    strict=False
                )
            )


            required_networks = [

                network

                for network in required_networks

                if network != host_network

            ]


        except ValueError:

            pass


    # -----------------------------------------------------
    # STEP 6
    # Run deterministic rule checker
    # -----------------------------------------------------

    rule_results = run_all_checks(

        ip_addresses=host_ips,

        ip_address=ip_address,

        subnet_mask=subnet_mask,

        gateway=gateway,

        show_interfaces=request.show_output,

        show_vlan=request.show_output,

        required_vlans=vlan_ids,

        show_routes=request.show_output,

        required_networks=required_networks,

    )


    # -----------------------------------------------------
    # STEP 7
    # Detect Cisco commands
    # -----------------------------------------------------

    detected_commands = (

        parsed_evidence.get(
            "commands"
        )

        or []

    )


    # -----------------------------------------------------
    # STEP 8
    # Cisco command intelligence
    # -----------------------------------------------------

    command_intelligence = (
        build_command_intelligence(

            commands=detected_commands

        )
    )


    # -----------------------------------------------------
    # STEP 9
    # Determine primary issue
    # -----------------------------------------------------

    issue_type = None


    if isinstance(
        rule_results,
        dict
    ):

        results = rule_results.get(
            "results",
            []
        )


        for result in results:

            if (
                result.get(
                    "status"
                )
                == "ISSUE"
            ):

                issue_type = result.get(
                    "check"
                )

                break


    # -----------------------------------------------------
    # STEP 10
    # Issue-specific Cisco intelligence
    # -----------------------------------------------------

    if issue_type:

        recommended_command_intelligence = (

            build_command_intelligence(

                commands=detected_commands,

                issue_type=issue_type

            )

        )

    else:

        recommended_command_intelligence = (
            command_intelligence
        )


    # -----------------------------------------------------
    # STEP 11
    # Generate AI diagnosis
    # -----------------------------------------------------

    ai_diagnosis = generate_diagnosis(

        symptom=request.symptom,

        topology=request.topology,

        parsed_evidence=parsed_evidence,

        rule_checker=rule_results,

        command_intelligence=(
            recommended_command_intelligence
        )

    )


    # -----------------------------------------------------
    # STEP 12
    # Unified response
    # -----------------------------------------------------

    return {

        "status": "success",

        "message": (
            "Network evidence analyzed successfully"
        ),

        "case": case,

        "parsed_evidence": parsed_evidence,

        "rule_checker": rule_results,

        "cisco_intelligence": (
            recommended_command_intelligence
        ),

        "ai_diagnosis": ai_diagnosis,

        "human_review": {

            "required": True,

            "status": "PENDING",

            "message": (
                "AI and automated findings must "
                "be reviewed by a qualified human "
                "before network changes are accepted."
            ),

        },

    }


# =========================================================
# HUMAN REVIEW ENDPOINT
# =========================================================

@app.post("/api/review")
def submit_review(
    request: ReviewRequest
):

    try:

        review = create_review(

            case_id=request.case_id,

            ai_issue=request.ai_issue,

            ai_root_cause=request.ai_root_cause,

            ai_action=request.ai_action,

            human_decision=request.human_decision,

            human_issue=request.human_issue,

            human_root_cause=request.human_root_cause,

            human_action=request.human_action,

            reviewer_note=request.reviewer_note,

        )


        return {

            "status": "success",

            "message": (
                "Human review recorded successfully."
            ),

            "review": review,

        }


    except ValueError as error:

        raise HTTPException(

            status_code=400,

            detail=str(error)

        )


    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=(
                "Unable to save human review: "
                f"{error}"
            )

        )


# =========================================================
# REVIEW HISTORY ENDPOINT
# =========================================================

@app.get("/api/reviews")
def review_history():

    reviews = load_reviews()

    return {

        "status": "success",

        "total": len(reviews),

        "reviews": reviews,

    }


# =========================================================
# REVIEW STATISTICS ENDPOINT
# =========================================================

@app.get("/api/reviews/statistics")
def review_statistics():

    statistics = (
        get_review_statistics()
    )

    return {

        "status": "success",

        "statistics": statistics,

    }


# =========================================================
# CORRECTED REVIEWS ENDPOINT
# =========================================================

@app.get("/api/reviews/corrected")
def corrected_reviews():

    reviews = (
        get_corrected_reviews()
    )

    return {

        "status": "success",

        "total": len(reviews),

        "reviews": reviews,

    }


# =========================================================
# SERVER INFORMATION
# =========================================================

@app.get("/api/info")
def api_info():

    return {

        "name": "NetSage AI",

        "version": "1.0.0",

        "purpose": (
            "Evidence-based Cisco network "
            "troubleshooting assistant"
        ),

        "modules": [

            "Evidence Parser",

            "Deterministic Rule Checker",

            "Cisco Command Intelligence",

            "AI Diagnosis Engine",

            "Human Review Manager",

            "Review History",

        ],

        "endpoints": [

            "GET /",

            "GET /health",

            "POST /api/diagnose",

            "POST /api/review",

            "GET /api/reviews",

            "GET /api/reviews/statistics",

            "GET /api/reviews/corrected",

            "GET /api/info",

        ],

    }