def profile4_f1(d1):
    """
    there is a leg l1 in d1 such that l1 visits "CAI" and the flight-number of l1 is in {400, 401}
    ∃l1:@Leg ∈ $d1. (visits($l1, "CAI") ∧ flight-number($l1) ∈ {400, 401})
    """
    return any(visits(l1, 'CAI') and l1.flight_number in {400, 401} for l1 in d1)


profile4_f1(d1)
