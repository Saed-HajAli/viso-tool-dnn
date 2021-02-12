from .Epoch import Epoch


class Model:

    def __init__(self, modelData=None):
        self.modelData = modelData

    def buildModel(self):
        self.epochs = []
        for i in range(len(self.modelData)):
            epoch = Epoch(self.modelData[i])
            self.epochs.append(epoch)

    def epochCount(self):
        return len(self.epochs)

    def lastEpoch(self):
        return self.epochs[self.epochCount() - 1]

    def epoch(self, index):
        return self.epochs[index]

    def modelFrames(self, classIndex):
        frames = []
        for i in range(self.epochCount()):
            frames.append({'data': self.epochs[i].getFrame(classIndex)})
        return frames

    def modelFramesSummary(self):
        frames = []
        for i in range(self.epochCount()):
            frames.append({'data': self.epochs[i].getSummaryFrame()})
        return frames

    def modelFramesSummaryPerScore(self):
        frames = []
        for i in range(self.epochCount()):
            frames.append({'data': self.epochs[i].getSummaryFramePerScore()})
        return frames

    def maxRangeXAxis(self):
        right = max([v.histsBoundMax.maxRight for v in self.epochs])
        left = max([v.histsBoundMax.maxLeft for v in self.epochs])
        return max(right,left)/len(self.lastEpoch().classNames)

    def maxRangeXAxisSummary(self, epoch):
        return self.epochs[epoch].summaryHistMax

    def maxRangeXAxisSummaryPerScore(self, epoch):
        return self.epochs[epoch].summaryHistPerScoreMax

    def xAxisRange(self):
        r = [0.2,0.25,0.3,0.5,1,2,3,4,5]
        range = {}
        for v in r:
            range[v] = str(str(v))
        return r, range