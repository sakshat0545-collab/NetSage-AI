# =========================================================
# NETSAGE AI
# CASE DATASET LOADER
# =========================================================

import csv
import os


# =========================================================
# PATH CONFIGURATION
# =========================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CASE_FILE = os.path.join(
    CURRENT_DIR,
    "cases.csv"
)


# =========================================================
# LOAD ALL CASES
# =========================================================

def load_cases():
    """
    Load all troubleshooting cases from cases.csv.
    """

    cases = []

    if not os.path.exists(CASE_FILE):
        return cases

    try:

        with open(
            CASE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                cases.append(dict(row))

    except (OSError, csv.Error):
        return []

    return cases


# =========================================================
# FIND CASE BY ID
# =========================================================

def get_case_by_id(case_id):
    """
    Return a specific troubleshooting case.
    """

    cases = load_cases()

    for case in cases:

        if case.get("case_id") == case_id:
            return case

    return None


# =========================================================
# FILTER CASES BY CATEGORY
# =========================================================

def get_cases_by_category(category):
    """
    Return all cases belonging to a category.
    """

    cases = load_cases()

    return [
        case
        for case in cases
        if case.get("category", "").lower()
        == category.lower()
    ]


# =========================================================
# SEARCH CASES
# =========================================================

def search_cases(keyword):
    """
    Search troubleshooting cases using
    symptom, category, root cause,
    or issue type.
    """

    cases = load_cases()

    keyword = keyword.lower().strip()

    if not keyword:
        return []

    matches = []

    for case in cases:

        searchable_text = " ".join([
            case.get("category", ""),
            case.get("symptom", ""),
            case.get("expected_issue", ""),
            case.get("expected_root_cause", ""),
            case.get("evidence", ""),
        ]).lower()

        if keyword in searchable_text:
            matches.append(case)

    return matches


# =========================================================
# GET DATASET STATISTICS
# =========================================================

def get_case_statistics():
    """
    Return basic dataset statistics.
    """

    cases = load_cases()

    categories = {}

    for case in cases:

        category = case.get(
            "category",
            "Unknown"
        )

        categories[category] = (
            categories.get(category, 0) + 1
        )

    return {
        "total_cases": len(cases),
        "categories": categories,
    }


# =========================================================
# MODULE TEST
# =========================================================

if __name__ == "__main__":

    cases = load_cases()

    print("=" * 60)
    print("NETSAGE AI - CASE DATASET")
    print("=" * 60)

    print(
        f"Total cases loaded: {len(cases)}"
    )

    statistics = get_case_statistics()

    print("\nCategories:")

    for category, count in (
        statistics["categories"].items()
    ):
        print(
            f"{category}: {count}"
        )

    print("\nDataset loader ready.")