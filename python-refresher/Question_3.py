# ==========================================
# QUESTION 3
# SMALL BUSINESS SALES PERFORMANCE MONITOR
# ==========================================
#
# Data structures used:
#   - list of tuples: raw sales records (day, salesperson, phone_brand, amount)
#   - dictionaries: aggregate totals by salesperson, by brand, and by day
#
# Assumptions:
#   - "Top performer" is based on total weekly sales amount, not number of sales.
#   - Ties at the top all receive the top-performer bonus (as required).

TOP_BONUS = 50000        # UGX
STANDARD_BONUS = 20000   # UGX
SLOW_DAY_THRESHOLD = 2000000  # UGX


def total_sales_per_person(sales):
    totals = {}
    for day, person, brand, amount in sales:
        totals[person] = totals.get(person, 0) + amount
    return totals


def find_top_performers(person_totals):
    """Return list of all salespeople tied for the highest total (handles ties)."""
    if not person_totals:
        return [], 0
    highest = max(person_totals.values())
    top_performers = [person for person, total in person_totals.items() if total == highest]
    return top_performers, highest


def award_bonuses(person_totals, top_performers):
    """Return dict {person: bonus_amount} applying the bonus rule."""
    bonuses = {}
    for person in person_totals:
        if person in top_performers:            # conditional: is this person top?
            bonuses[person] = TOP_BONUS
        else:
            bonuses[person] = STANDARD_BONUS
    return bonuses


def revenue_per_brand(sales):
    brand_totals = {}
    for day, person, brand, amount in sales:
        brand_totals[brand] = brand_totals.get(brand, 0) + amount
    return brand_totals


def find_top_brand(brand_totals):
    top_brand = None
    highest = 0
    for brand, total in brand_totals.items():
        if total > highest:
            highest = total
            top_brand = brand
    return top_brand, highest


def sales_per_day(sales):
    day_totals = {}
    for day, person, brand, amount in sales:
        day_totals[day] = day_totals.get(day, 0) + amount
    return day_totals


def find_slow_days(day_totals):
    slow_days = []
    for day, total in day_totals.items():
        if total < SLOW_DAY_THRESHOLD:          # conditional check
            slow_days.append((day, total))
    return slow_days


def generate_report(sales):
    person_totals = total_sales_per_person(sales)
    top_performers, top_amount = find_top_performers(person_totals)
    bonuses = award_bonuses(person_totals, top_performers)
    brand_totals = revenue_per_brand(sales)
    top_brand, top_brand_amount = find_top_brand(brand_totals)
    day_totals = sales_per_day(sales)
    slow_days = find_slow_days(day_totals)

    print("=" * 50)
    print("WEEKLY SALES PERFORMANCE REPORT")
    print("=" * 50)

    print("\n--- Total Weekly Sales per Salesperson ---")
    for person, total in person_totals.items():
        print(f"{person}: {total:,} UGX")

    print(f"\nTop Performer(s): {', '.join(top_performers)} ({top_amount:,} UGX)")

    print("\n--- Bonuses Awarded ---")
    for person, bonus in bonuses.items():
        print(f"{person}: {bonus:,} UGX")

    print("\n--- Revenue per Phone Brand ---")
    for brand, total in brand_totals.items():
        print(f"{brand}: {total:,} UGX")
    print(f"Top Brand: {top_brand} ({top_brand_amount:,} UGX)")

    print("\n--- Total Sales per Day ---")
    for day, total in day_totals.items():
        print(f"{day}: {total:,} UGX")

    print(f"\n--- Slow Days (< {SLOW_DAY_THRESHOLD:,} UGX) ---")
    if slow_days:
        for day, total in slow_days:
            print(f"{day}: {total:,} UGX")
    else:
        print("None")

    print("=" * 50)

    return {
        "person_totals": person_totals,
        "top_performers": top_performers,
        "bonuses": bonuses,
        "brand_totals": brand_totals,
        "top_brand": top_brand,
        "day_totals": day_totals,
        "slow_days": slow_days,
    }


# ---------------- TESTING ----------------
if __name__ == "__main__":
    # 1) Supplied dataset
    sales = [
        ("Monday", "Alice", "Samsung", 1200000),
        ("Monday", "Brian", "Tecno", 850000),
        ("Tuesday", "Alice", "iPhone", 2500000),
        ("Tuesday", "Charles", "Samsung", 1100000),
        ("Wednesday", "Brian", "Infinix", 900000),
        ("Wednesday", "Alice", "Samsung", 1600000),
        ("Thursday", "Charles", "Tecno", 700000),
        ("Friday", "Brian", "Samsung", 2300000),
    ]
    print("### TEST 1: SUPPLIED DATASET ###")
    generate_report(sales)

    # 2) Additional dataset: normal case + edge case
    #    - normal: ordinary sales spread across the week
    #    - edge: a tie for top performer, and a day with total sales exactly at threshold
    extra_sales = [
        ("Monday", "Denis", "Samsung", 1000000),
        ("Monday", "Denis", "iPhone", 1000000),      # Denis total = 2,000,000 -> edge: exactly threshold day
        ("Tuesday", "Fiona", "Tecno", 2000000),       # Fiona total = 2,000,000 -> ties with Denis for top
        ("Wednesday", "George", "Infinix", 500000),
    ]
    print("\n### TEST 2: ADDITIONAL DATASET (edge cases: tie for top, threshold-exact day) ###")
    generate_report(extra_sales)
