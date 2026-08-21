# ==========================================
# QUESTION 4
# CLINIC PATIENT STATUS CLASSIFICATION SYSTEM
# ==========================================
#
# NOTE: The categories below are supplied strictly as PROGRAMMING RULES
# for this exercise and should NOT be treated as medical advice.
#
# Data structures used:
#   - list of tuples: raw patient records (name, systolic, diastolic)
#   - lists: normal_patients, at_risk_patients, urgent_patients
#
# Classification rule: a patient is classified by whichever reading
# (systolic or diastolic) reaches the MORE SERIOUS category.

# ---- Thresholds (named, not hard-coded) ----
NORMAL_SYSTOLIC_MAX = 120     # below this
NORMAL_DIASTOLIC_MAX = 80     # below this
ELEVATED_SYSTOLIC_MAX = 140   # 120-139
ELEVATED_DIASTOLIC_MAX = 90   # 80-89
STAGE1_SYSTOLIC_MAX = 160     # 140-159
STAGE1_DIASTOLIC_MAX = 100    # 90-99
# Stage 2 / Urgent: systolic >= 160 OR diastolic >= 100


def classify_patient(systolic, diastolic):
    """Return the classification string for one patient's readings."""
    # Check from most serious to least serious, so the "more serious" rule wins.
    if systolic >= STAGE1_SYSTOLIC_MAX or diastolic >= STAGE1_DIASTOLIC_MAX:
        return "Stage 2 / Urgent"
    elif systolic >= ELEVATED_SYSTOLIC_MAX or diastolic >= ELEVATED_DIASTOLIC_MAX:
        return "Stage 1"
    elif systolic >= NORMAL_SYSTOLIC_MAX or diastolic >= NORMAL_DIASTOLIC_MAX:
        return "Elevated"
    else:
        return "Normal"


def categorize_patients(patients):
    """Classify every patient and sort into normal / at-risk / urgent lists.
    Elevated + Stage 1 are grouped together as 'at-risk'.
    Returns: dict with keys 'normal', 'at_risk', 'urgent', plus a full detail list.
    """
    normal_patients = []
    at_risk_patients = []
    urgent_patients = []
    details = []   # (name, systolic, diastolic, classification)

    for name, systolic, diastolic in patients:
        classification = classify_patient(systolic, diastolic)
        details.append((name, systolic, diastolic, classification))

        if classification == "Normal":
            normal_patients.append(name)
        elif classification in ("Elevated", "Stage 1"):
            at_risk_patients.append(name)
        else:  # Stage 2 / Urgent
            urgent_patients.append(name)

    return {
        "normal": normal_patients,
        "at_risk": at_risk_patients,
        "urgent": urgent_patients,
        "details": details,
    }


def calculate_average_readings(patients):
    """Return (average_systolic, average_diastolic)."""
    if not patients:
        return 0, 0
    total_systolic = sum(p[1] for p in patients)
    total_diastolic = sum(p[2] for p in patients)
    count = len(patients)
    return total_systolic / count, total_diastolic / count


def generate_urgent_alerts(details):
    """Generate an alert message for each urgent patient."""
    alerts = []
    for name, systolic, diastolic, classification in details:
        if classification == "Stage 2 / Urgent":
            alerts.append(
                f"ALERT: {name} requires immediate attention "
                f"(BP {systolic}/{diastolic})"
            )
    return alerts


def find_followup_patients(details):
    """Patients needing follow-up = anyone not classified Normal."""
    followup = [name for name, s, d, classification in details if classification != "Normal"]
    return followup


def generate_report(patients):
    result = categorize_patients(patients)
    details = result["details"]
    avg_systolic, avg_diastolic = calculate_average_readings(patients)
    alerts = generate_urgent_alerts(details)
    followup = find_followup_patients(details)

    print("=" * 50)
    print("CLINIC PATIENT STATUS REPORT")
    print("(Programming exercise only - not medical advice)")
    print("=" * 50)

    print("\n--- Individual Classifications ---")
    for name, systolic, diastolic, classification in details:
        print(f"{name}: {systolic}/{diastolic} -> {classification}")

    print(f"\nAverage Systolic: {avg_systolic:.1f}")
    print(f"Average Diastolic: {avg_diastolic:.1f}")

    print("\n--- Urgent Alerts ---")
    if alerts:
        for alert in alerts:
            print(alert)
    else:
        print("None")

    print("\n--- Patients Requiring Follow-up ---")
    print(", ".join(followup) if followup else "None")

    print("\n--- Summary Counts ---")
    print(f"Normal: {len(result['normal'])}")
    print(f"At-Risk: {len(result['at_risk'])}")
    print(f"Urgent: {len(result['urgent'])}")
    print("=" * 50)

    return result


# ---------------- TESTING ----------------
if __name__ == "__main__":
    # 1) Supplied dataset
    patients = [
        ("Alice", 115, 75),
        ("Brian", 128, 84),
        ("Carol", 145, 95),
        ("Daniel", 165, 105),
        ("Grace", 118, 78),
    ]
    print("### TEST 1: SUPPLIED DATASET ###")
    generate_report(patients)

    # 2) Additional dataset: normal case + edge case
    #    - normal: a clearly normal and a clearly elevated patient
    #    - edge: exactly on a boundary (120/80 -> Elevated, not Normal)
    #            and diastolic driving the classification higher than systolic suggests
    extra_patients = [
        ("Edith", 110, 70),     # normal case
        ("Frank", 120, 80),     # edge: exactly at Elevated boundary
        ("Ivan", 118, 101),     # edge: systolic looks normal, but diastolic pushes to Urgent
    ]
    print("\n### TEST 2: ADDITIONAL DATASET (edge cases included) ###")
    generate_report(extra_patients)
