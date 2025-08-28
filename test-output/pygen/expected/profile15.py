def profile15_f1(d1):
    """
    there are Legs l1, l2, l3 in d1 such that for each l0 in {l1, l2, l3}, l0 is operational and the flight-number of l0 is in {2800, 1370, 1226, 2100, 2118}
    ∃l1:@Leg ∈ $d1. ∃l2:@Leg ∈ $d1. ∃l3:@Leg ∈ $d1. ∀l0 ∈ {$l1, $l2, $l3}. (operational($l0) ∧ flight-number($l0) ∈ {2800, 1370, 1226, 2100, 2118})
    """
    return any(any(any(all(operational(l0) and l0.flight_number in {2800, 1370, 1226, 2100, 2118} for l0 in {l1, l2, l3}) for l3 in d1) for l2 in d1) for l1 in d1)


profile15_f1(d1)
