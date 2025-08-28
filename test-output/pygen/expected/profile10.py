def profile10_f1(t1):
    """
    there is a Leg l1 in t1 such that the activity of l1 is "ALV"
    ∃l1:@Leg ∈ $t1. activity($l1) = "ALV"
    """
    return any(l1.activity == 'ALV' for l1 in t1)


profile10_f1(t1)
