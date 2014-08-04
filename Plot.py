from unittest.test.test_result import __init__

__author__ = 'amyalenkov'

import pylab
from matplotlib import mlab


class CreatePlot:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.addPlot()

    def addPlot(self):
        pylab.plot(self.dx, self.dy)

    def showPlot(self):
        pylab.show()


# pylab.plot([647, 643], [-458, -459])
# pylab.plot([954, 86], [-260, -266])
# pylab.show()