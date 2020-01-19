# /usr/bin/python
# -*- coding: utf-8 -*-
"""
Tests this query searchs a document, highlights a snippit and returns it
http://www.example.com/search?find_desc=deep+dish+pizza&ns=1&rpp=10&find_loc=\
                                                        San+Francisco%2C+CA

Contains both unit and functional tests.

"""


import unittest
from highlight import HighlightDocumentOperations


class TestHighlight(unittest.TestCase):
    def setUp(self):

        self.document = """
Review for their take-out only.
Tried their large Classic (sausage, mushroom, peppers and onions) deep dish;\
and their large Pesto Chicken thin crust pizzas.
Pizza = I've had better.  The crust/dough was just way too effin' dry for me.\
Yes, I know what 'cornmeal' is, thanks.  But it's way too dry.\
I'm not talking about the bottom of the pizza...I'm talking about the dough \
that's in between the sauce and bottom of the pie...it was like cardboard, sorry!
Wings = spicy and good.   Bleu cheese dressing only...hmmm, but no alternative\
of ranch dressing, at all.  Service = friendly enough at the counters.  
Decor = freakin' dark.  I'm not sure how people can see their food.  
Parking = a real pain.  Good luck.        
        
        """
        self.query = "deep+dish+pizza"
        self.hdo = HighlightDocumentOperations(self.document, self.query)

    def test_custom_highlight_tag(self):

        actual = self.hdo._custom_highlight_tag("foo", start="[BAR]", end="[ENDBAR]")
        expected = "[BAR]foo[ENDBAR]"
        self.assertEqual(actual, expected)

    def test_query_string_to_dict(self):
        """Verifies the yielded results are what is expected"""

        result = self.hdo._querystring_to_dict()
        expected = {
            "deep": "<strong>deep</strong>",
            "dish": "<strong>dish</strong>",
            "pizza": "<strong>pizza</strong>",
        }

        self.assertEqual(result, expected)

    def test_multi_string_replace(self):

        query = """pizza = I've had better"""
        expected = """<strong>pizza</strong> = I've had better"""
        query_dict = self.hdo._querystring_to_dict()
        result = self.hdo._multiple_string_replace(query, query_dict)
        self.assertEqual(expected, result)

    def test_doc_to_sentences(self):
        """Consumes the generator, and then verifies the result[0]"""

        results = []
        expected = (0, "\nReview for their take-out only.")

        for sentence in self.hdo._doc_to_sentences():
            results.append(sentence)
        self.assertEqual(results[0], expected)

    def test_highlight(self):
        """Verifies highlighted text is what we expect"""

        expected = """Tried their large Classic (sausage, mushroom, peppers and onions) <strong>deep</strong> <strong>dish</strong>;and their large Pesto Chicken thin crust <strong>pizza</strong>s."""
        actual = self.hdo.highlight_doc()
        self.assertEqual(expected, actual)

    def tearDown(self):

        del self.query
        del self.hdo
        del self.document


if __name__ == "__main__":
    unittest.main()
