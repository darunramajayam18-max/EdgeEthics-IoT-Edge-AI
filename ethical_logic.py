
def calculate_ethical_score(person_detected, person_id, temperature):
    """
    Calculate Safety, Privacy and Ethical Score.

    Score:
    Safety        = 40 points
    Privacy       = 40 points
    Accountability = 20 points

    These are prototype rules and should be validated.
    """

    # -------------------------
    # NO PERSON DETECTED
    # -------------------------
    if not person_detected:
        return {
            "safety": "—",
            "privacy": "—",
            "ethical_score": "—"
        }

    # -------------------------
    # SAFETY CHECK
    # -------------------------
    # Do not treat missing temperature as safe.
    if temperature is None:
        safety = "REVIEW"
    elif temperature <= 35:
        safety = "PASS"
    else:
        safety = "FAIL"

    # -------------------------
    # PRIVACY CHECK
    # -------------------------
    # Only a registered identity should pass.
    # Update this condition if your recognition
    # code uses a different unknown-person label.
    registered = (
        person_id is not None
        and str(person_id).strip() != ""
        and str(person_id).strip().lower()
        not in {"unknown", "unregistered", "—", "none"}
    )

    privacy = "PASS" if registered else "FAIL"

    # -------------------------
    # ACCOUNTABILITY CHECK
    # -------------------------
    # A detected person and an available identity
    # result must be present for this basic check.
    accountability = (
        "PASS" if person_id is not None
        and str(person_id).strip() != ""
        else "FAIL"
    )

    # -------------------------
    # DYNAMIC ETHICAL SCORE
    # -------------------------
    score = 0

    if safety == "PASS":
        score += 40

    if privacy == "PASS":
        score += 40

    if accountability == "PASS":
        score += 20

    # If a required input is unavailable, avoid
    # presenting the result as a fully evaluated score.
    if safety == "REVIEW":
        ethical_score = "REVIEW"
    else:
        ethical_score = score

    return {
        "safety": safety,
        "privacy": privacy,
        "ethical_score": ethical_score
    }
