import unittest
from jgstrings.suffixtree import SuffixTree

class SuffixTreeTestCase(unittest.TestCase):
    def test_treeconstruction(self):
        suffixtree = SuffixTree('xabxac')
        searcher = suffixtree.start_traverse()
        suffixes = searcher.get_suffixes()
        self.assertEqual(len(suffixes), 6)
        
        searcher.match('c')
        suffixes = searcher.get_suffixes()
        self.assertEqual(len(suffixes), 1)
        
        searcher.reset()
        for c in 'bxac':
            self.assertTrue(searcher.match(c))

        suffixes = searcher.get_suffixes()
        self.assertEqual(len(suffixes), 1)

        suffixtree = SuffixTree('mississippi')
        searcher = suffixtree.start_traverse()
        suffixes = searcher.get_suffixes()
        self.assertEqual(len(suffixes), 11)

        for c in 'ssi':
            self.assertTrue(searcher.match(c))
        self.assertEqual(len(searcher.get_suffixes()), 2)

    def test_treeconstruction_with_list(self):
        data = ['19', '18', '28', '15', '8', '15', '5', '15',
                '9', '15', '4', '15', '9', '25', '27', '22', '6', 
                '16', '20', '24', '20', '21', '21', '3', '3',
                '17', '17', '17', '13', '13', '13', '13', '16', '2', 
                '22', '25', '20', '23', '24', '23', '22', '19',
                '18', '8', '9', '18', '19', '11', '1', '20', '2',
                '21', '17', '13', '13', '17', '13', '13', '13',
                '16', '22', '22', '19', '12', '23', '24', '17',
                '23', '17', '24', '1', '23', '23', '22', '3', '16',
                '22', '12', '8', '12', '22', '24', '21', '17', '21',
                '13', '13', '13', '13', '13', '17', '17', '17',
                '17', '23', '23', '20', '6', '7', '25', '8', '4',
                '4', '5', '4', '4', '4', '27', '26', '7', '26',
                '27', '4', '4', '4', '4', '4', '4']
        suffixtree = SuffixTree(data)
        searcher = suffixtree.start_traverse()
        for c in ['4', '4', '4', '4', '4', '4']:
            self.assertTrue(searcher.match(c))

        suffixes = searcher.get_suffixes()
        self.assertEqual(len(suffixes), 1)

    def test_string_matching(self):
        data = ['10', '22', '16', '13', '13', '13', '13', '13', '13', '13',
                '3', '17', '17', '13', '17', '17', '21', '16', '16', '21',
                '13', '13', '13', '13', '13', '13', '13', '13', '13', '13',
                '13', '3', '16', '2', '16', '21', '17', '17', '14', '21',
                '2', '2', '6', '21', '12', '1', '23', '1', '22', '2', '21',
                '13', '13', '21', '21', '2', '22', '21', '13', '13', '13',
                '13', '13', '13', '13', '13', '13', '13', '13', '13', '13',
                '13', '13', '17', '21', '16', '16', '24', '20', '20', '23',
                '21', '17', '17', '21', '17', '13', '13', '13', '13', '13',
                '3', '3', '2', '26', '12', '19', '12', '23', '21', '17', '13',
                '13', '13', '13', '13', '13', '13', '13', '13', '13', '13',
                '13', '13', '3', '16', '16', '16', '24', '23', '14', '22',
                '16', '16', '13', '13', '13', '13', '13', '13', '13', '13',
                '13', '13', '13', '13', '13', '13', '13', '13', '13', '13',
                '13', '13', '13', '16', '2', '22']
        suffixtree = SuffixTree(data)
        searcher = suffixtree.start_traverse()
        for c in ['13', '16', '2', '22']:
            self.assertTrue(searcher.match(c))

        self.assertFalse(searcher.match('4'))
        searcher.moveup()
        self.assertFalse(searcher.match('4'))

        data2 = ['10', '22', '16', '13', '13', '13', '13', '13', '13', '13',
                 '3', '17', '17', '13', '17', '17', '21', '16', '16', '21',
                 '13', '13', '13', '13', '13', '13', '13', '13', '13', '13',
                 '13', '3', '16', '2', '16', '21', '17', '17', '14', '21',
                 '2', '2', '6', '21', '12', '1', '23', '1', '22', '2', '21',
                 '13', '13', '21', '21', '2', '22', '21', '13', '13', '13',
                 '13', '13', '13', '13', '13', '13', '13', '13', '13', '13',
                 '13', '13', '17', '21', '16', '16', '24', '20', '20', '23',
                 '21', '17', '17', '21', '17', '13', '13', '13', '13', '13',
                 '3', '3', '2', '26', '12', '19', '12', '23', '21', '17', '13',
                 '13', '13', '13', '13', '13', '13', '13', '13', '13', '13',
                 '13', '13', '3', '16', '16', '16', '24', '23', '14', '22',
                 '16', '16', '13', '13', '13', '13', '13', '13', '13', '13',
                 '13', '13', '13', '13', '13', '13', '13', '13', '13', '13',
                 '13', '13', '13', '16', '2', '22']
        suffixtree = SuffixTree(data2)
        searcher = suffixtree.start_traverse()
        for c in ['19', '12', '23', '21']:
            self.assertTrue(searcher.match(c))
        self.assertFalse(searcher.match('13'))
        searcher.moveup()
        
                         
                         

        
    
