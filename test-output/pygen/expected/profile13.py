def profile13_f1(d1):
    """
    there are different Legs l1, l2 in d1 such that l1 is operational and l2 is operational and the type of the aircraft of l1 is "77W" and the type of the aircraft of l2 is "77W" and the flight-number of (l1 or l2) is 504
    ∃l1:@Leg ∈ $d1. ∃l2:@Leg ∈ $d1. (*different*($l1, $l2) ∧ operational($l1) ∧ operational($l2) ∧ type(aircraft($l1)) = "77W" ∧ type(aircraft($l2)) = "77W" ∧ (flight-number($l1) = 504 ∨ flight-number($l2) = 504))
    """
    return any(any(l1 != l2 and operational(l1) and operational(l2) and l1.aircraft.type == '77W' and l2.aircraft.type == '77W' and (l1.flight_number == 504 or l2.flight_number == 504) for l2 in d1) for l1 in d1)


profile13_f1(d1)
