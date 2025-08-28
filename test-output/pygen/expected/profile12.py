def profile12_f1(d1):
    """
    there is a Leg l1 in d1 such that l1 visits "LAX" and for all Leg l2 in d1, the type of l2 is not "Travel"
    ∃l1:@Leg ∈ $d1. (visits($l1, "LAX") ∧ ∀l2:@Leg ∈ $d1. type($l2) ≠ "Travel")
    """
    return any(visits(l1, 'LAX') and all(l2.type != 'Travel' for l2 in d1) for l1 in d1)


profile12_f1(d1)
