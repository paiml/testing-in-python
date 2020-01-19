"""Functional Test That Performs Some Basic Sanity Checks"""

from highlight import HighlightDocumentOperations


def test_snippit_algorithm():
    document1 = """
        This place has awesome deep dish pizza.
        I have been getting delivery through Waiters on wheels for years.
        It is classic, deep dish  Chicago style pizza.
        Now I found out they also have half-baked to pick-up and cook at home.
        This is a great benefit. I am having it tonight. Yum.
        """
    document2 = """Review for their take-out only.
Tried their large Classic (sausage, mushroom, peppers and onions) deep dish;\
and their large Pesto Chicken thin crust pizzas.
Pizza = I've had better.  The crust/dough was just way too effin' dry for me.\
Yes, I know what 'cornmeal' is, thanks.  But it's way too dry.\
I'm not talking about the bottom of the pizza...I'm talking about the dough \
that's in between the sauce and bottom of the pie...it was like cardboard, sorry!
Wings = spicy and good.   Bleu cheese dressing only...hmmm, but no alternative\
of ranch dressing, at all.  Service = friendly enough at the counters.  
Decor = freakin' dark.  I'm not sure how people can see their food.  
Parking = a real pain.  Good luck."""

    h1 = HighlightDocumentOperations(document1, "deep+dish+pizza")
    actual = h1.highlight_doc()
    print "Raw Document1: %s" % document1
    print " Formatted Document1: %s" % actual
    assert len(actual) < 500
    assert "<strong>" in actual

    h2 = HighlightDocumentOperations(document2, "deep+dish+pizza")
    actual = h2.highlight_doc()
    print "Raw Document2: %s" % document2
    print " Formatted Document2: %s" % actual
    assert len(actual) < 500
    assert "<strong>" in actual


if __name__ == "__main__":
    test_snippit_algorithm()
