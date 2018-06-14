# data_transform.py
# A data-transformation implementation based on IEEE S&P 2018 paper
# 'Manipulating Machine Learning: Poisoning Attacks and Countermeasures for
# Regression Learning.'
# Matthew Sedam. 2018. Original code from Matthew Jagielski.

from adlib.adversaries import Adversary
from data_reader.binary_input import Instance
from typing import Dict, List

""" Examples
GD with random flipping
python MYTEST -m ridge -init randflip -obj 0 -a 0.5 -b 0.1 -i 1 -s 4 -seed 123

BGD with AlfaTilt
python MYTEST -m ridge -init alfatilt -obj 0 -a 0.5 -b 0.1 -i 1 -s 4 -seed 123

BGD with InfFlip
python MYTEST -m ridge -init inflip -obj 0 -a 0.5 -b 0.1 -i 1 -s 4 -seed 123

BGD with Adaptive
python MYTEST -m ridge -init adaptive -obj 0 -a 0.5 -b 0.1 -i 1 -s 4 -seed 123

Validation with random flipping
python MYTEST -m ridge -init randflip -obj 1 -a 0.5 -b 0.1 -i 1 -s 4 -seed 123

New objective with random flipping
python MYTEST -m ridge -init randflip -obj 2 -a 0.5 -b 0.1 -i 1 -s 4 -seed 123
"""


class DataTransform(Adversary):
    def __init__(self, beta=0.1,
                 dataset=('./data_reader/data/raw/data-transform/'
                          'house-processed.csv'),
                 epsilon=0.001, eta=0.5, initialization='randflip', lambd=1,
                 logdir='./results', logind=0, model='ridge', multiproc=True,
                 numinit=1, objective=1, optimizey=False, partct=4, poisct=75,
                 rounding=False, seed=123, sigma=1.0, testct=500, trainct=300,
                 validct=250, visualize=False):
        Adversary.__init__(self)
        self.beta = beta
        self.dataset = dataset
        self.epsilon = epsilon
        self.eta = eta
        self.initialization = initialization
        self.lambd = lambd
        self.logdir = logdir
        self.logind = logind
        self.model = model
        self.multiproc = multiproc
        self.numinit = numinit
        self.objective = objective
        self.optimizey = optimizey
        self.partct = partct
        self.poisct = poisct
        self.rounding = rounding
        self.seed = seed
        self.sigma = sigma
        self.testct = testct
        self.trainct = trainct
        self.validct = validct
        self.visualize = visualize

    def attack(self, instances) -> List[Instance]:
        raise NotImplementedError

    def set_params(self, params: Dict):
        raise NotImplementedError

    def get_available_params(self):
        raise NotImplementedError

    def set_adversarial_params(self, learner, train_instances):
        raise NotImplementedError
