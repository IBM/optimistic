def profile16_f1(p1):
    """
    the departure station of the first Leg of p1 is "SVO" and there is a Duty d1 in p1 such that the departure station of the first Leg of d1 is "KJA" and d1 is not quicky
    departure-station(first-Leg($p1)) = "SVO" ∧ ∃d1:@Duty ∈ $p1. (departure-station(first-Leg($d1)) = "KJA" ∧ ¬quicky($d1))
    """
    return p1.first_Leg.departure_station == 'SVO' and any(d1.first_Leg.departure_station == 'KJA' and not quicky(d1) for d1 in p1)


profile16_f1(p1)
