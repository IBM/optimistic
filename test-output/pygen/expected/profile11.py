from optimistic_rt import Period, Time
from optimistic_rt.util import period_intersection, period_length


def profile11_f1(t1):
    """
    there is a Leg l1 in t1 such that the activity of l1 is "SBY" and the length of (the intersection of the period of l1 and 08:00-20:00) is at least 20% of 12 and the type of the aircraft of l1 is in {"77W", "333", "332"}
    ∃l1:@Leg ∈ $t1. (activity($l1) = "SBY" ∧ length(intersection(period($l1), [08:00-20:00])) ≥ %*(20%, 12) ∧ type(aircraft($l1)) ∈ {"77W", "333", "332"})
    """
    return any(l1.activity == 'SBY' and period_length(period_intersection(l1.period, Period(Time('08:00'), Time('20:00')))) >= 20 / 100 * 12 and l1.aircraft.type in {'77W', '333', '332'} for l1 in t1)


profile11_f1(t1)
