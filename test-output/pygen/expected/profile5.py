def profile5_f1(l1):
    """
    the departure station of l1 is a base station and the arrival station of l1 is not a base station and (the departure station or the arrival station) of l1 is in {"HAV", "MIA", "IAD"}
    base-station(departure-station($l1)) ∧ ¬base-station(arrival-station($l1)) ∧ (departure-station($l1) ∈ {"HAV", "MIA", "IAD"} ∨ arrival-station($l1) ∈ {"HAV", "MIA", "IAD"})
    """
    return base_station(l1.departure_station) and not base_station(l1.arrival_station) and (l1.departure_station in {'HAV', 'MIA', 'IAD'} or l1.arrival_station in {'HAV', 'MIA', 'IAD'})


profile5_f1(l1)
