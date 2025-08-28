from optimistic_rt.temporal import t_meets_inv
from optimistic_rt.util import unique_element


def profile18_f3(p1):
    """
    there are Duties d1 and d2 in p1 such that d1 has one Leg l1 and d2 has one Leg l2 such that the departure station of l1 is "SVO" and the arrival station of l2 is "KJA" and d2 immediately follows d1 in p1
    ∃d1:@Duty ∈ $p1. ∃d2:@Duty ∈ $p1. ∃!l1:@Leg ∈ $d1. ∃!l2:@Leg ∈ $d2. (departure-station($l1) = "SVO" ∧ arrival-station($l2) = "KJA" ∧ *t-meets-inverse*($d2, $d1, $p1))
    """
    def profile18_f2(d1, d2, p1):
        """
        d1 has one Leg l1 and d2 has one Leg l2 such that the departure station of l1 is "SVO" and the arrival station of l2 is "KJA" and d2 immediately follows d1 in p1
        """
        def profile18_f1(d1, d2, l1, p1):
            l2 = unique_element(d2)
            return l2 is not None and l1.departure_station == 'SVO' and l2.arrival_station == 'KJA' and t_meets_inv(d2, d1, p1)
        l1 = unique_element(d1)
        return l1 is not None and profile18_f1(d1, d2, l1, p1)
    return any(any(profile18_f2(d1, d2, p1) for d2 in p1) for d1 in p1)


profile18_f3(p1)
