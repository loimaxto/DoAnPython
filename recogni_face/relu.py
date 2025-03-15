import numpy

class Relu:
    def __init__(self,input):
        self.input = input
        self.result = numpy.zeros((self.input.shape[0],
                               self.input.shape[1],
                               self.input.shape[2]))
    def operate(self):
        for layer in range(self.input.shape[2]):
            for row in range(self.input.shape[0]):
                for col in range(self.input.shape[1]):
                    if self.input[row,col,layer]<0:
                        self.result[row,col,layer] = 0
                    else: 
                        self.result[row,col,layer] = self.input[row,col,layer]
        return self.result
class LeakyRelu(Relu):

    def operate(self):
        for layer in range(self.input.shape[2]):
            for row in range(self.input.shape[0]):
                for col in range(self.input.shape[1]):
                    if self.input[row,col,layer]<0:
                        self.result[row,col,layer] = 0.1*self.input[row,col,layer]
                    else: 
                        self.result[row,col,layer] = self.input[row,col,layer]
        return self.result
class MaxPooling:
    def __init__(self,input, poolingsize = 2):
        self.input = input
        self.poolingsize= poolingsize
        self.result = numpy.zeros((
            int(self.input.shape[0]/poolingsize),
            int(self.input.shape[1]/poolingsize),
            self.input.shape[2]
        ))
    def operate(self):
        for layer in range(self.input.shape[2]):
            for row in range(int(self.input.shape[0]/self.poolingsize)):
                for col in range(int(self.input.shape[1]/self.poolingsize)):
                    self.result[row,col,layer]= numpy.max(
                        self.input[
                            row*self.poolingsize: row*self.poolingsize+self.poolingsize,
                            col*self.poolingsize: col*self.poolingsize+self.poolingsize,
                            layer
                        ])

        return self.result
class SoftMax:
    def __init__(self,input,nodes:int):
        self.input = input
        self.nodes = nodes
        self.flatten = self.input.flatten()
        self.weight = numpy.random.randn(self.flatten.shape[0])/self.flatten.shape[0]
        self.bias = numpy.random.randn(nodes)
    def operate(self):
        totals = numpy.dot(self.flatten,self.weight)*self.bias
        exp = numpy.exp(totals)
        print(exp.shape)
        return exp/sum(exp)