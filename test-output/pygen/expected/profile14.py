def profile14_f1(p1):
    """
    there is a Leg l1 in p1 such that l1 visits USA and there is a Leg l2 in p1 such that the type of l2 is "Travel"
    ∃l1:@Leg ∈ $p1. (visits($l1, USA) ∧ ∃l2:@Leg ∈ $p1. type($l2) = "Travel")
    """
    return any(visits(l1, USA) and any(l2.type == 'Travel' for l2 in p1) for l1 in p1)


profile14_f1(p1)
