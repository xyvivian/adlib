# label_flipping_test.py
# Tests the label flipping implementation
# Matthew Sedam

from adlib.adversaries.label_flipping import LabelFlipping
from adlib.learners import SimpleLearner
from adlib.utils.common import calculate_correct_percentages
from data_reader.dataset import EmailDataset
from data_reader.operations import load_dataset
from copy import deepcopy
from sklearn import svm
import numpy as np
import time


def test_label_flipping():
    print('\n#################################################################')
    print('START label flipping attack.\n')

    begin = time.time()

    # Data processing unit
    # The path is an index of 400 testing samples(raw email data).
    dataset = EmailDataset(path='./data_reader/data/raw/trec05p-1/test-400',
                           binary=True, raw=True)
    training_data = load_dataset(dataset)

    print('Training sample size: ', len(training_data), '/400\n', sep='')

    # Randomly cut dataset in approximately half
    rand_choices = np.random.binomial(1, 0.5, len(training_data))
    new_training_data = []
    predict_data = []
    for i in range(len(training_data)):
        if rand_choices[i] == 1:
            new_training_data.append(training_data[i])
        else:
            predict_data.append(training_data[i])
    training_data = new_training_data

    # Setting the default learner
    # Test simple learner svm
    learning_model = svm.SVC(probability=True, kernel='linear')
    learner = SimpleLearner(learning_model, training_data)
    learner.train()
    orig_learner = deepcopy(learner)

    # Execute the attack
    cost = list(np.random.binomial(2, 0.5, len(training_data)))
    total_cost = 0.3 * len(training_data)  # flip around ~30% of the labels
    attacker = LabelFlipping(learner, cost, total_cost, verbose=True)
    attack_data = attacker.attack(training_data)

    flip_vector = []  # 0 -> flipped, 1 -> not flipped
    for i in range(len(attack_data)):
        if attack_data[i].get_label() != training_data[i].get_label():
            flip_vector.append(0)
        else:
            flip_vector.append(1)

    print('Flip vector with 0 -> flipped and 1 -> not flipped: \n',
          np.array(flip_vector), '\n')

    original_pred_labels = learner.predict(training_data)

    # Retrain the model with poisoned data
    learning_model = svm.SVC(probability=True, kernel='linear')
    learner = SimpleLearner(learning_model, attack_data)
    learner.train()

    ############################################################################
    # Calculate statistics with training data

    attack_pred_labels = learner.predict(training_data)  # predict w/ orig label

    (orig_precent_correct,
     attack_precent_correct,
     difference) = calculate_correct_percentages(original_pred_labels,
                                                 attack_pred_labels,
                                                 training_data)

    print('###################################################################')
    print('Predictions with training dataset:')
    print('Original correct percentage: ', orig_precent_correct, '%')
    print('Attack correct percentage: ', attack_precent_correct, '%')
    print('Difference: ', difference, '%')

    ############################################################################
    # Calculate statistics with predict data (other half of dataset)

    original_pred_labels = orig_learner.predict(predict_data)
    attack_pred_labels = learner.predict(predict_data)

    (orig_precent_correct,
     attack_precent_correct,
     difference) = calculate_correct_percentages(original_pred_labels,
                                                 attack_pred_labels,
                                                 predict_data)

    print('###################################################################')
    print('Predictions with other half of dataset:')
    print('Original correct percentage: ', orig_precent_correct, '%')
    print('Attack correct percentage: ', attack_precent_correct, '%')
    print('Difference: ', difference, '%')

    end = time.time()
    print('\nTotal time: ', round(begin - end, 2), 's', '\n', sep='')

    print('\nEND label flipping attack.')
    print('#################################################################\n')


if __name__ == '__main__':
    test_label_flipping()
