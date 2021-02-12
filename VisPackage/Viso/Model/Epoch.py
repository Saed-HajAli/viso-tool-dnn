import numpy as np
from ..Entity.Bound import Bound
from ..Entity.MatrixBound import MatrixBound
from ..Entity.BoxFeaturesBound import BoxFeaturesBound
from .. import Helper as hlp
from sklearn.metrics import confusion_matrix
import math


class Epoch:
    class Settings:
        def __init__(self):
            self.probLimits = [0.00, 1.00]
            self.probtnFilter = 0.10
            self.probtpFilter = 1.00
            self.probbins = 10
            self.boxIQR = 1.5
            self.opl = 0.00
            self.oph = 1.00
            self.oca = "all"
            self.ocp = "all"
            self.ors = "all"
            self.tpColor = "#59a954"
            self.fpColor = "#ff874d"
            self.tnColor = "#a4a6a9"
            self.fnColor = "#dc3842"

    def __init__(self, EpochData=None, Settings=None):
        self.orgData = EpochData

        self.Settings = Epoch.Settings() if Settings is None else Settings
        self.histsBoundMax = Bound()
        self.matrixBound = MatrixBound()
        self.boxFeaturesBound = BoxFeaturesBound()
        self.summaryHistMax = 0

        self.histPreparedData = []
        self.summaryHistData = []
        self.confMatrix = []
        self.confMatrixData = []

        self.headers = self.getColumns(self.orgData)
        self.nCols = self.getNCols(self.headers)
        self.images = self.getImages(self.headers, self.nCols)
        self.features = self.getFeatures(self.headers, self.nCols)
        self.probs = self.getProbs(self.headers, self.nCols)
        self.target = self.getTarget(self.headers, self.nCols)
        self.predicted = self.getPredicted(self.headers, self.nCols)
        self.classNames = self.getClassNames(self.orgData, self.target)
        self.confMatrix = self.getConfusionMatrix(self.orgData, self.classNames, self.target, self.predicted)
        self.labeledData = self.labelData(self.orgData, self.classNames, self.target, self.predicted)

        self.numericData = self.getNumericData(self.orgData, self.features)
        # print(np.array(self.orgData[0]))
        self.histPreparedData = self.getHistsData(self.orgData)

        # print(self.orgData)

        self.summaryHistData = self.getSummaryHistData(self.orgData)
        self.summaryHistDataPerScore = self.getSummaryHistDataPerScore()

        # print(self.summaryHistDataPerScore)

        # print(self.summaryHistData)
        self.confMatrixData = self.getConfusionMatrixData(self.confMatrix)
        self.featuresData = self.getFeaturesData(self.orgData)
        self.imageData = self.getImageData(self.orgData)

        # print("-------------------------------------------")
        self.computeAccuracyForEachClass()
        # print("-------------------------------------------")

    def getNumericData(self, data, names):
        for i in range(len(data)):
            for j in range(len(names)):
                if data[i][names[j]] in data[i].values():
                    data[i][names[j]] = int(data[i][names[j]])
        return data

    def getColumns(self, data):
        return list(data[0].keys())

    def getNCols(self, names):
        return len(names)

    def getImages(self, names, n):
        a = -1
        for i in range(n):
            if names[i] == 'image_url':
                a = i
        return a

    def getFeatures(self, names, n):
        a = []
        for i in range(n):
            if names[i][:2] == 'F-':
                a.append(names[i])
        return a

    def getProbs(self, names, n):
        a = []
        for i in range(n):
            if names[i][:2] == 'P-':
                a.append(names[i])
        return a

    def getTarget(self, names, n):
        for i in range(n):
            if names[i][:2] == 'A-':
                break
        return names[i]

    def getPredicted(self, names, n):
        for i in range(n):
            if names[i][:9] == 'Predicted':
                break
        return names[i]

    def getClassNames(self, data, target):
        distinct = list(set(dic[target] for dic in data))
        distinct.sort()
        return distinct

    def getConfusionMatrix(self, data, classNames, target, predicted):
        classmap = {}
        cl = len(classNames)
        mat = self.zeros(cl, cl)
        for i in range(cl):
            classmap[classNames[i]] = i

        for i in range(len(data)):
            aclass = data[i][target]
            pclass = data[i][predicted]
            aind = classmap[aclass]
            pind = classmap[pclass]
            mat[aind][pind] += 1

        return mat

    def computeAccuracyForEachClass(self):
        y_true = [t[self.target] for t in self.orgData]
        y_pred = [t[self.predicted] for t in self.orgData]
        target_names = self.classNames

        cm = confusion_matrix(y_true, y_pred)
        # print(cm)
        # print("--------------------------------")

        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        # print("--------------------------------")

        # print(1-cm.diagonal())

    def errorRatePerClass(self):
        return 1 - self.computeAccuracyForEachClass()

    def labelData(self, data, classNames, target, predicted):

        for j in range(len(classNames)):
            name = classNames[j]
            for i in range(len(data)):
                if data[i][target] == name and data[i][predicted] == name:
                    data[i]["L-" + name] = "TP"
                else:
                    if data[i][target] != name and data[i][predicted] == name:
                        data[i]["L-" + name] = "FP"
                    else:
                        if data[i][target] == name and data[i][predicted] != name:
                            data[i]["L-" + name] = "FN"
                        else:
                            if data[i][target] != name and data[i][predicted] != name:
                                data[i]["L-" + name] = "TN"

        # print(data[0])
        return data

    def zeros(self, r, c):
        return np.zeros((r, c)).tolist()

    def getBinValues(self):
        bins = self.Settings.probbins
        array = []
        k = (self.Settings.probLimits[1] - self.Settings.probLimits[0]) / bins
        num = 0
        for i in range(1, bins + 1):
            num = i * k
            num = round((self.Settings.probLimits[0] + num) * 100) / 100
            array.append(num)
        return array

    def getHistsData(self, data):
        classes = self.classNames
        bins = self.Settings.probbins  # settings.probbins
        self.histPreparedData = []
        self.histsBoundMax = Bound(0, 0)
        binValues = self.getBinValues()
        maxright = maxleft = 0

        probDataOptions = {
            'tp': True,
            'tn': True,
            'fp': True,
            'fn': True
        }

        for i in range(len(classes)):
            name = "L-" + classes[i]
            prob = "P-" + classes[i]
            preparedData = []
            for j in range(len(binValues)):
                if j == 0:
                    l = self.Settings.probLimits[0]
                else:
                    l = round((binValues[j - 1] + 0.01) * 100) / 100
                preparedData.append({
                    'name': classes[i],
                    'lowProb': l,
                    'probability': binValues[j],  # upper value for all buckets
                    'tn': 0,
                    'tp': 0,
                    'fn': 0,
                    'fp': 0,
                })

            for j in range(len(data)):
                for k in range(len(preparedData)):
                    if data[j][name].lower() == "tn" and data[j][prob] < self.Settings.probtnFilter:
                        break

                    if data[j][name].lower() == "tp" and data[j][prob] > self.Settings.probtpFilter:
                        break

                    if probDataOptions[data[j][name].lower()] and preparedData[k]['lowProb'] <= data[j][prob] <= \
                            preparedData[k]['probability']:
                        preparedData[k][data[j][name].lower()] += 1
                        break

            self.histPreparedData.append(preparedData)
            maxleft = max(maxleft, max([dic['tn'] + dic['fn'] for dic in preparedData]))
            maxright = max(maxright, max([dic['tp'] + dic['fp'] for dic in preparedData]))
            self.histsBoundMax = Bound(maxright, maxleft)
        return self.histPreparedData

    def getSummaryHistData(self, data):
        self.summaryHistData = []
        for i in range(len(self.classNames)):
            self.summaryHistData.append({
                'name': self.classNames[i],
                'tp': 0,
                'fn': 0,
                'fp': 0,
                'tn': 0
            })

        # print(self.summaryHistData)
        for j in range(len(data)):
            for k in range(len(self.summaryHistData)):
                Cname = "L-" + self.summaryHistData[k]['name']
                if data[j][Cname].lower() != 'tn':
                    self.summaryHistData[k][data[j][Cname].lower()] += 1
        left = max([obj['fn'] + obj['tn'] for obj in self.summaryHistData])
        right = max([obj['tp'] + obj['fp'] for obj in self.summaryHistData])
        self.summaryHistMax = max(left, right)
        return self.summaryHistData

    def getSummaryHistDataPerScore(self):

        self.summaryHistDataPerScore = []
        # 10 is number of ranges (0.1, 0.2, 0.3 ... 0.9 )
        binValues = self.getBinValues()
        for j in range(len(binValues)):
            if j == 0:
                l = self.Settings.probLimits[0]
            else:
                l = round((binValues[j - 1] + 0.01) * 100) / 100
            self.summaryHistDataPerScore.append({
                'lowProb': l,
                'probability': binValues[j],  # upper value for all buckets
                'tn': 0,
                'tp': 0,
                'fn': 0,
                'fp': 0,
            })

        for i in range(len(self.orgData)):
            for k in range(len(self.summaryHistDataPerScore)):
                if self.orgData[i]['P-' + self.orgData[i][self.predicted]] <= self.summaryHistDataPerScore[k][
                    'probability'] and self.orgData[i]['P-' + self.orgData[i][self.predicted]] >= \
                        self.summaryHistDataPerScore[k]['lowProb']:
                    if self.orgData[i][self.target] == self.orgData[i][self.predicted]:
                        self.summaryHistDataPerScore[k]['tp'] += 1
                    else:
                        self.summaryHistDataPerScore[k]['fn'] += 1

        left = max([obj['fn'] + obj['tn'] for obj in self.summaryHistDataPerScore])
        right = max([obj['tp'] + obj['fp'] for obj in self.summaryHistDataPerScore])
        self.summaryHistPerScoreMax = max(left, right)

        # print(self.summaryHistDataPerScore)

        return self.summaryHistDataPerScore

    def getConfusionMatrixData(self, matrix):
        self.confMatrixData = []
        for i in range(len(self.classNames)):
            for j in range(len(self.classNames)):
                c = matrix[i][j]
                self.confMatrixData.append({
                    'actual': self.classNames[i],
                    'predicted': self.classNames[j],
                    'value': c,
                    'fill': "#000",
                    'filld': "#fff"
                })
                if self.classNames[i] != self.classNames[j] and c < self.matrixBound.minMat:
                    self.matrixBound.minMat = c
                if self.classNames[i] != self.classNames[j] and c > self.matrixBound.maxMat:
                    self.matrixBound.maxMat = c
                if self.classNames[i] == self.classNames[j] and c < self.matrixBound.mindMat:
                    self.matrixBound.mindMat = c
                if self.classNames[i] == self.classNames[j] and c > self.matrixBound.maxdMat:
                    self.matrixBound.maxdMat = c
        return self.confMatrixData

    def getFeaturesData(self, data):
        tmpFeaturesData = []
        featuresData = []
        filteredData = data

        for j in range(len(self.features)):
            if filteredData[0][self.features[j]] is not None:
                tmpFeaturesData.append([self.features[j], []])
        kk = 0
        for i in range(len(filteredData)):
            for j in range(len(tmpFeaturesData)):
                value = filteredData[i][self.features[j]]
                tmpFeaturesData[j][1].append(value)
                if self.boxFeaturesBound.max < value:
                    self.boxFeaturesBound.max = value
                if self.boxFeaturesBound.min > value:
                    self.boxFeaturesBound.min = value

        for k in range(len(tmpFeaturesData)):
            n = tmpFeaturesData[k][0]
            tmpFeaturesData[k][1].sort()
            # d = tmpFeaturesData[k][1]
            q = hlp.quartiles(tmpFeaturesData[k][1])
            w = hlp.whiskers(tmpFeaturesData[k][1], q, self.Settings)
            o = hlp.outliers(tmpFeaturesData[k][1], w)
            featuresData.append({
                'name': n,
                'data': tmpFeaturesData[k][1],
                'quartiles': q,
                'whiskers': w,
                'outliers': o,
                'difference': 0
            })
        # print(*np.array(featuresData[0]['data']))
        return featuresData

    def getImageData(self, data):
        imageData = []

        if 'image_url' not in data[0].keys():
            return imageData

        for i in range(len(data)):
            imageData.append({
                'url': data[i]['image_url'],
                'actual': data[i][self.target],
                'predicted': data[i][self.predicted],
                'id': data[i]["id"]
            })
        return imageData

    def getDataJson(self):
        response = {
            'data': self.orgData,
            'headers': self.headers,
            'classNames': self.classNames,
            'histsBounds': {
                'maxRight': self.histsBoundMax.maxRight,
                'maxLeft': self.histsBoundMax.maxLeft,
            },
            'matrixBound': {
                'maxd': self.matrixBound.maxdMat,
                'max': self.matrixBound.maxMat,
                'mind': self.matrixBound.mindMat,
                'min': self.matrixBound.minMat
            },
            'images': self.images,
            'features': self.features,
            'histsPreparedData': self.histPreparedData,
            'confMatrixData': self.confMatrixData,
            'summaryHistData': self.summaryHistData,
            'summaryHistMax': self.summaryHistMax,
            'featuredData': self.featuresData,
            'featuresBound': {
                'max': self.boxFeaturesBound.max,
                'min': self.boxFeaturesBound.min
            },
            'imageData': self.imageData
        }
        return response

    def getFrame(self, classIndex):
        y = [x['lowProb'] for x in self.histPreparedData[classIndex]]
        tps = [x['tp'] for x in self.histPreparedData[classIndex]]
        fps = [x['fp'] for x in self.histPreparedData[classIndex]]
        fns = [-x['fn'] for x in self.histPreparedData[classIndex]]
        tns = [-x['tn'] for x in self.histPreparedData[classIndex]]
        data = [
            {'x': fns,
             'y': y,
             'type': 'bar',
             'name': 'FN',
             'showlegend': False,
             'orientation': 'h',
             'hovertemplate': "%{text}",
             'text': [abs(fn) for fn in fns],
             'marker': {'color': self.Settings.fnColor},
             'base': 0},
            {'x': tns,
             'y': y,
             'type': 'bar',
             'name': 'TN',
             'showlegend': False,
             'hovertemplate': "%{text}",
             'text': [abs(tn) for tn in tns],
             'orientation': 'h',
             'marker': {'color': self.Settings.tnColor},
             'base': fns},
            {'x': tps,
             'y': y,
             'type': 'bar',
             'name': 'TP',
             'showlegend': False,
             'hovertemplate': "%{text}",
             'text': [abs(tp) for tp in tps],
             'orientation': 'h',
             'marker': {'color': self.Settings.tpColor},
             'base': fps},
            {'x': fps,
             'y': y,
             'type': 'bar',
             'showlegend': False,
             'name': 'FP',
             'hovertemplate': "%{text}",
             'text': [abs(fp) for fp in fps],
             'orientation': 'h',
             'marker': {'color': self.Settings.fpColor},
             'base': 0}
        ]
        return data

    def getSummaryFrame(self):
        y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        tps = [x['tp'] for x in self.summaryHistData]
        fps = [x['fp'] for x in self.summaryHistData]
        fns = [-x['fn'] for x in self.summaryHistData]
        tns = [-x['tn'] for x in self.summaryHistData]
        data = [
            {'x': fns,
             'y': y,
             'type': 'bar',
             'name': 'FN',
             'orientation': 'h',
             'hovertemplate': "%{text}",
             'text': [abs(fn) for fn in fns],
             'marker': {'color': self.Settings.fnColor},
             'base': 0},
            {'x': tns,
             'y': y,
             'type': 'bar',
             'name': 'TN',
             'hovertemplate': "%{text}",
             'text': [abs(tn) for tn in tns],
             'orientation': 'h',
             'marker': {'color': self.Settings.tnColor},
             'base': fns},
            {'x': tps,
             'y': y,
             'type': 'bar',
             'name': 'TP',
             'hovertemplate': "%{text}",
             'text': [abs(tp) for tp in tps],
             'orientation': 'h',
             'marker': {'color': self.Settings.tpColor},
             'base': fps},
            {'x': fps,
             'y': y,
             'type': 'bar',
             'name': 'FP',
             'hovertemplate': "%{text}",
             'text': [abs(fp) for fp in fps],
             'orientation': 'h',
             'marker': {'color': self.Settings.fpColor},
             'base': 0}
        ]
        return data


    # tn and fp not included in the array 'summaryHistDataPerScore',
    # because we want to show only the samples related to our class !
    # tp = ci ==> ci , fn = ci ==> ck
    # we colored the fn with fp color (orange) instead of (red)
    # in the array fp and tn = 0
    # we named the title as True | False (not TP and FN) because we
    # focus to show the True and False count of samples for this class (score)
    # We want show how much the model is confident of the fn value ! if the value was high so it is problem
    # because the model predict with fn and it confident about that.
    def getSummaryFramePerScore(self):



        y = [x['lowProb'] for x in self.summaryHistDataPerScore]
        tps = [x['tp'] for x in self.summaryHistDataPerScore]
        #fps = [x['fp'] for x in self.summaryHistDataPerScore]
        fns = [-x['fn'] for x in self.summaryHistDataPerScore]
        #tns = [-x['tn'] for x in self.summaryHistDataPerScore]
        data = [
            {'x': fns,
             'y': y,
             'type': 'bar',
             'name': 'False',
             'orientation': 'h',
             'hovertemplate': "%{text}",
             'text': [abs(fn) for fn in fns],
             'marker': {'color': self.Settings.fpColor},
             'base': 0},
            # {'x': tns,
            #  'y': y,
            #  'type': 'bar',
            #  'name': 'TN',
            #  'hovertemplate': "%{text}",
            #  'text': [abs(tn) for tn in tns],
            #  'orientation': 'h',
            #  'marker': {'color': self.Settings.tnColor},
            #  'base': fns},
            {'x': tps,
             'y': y,
             'type': 'bar',
             'name': 'True',
             'hovertemplate': "%{text}",
             'text': [abs(tp) for tp in tps],
             'orientation': 'h',
             'marker': {'color': self.Settings.tpColor},
             'base': 0},
            # {'x': fps,
            #  'y': y,
            #  'type': 'bar',
            #  'name': 'FP',
            #  'hovertemplate': "%{text}",
            #  'text': [abs(fp) for fp in fps],
            #  'orientation': 'h',
            #  'marker': {'color': self.Settings.fpColor},
            #  'base': 0}
        ]
        return data
