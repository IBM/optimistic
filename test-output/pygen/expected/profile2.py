def profile2_f1(d1):
    """
    the sum of the duration of l1 for all Legs l1 in d1 such that the type of l1 is in {"Flight", "Travel", "Other-carrier", "Simulator"} is at least 12
    Σ duration($l1) FOR l1:@Leg IN $d1 S.T. type($l1) ∈ {"Flight", "Travel", "Other-carrier", "Simulator"} ≥ 12
    """
    return sum(l1.duration for l1 in d1 if l1.type in {'Flight', 'Travel', 'Other-carrier', 'Simulator'}) >= 12


profile2_f1(d1)
