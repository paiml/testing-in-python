# /usr/bin/python
# -*- coding: utf-8 -*-

"""
:mod:`highlight` -- Highlight Methods
===================================

.. module:: highlight
   :platform: Unix, Windows
   :synopsis: highlight document snippets that match a query.
.. moduleauthor:: Noah Gift <noah.gift@gmail.com>

Requirements::
    1.  You will need to install the ntlk library to run this code.
        http://www.nltk.org/download
    2.  You will need to download the data for the ntlk:
        See http://www.nltk.org/data::
        
        import nltk
        nltk.download()

"""

import re
import logging

import nltk

# Globals
logging.basicConfig()
LOG = logging.getLogger("highlight")
LOG.setLevel(logging.INFO)


class HighlightDocumentOperations(object):

    """Highlight Operations for a Document"""

    def __init__(self, document=None, query=None):
        """
        Kwargs:
            document (str):
            query (str):
            
        """
        self._document = document
        self._query = query

    @staticmethod
    def _custom_highlight_tag(phrase, start="<strong>", end="</strong>"):

        """Injects an open and close highlight tag after a word

        Args:
            phrase (str) - A word or phrase.
        Kwargs:
            start (str) - An opening tag.  Defaults to <strong>
            end (str) - A closing tag.  Defaults to </strong>
        Returns:
            (str) word or phrase with custom opening and closing tags
            
        >>> h = HighlightDocumentOperations()
        >>> h._custom_highlight_tag("foo")
        '<strong>foo</strong>'
        >>>
        
        """
        tagged_phrase = "{0}{1}{2}".format(start, phrase, end)
        return tagged_phrase

    def _doc_to_sentences(self):
        """Takes a string document and converts it into a list of sentences
        
        Unfortunately, this approach might be a tad naive for production
        because some segments that are split on a period are really an
        abbreviation, and to make things even more complicated, an
        abbreviation can also be the end of a sentence::
            http://nltk.googlecode.com/svn/trunk/doc/book/ch03.html
        
        Returns:
            (generator) A generator object of a tokenized sentence tuple,
            with the list position of sentence as the first portion of
            the tuple, such as:  (0, "This was the first sentence")
        
        """

        tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
        sentences = tokenizer.tokenize(self._document)
        for sentence in enumerate(sentences):
            yield sentence

    @staticmethod
    def _score_sentences(sentence, querydict):
        """Creates a scoring system for each sentence by substitution analysis
        
        Tokenizes each sentence, counts characters
        in sentence, and pass it back as nested tuple
    
        Returns:
            (tuple) - (score (int), (count (int), position (int),
                    raw sentence (str))
            
        """

        position, sentence = sentence
        count = len(sentence)
        regex = re.compile("|".join(map(re.escape, querydict)))
        score = len(re.findall(regex, sentence))
        processed_score = (score, (count, position, sentence))
        return processed_score

    def _querystring_to_dict(self, split_token="+"):
        """Converts query parameters into a dictionary
        
        Returns:
            (dict)- dparams, a dictionary of query parameters
            
        """

        params = self._query.split(split_token)
        dparams = dict([(key, self._custom_highlight_tag(key)) for key in params])
        return dparams

    @staticmethod
    def _word_frequency_sort(sentences):
        """Sorts sentences by score frequency, yields sorted result
        
        This will yield the highest score count items first.
        
        Args:
            sentences (list) - a nested tuple inside of list
            [(0, (90, 3, "The crust/dough was just way too effin' dry for me.
            Yes, I know what 'cornmeal' is, thanks."))]

        """

        sentences.sort()
        while sentences:
            yield sentences.pop()

    def _create_snippit(self, sentences, max_characters=175):
        """Creates a snippet from a sentence while keeping it under max_chars 
        
        Returns a sorted list with max characters.  The sort is an attempt
        to rebuild the original document structure as close as possible,
        with the new sorting by scoring and the limitation of max_chars.
        
        Args:
            sentences (generator) - sorted object to turn into a snippit
            max_characters (int) - optional max characters of snippit
           
        Returns:
            snippit (list) - returns a sorted list with a nested tuple that
            has the first index holding the original position of the list::
            
            [(0, (90, 3, "The crust/dough was just way too effin' dry for me.
            Yes, I know what 'cornmeal' is, thanks."))]
            
        """

        snippit = []
        total = 0
        for sentence in self._word_frequency_sort(sentences):
            LOG.debug("Creating snippit", sentence)
            score, (count, position, raw_sentence) = sentence
            total += count
            if total < max_characters:
                # position now gets converted to index 0 for sorting later
                snippit.append(((position), score, count, raw_sentence))

        # try to reassemble document by original order by doing a simple sort
        snippit.sort()
        return snippit

    @staticmethod
    def _multiple_string_replace(string_to_replace, dict_patterns):
        """Performs a multiple replace in a string with dict pattern.
        
        Borrowed from Python Cookbook.
        
        Args:
            string_to_replace (str) - String to be multi-replaced
            dict_patterns (dict) - A dict full of patterns
            
        Returns:
            (str) - Multiple replaced string.
        
        """

        regex = re.compile("|".join(map(re.escape, dict_patterns)))

        def one_xlat(match):
            """Closure that is called repeatedly during multi-substitution.
            
            Args:
                match (SRE_Match object)
            Returns:
                partial string substitution (str)
            
            """

            return dict_patterns[match.group(0)]

        return regex.sub(one_xlat, string_to_replace)

    def _reconstruct_document_string(self, snippit, querydict):
        """Reconstructs string snippit, build tags, and return string
        
        A helper function for highlight_doc.
        
        Args:
            string_to_replace (list) - A list of nested tuples, containting
            this pattern::
            
            [(0, (90, 3, "The crust/dough was just way too effin' dry for me.
            Yes, I know what 'cornmeal' is, thanks."))]
            
            dict_patterns (dict) - A dict full of patterns
        
        Returns:
            (str) The most relevant snippet with the query terms highlighted.
        
        """

        snip = []
        for entry in snippit:
            score = entry[1]
            sent = entry[3]
            # if we have matches, now do the multi-replace
            if score:
                sent = self._multiple_string_replace(sent, querydict)
            snip.append(sent)
        highlighted_snip = " ".join(snip)

        return highlighted_snip

    def highlight_doc(self):
        """Finds the most relevant snippit with the query terms highlighted
        
        Returns:
            (str) The most relevant snippet with the query terms highlighted.
        
        """

        # tokenize to sentences, and convert query to a dict
        sentences = self._doc_to_sentences()
        querydict = self._querystring_to_dict()

        # process and score sentences
        scored_sentences = []
        for sentence in sentences:
            scored = self._score_sentences(sentence, querydict)
            scored_sentences.append(scored)

        # fit into max characters, and sort by original position
        snippit = self._create_snippit(scored_sentences)
        # assemble back into string
        highlighted_snip = self._reconstruct_document_string(snippit, querydict)

        return highlighted_snip
