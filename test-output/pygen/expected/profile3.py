def profile3_f1(d1):
    """
    the departure station of the first Leg of d1 is a base station and the arrival station of the last leg of d1 is not a base station
    base-station(departure-station(first-Leg($d1))) ∧ ¬base-station(arrival-station(last-leg($d1)))
    """
    return base_station(d1.first_Leg.departure_station) and not base_station(d1.last_leg.arrival_station)


profile3_f1(d1)
