def profile9_f1(d1):
    """
    every Leg l1 of d1 is abroad, and the arrival station of l1 is not a base station and the duration of d1 is at most 12
    ∀l1:@Leg ∈ $d1. (abroad($l1) ∧ ¬base-station(arrival-station($l1)) ∧ duration($d1) ≤ 12)
    """
    return all(abroad(l1) and not base_station(l1.arrival_station) and d1.duration <= 12 for l1 in d1)


profile9_f1(d1)
