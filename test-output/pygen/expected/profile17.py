from optimistic_rt.temporal import t_after


def profile17_f1(p1):
    """
    the departure station of the first Leg of p1 is "SVO" and there are Legs l1 and l2 in p1 such that l2 follows l1 in p and l1 visits X and l2 visits Y
    departure-station(first-Leg($p1)) = "SVO" ∧ ∃l1:@Leg ∈ $p1. ∃l2:@Leg ∈ $p1. (*t-after*($l2, $l1, p) ∧ visits($l1, X) ∧ visits($l2, Y))
    """
    return p1.first_Leg.departure_station == 'SVO' and any(any(t_after(l2, l1, p) and visits(l1, X) and visits(l2, Y) for l2 in p1) for l1 in p1)


profile17_f1(p1)
