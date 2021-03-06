
import os
import iquail
from .base_test_solution import BaseTestSolution


class TestSolutionLocal(BaseTestSolution):
    def test_file_1(self):
        solution = iquail.SolutionLocal(self.path('Allum1'))
        self.assertSolutionFile(solution,
                           'icon.jpeg',
                           '4ab70bcb55ddd942b81485aeb04747531c265778280bf4ca89debbe84209ff41')

    def test_walk_1(self):
        expected = [('.', ['conf', 'subfolder'], ['.conf_ignore', 'allum1', 'icon.jpeg', 'test.conf']),
                    ('conf', [], ['test.txt']),
                    ('subfolder', [], ['testfile.txt'])]
        solution = iquail.SolutionLocal(self.path('Allum1'))
        self.assertSolutionWalk(solution, expected)
