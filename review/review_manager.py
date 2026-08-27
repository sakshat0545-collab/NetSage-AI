# =========================================================
# NETSAGE AI
# HUMAN REVIEW MANAGER
# =========================================================

import json
import os
from datetime import datetime


# =========================================================
# PATH CONFIGURATION
# =========================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

REVIEW_LOG_FILE = os.path.join(
    CURRENT_DIR,
    "review_log.json"
)


# =========================================================
# LOAD REVIEW LOG
# =========================================================

def load_reviews():
    """
    Load all previously saved human reviews.
    """

    if not os.path.exists(REVIEW_LOG_FILE):
        return []

    try:

        with open(
            REVIEW_LOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

    except (
        OSError,
        json.JSONDecodeError
    ):
        pass

    return []


# =========================================================
# SAVE REVIEW LOG
# =========================================================

def save_reviews(reviews):
    """
    Save all human reviews.
    """

    with open(
        REVIEW_LOG_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            reviews,
            file,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# CREATE REVIEW RECORD
# =========================================================

def create_review(
    case_id,
    ai_issue,
    ai_root_cause,
    ai_action,
    human_decision,
    human_issue=None,
    human_root_cause=None,
    human_action=None,
    reviewer_note=""
):
    """
    Create and save a human review record.

    human_decision:
        ACCEPT
        EDIT
        REJECT
    """

    decision = (
        human_decision
        .strip()
        .upper()
    )

    allowed_decisions = {
        "ACCEPT",
        "EDIT",
        "REJECT",
    }

    if decision not in allowed_decisions:
        raise ValueError(
            "Invalid human decision. "
            "Use ACCEPT, EDIT, or REJECT."
        )

    # If human accepts the AI recommendation,
    # the final result remains the AI result.

    if decision == "ACCEPT":

        final_issue = ai_issue
        final_root_cause = ai_root_cause
        final_action = ai_action

    # If human edits the recommendation,
    # use the human-provided correction.

    elif decision == "EDIT":

        final_issue = (
            human_issue
            if human_issue
            else ai_issue
        )

        final_root_cause = (
            human_root_cause
            if human_root_cause
            else ai_root_cause
        )

        final_action = (
            human_action
            if human_action
            else ai_action
        )

    # If human rejects the recommendation,
    # mark the automated recommendation as rejected.

    else:

        final_issue = (
            human_issue
            if human_issue
            else "Rejected AI diagnosis"
        )

        final_root_cause = (
            human_root_cause
            if human_root_cause
            else "AI recommendation rejected by reviewer"
        )

        final_action = (
            human_action
            if human_action
            else "Perform manual network investigation"
        )

    # Determine whether the human changed
    # the AI recommendation.

    human_correction = (
        decision in {
            "EDIT",
            "REJECT"
        }
    )

    review = {

        "review_id": (
            f"REV-"
            f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        ),

        "case_id": case_id,

        "timestamp": (
            datetime.now().isoformat()
        ),

        "ai_recommendation": {

            "issue": ai_issue,

            "root_cause": ai_root_cause,

            "recommended_action": ai_action,
        },

        "human_review": {

            "decision": decision,

            "issue": human_issue,

            "root_cause": human_root_cause,

            "recommended_action": human_action,

            "reviewer_note": reviewer_note,
        },

        "final_decision": {

            "issue": final_issue,

            "root_cause": final_root_cause,

            "recommended_action": final_action,
        },

        "human_correction": human_correction,
    }

    reviews = load_reviews()

    reviews.append(review)

    save_reviews(reviews)

    return review


# =========================================================
# REVIEW STATISTICS
# =========================================================

def get_review_statistics():
    """
    Return statistics about human reviews.
    """

    reviews = load_reviews()

    accepted = 0
    edited = 0
    rejected = 0
    corrections = 0

    for review in reviews:

        decision = (
            review
            .get("human_review", {})
            .get("decision")
        )

        if decision == "ACCEPT":
            accepted += 1

        elif decision == "EDIT":
            edited += 1

        elif decision == "REJECT":
            rejected += 1

        if review.get(
            "human_correction",
            False
        ):
            corrections += 1

    return {

        "total_reviews": len(reviews),

        "accepted": accepted,

        "edited": edited,

        "rejected": rejected,

        "human_corrections": corrections,
    }


# =========================================================
# GET CORRECTED CASES
# =========================================================

def get_corrected_reviews():
    """
    Return reviews where human review
    changed the automated recommendation.
    """

    reviews = load_reviews()

    return [
        review
        for review in reviews
        if review.get(
            "human_correction",
            False
        )
    ]


# =========================================================
# MODULE TEST
# =========================================================

if __name__ == "__main__":

    print("=" * 60)

    print(
        "NETSAGE AI - HUMAN REVIEW MANAGER"
    )

    print("=" * 60)

    statistics = (
        get_review_statistics()
    )

    print(
        f"Total reviews: "
        f"{statistics['total_reviews']}"
    )

    print(
        f"Accepted: "
        f"{statistics['accepted']}"
    )

    print(
        f"Edited: "
        f"{statistics['edited']}"
    )

    print(
        f"Rejected: "
        f"{statistics['rejected']}"
    )

    print(
        f"Human corrections: "
        f"{statistics['human_corrections']}"
    )

    print(
        "\nReview manager ready."
    )