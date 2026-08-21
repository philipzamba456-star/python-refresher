# ==========================================
# QUESTION 2
# COMMUNITY LIBRARY BOOK DONATION MANAGER
# ==========================================
#
# Data structures used:
#   - list of tuples: raw donations (donor_name, genre, number_of_books)
#   - dictionaries: aggregate totals by donor and by genre
#
# Assumptions:
#   - A donor can appear multiple times (e.g. Alice donates Fiction, then Technology);
#     their totals must be summed across all their records.

GOLD_DONOR_THRESHOLD = 5   # books, minimum to qualify as a Gold Donor
TOP_DONORS_COUNT = 3


def total_books_per_donor(donations):
    """Returns dict {donor_name: total_books_donated}"""
    donor_totals = {}
    for donor, genre, books in donations:
        donor_totals[donor] = donor_totals.get(donor, 0) + books
    return donor_totals


def total_books_per_genre(donations):
    """Returns dict {genre: total_books}"""
    genre_totals = {}
    for donor, genre, books in donations:
        genre_totals[genre] = genre_totals.get(genre, 0) + books
    return genre_totals


def find_gold_donors(donor_totals):
    """Gold donors = donors with total books >= threshold."""
    gold_donors = []
    for donor, total in donor_totals.items():
        if total >= GOLD_DONOR_THRESHOLD:      # conditional check
            gold_donors.append((donor, total))
    return gold_donors


def overall_books_donated(donor_totals):
    return sum(donor_totals.values())


def find_most_popular_genre(genre_totals):
    most_popular = None
    highest = 0
    for genre, total in genre_totals.items():
        if total > highest:
            highest = total
            most_popular = genre
    return most_popular, highest


def top_donors(donor_totals, count=TOP_DONORS_COUNT):
    """Sort donors by total books, descending, return top `count`."""
    sorted_donors = sorted(donor_totals.items(), key=lambda item: item[1], reverse=True)
    return sorted_donors[:count]


def generate_report(donations):
    donor_totals = total_books_per_donor(donations)
    genre_totals = total_books_per_genre(donations)
    gold_donors = find_gold_donors(donor_totals)
    total_books = overall_books_donated(donor_totals)
    popular_genre, popular_genre_count = find_most_popular_genre(genre_totals)
    top3 = top_donors(donor_totals)

    print("=" * 50)
    print("LIBRARY DONATION REPORT")
    print("=" * 50)

    print("\n--- Total Books per Donor ---")
    for donor, total in donor_totals.items():
        print(f"{donor}: {total} books")

    print("\n--- Total Books per Genre ---")
    for genre, total in genre_totals.items():
        print(f"{genre}: {total} books")

    print(f"\n--- Gold Donors (>= {GOLD_DONOR_THRESHOLD} books) ---")
    if gold_donors:
        for donor, total in gold_donors:
            print(f"{donor}: {total} books")
    else:
        print("None")

    print(f"\nTotal Books Donated Overall: {total_books}")
    print(f"Most Popular Genre: {popular_genre} ({popular_genre_count} books)")

    print(f"\n--- Top {TOP_DONORS_COUNT} Donors ---")
    for rank, (donor, total) in enumerate(top3, start=1):
        print(f"{rank}. {donor} - {total} books")

    print("=" * 50)

    return {
        "donor_totals": donor_totals,
        "genre_totals": genre_totals,
        "gold_donors": gold_donors,
        "total_books": total_books,
        "most_popular_genre": popular_genre,
        "top_donors": top3,
    }


# ---------------- TESTING ----------------
if __name__ == "__main__":
    # 1) Supplied dataset
    donations = [
        ("Alice", "Fiction", 3),
        ("Brian", "Technology", 6),
        ("Carol", "History", 2),
        ("Alice", "Technology", 3),
        ("Daniel", "Fiction", 7),
        ("Grace", "Science", 5),
    ]
    print("### TEST 1: SUPPLIED DATASET ###")
    generate_report(donations)

    # 2) Additional dataset: normal case + edge case
    #    - normal: a few ordinary donors
    #    - edge: a donor at exactly the Gold threshold (5), and a donor with 0 books
    extra_donations = [
        ("Esther", "Fiction", 4),
        ("Esther", "History", 1),   # Esther total = 5 -> edge case, exactly Gold threshold
        ("Moses", "Science", 0),    # edge case: zero-book donation record
        ("Ruth", "Technology", 9),
    ]
    print("\n### TEST 2: ADDITIONAL DATASET (edge cases included) ###")
    generate_report(extra_donations)
