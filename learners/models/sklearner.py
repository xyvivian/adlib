from typing import List, Dict
from data_reader.input import Instance
from learners.models.model import BaseModel
import numpy as np
from data_reader.operations import sparsify


class Model(BaseModel):
    """Learner model wrapper around sklearn classifier

    Extends the BaseModel class to use the functionality of
    a user-supplied sklearn classifier in conjunction with
    the adversarial library.

    """

    def __init__(self, sklearn_object):
        """Creates new model from user-supplied sklearn function.

        Args:
            sklearn_object (sklearn classifier): Model for sklearn
            classification.

        """
        self.learner = sklearn_object

    def train(self, instances: List[Instance]):
        """Train on the set of training instances using the underlying
        sklearn object.

        Args:
            instances (List[Instance]): training instances.

        """
        (y, X) = sparsify(instances)
        self.learner.fit(X,y)

    def predict(self, instances):
        """Predict classification labels for the set of instances using
        the predict function of the sklearn classifier.

        Args:
            instances (List[Instance]) or (Instance): training or test instances.

        Returns:
            label classifications (List(int))

        """
        if isinstance(instances, List):
            (y, X) = sparsify(instances)
            predictions = self.learner.predict(X)
        else:
            predictions = self.learner.predict(instances.get_feature_vector().get_csr_matrix())[0]
        return predictions

    def predict_proba_adversary(self, instances):
        """Use the model to determine probability of adversarial classification.

        Args:
            instances (List[Instance]) or (Instance): training or test instances.

        Returns:
            probability of adversarial classification (List(int))

        """
        if isinstance(instances, List):
            (y, X) = sparsify(instances)
            full_probs = self.learner.predict_proba(X)
            probs = [x[0] for x in full_probs]
        else:
            probs = self.learner.predict_proba(instances.get_feature_vector().get_csr_matrix())[0][0]
        return probs

    def decision_function_adversary(self, instances):
        """Use the model to determine the decision function for each instance.

        Args:
            instances (List[Instance]) or (Instance): training or test instances.

        Returns:
            decision values (List(int))

        """
        if isinstance(instances, List):
            (y, X) = sparsify(instances)
            f = self.learner.decision_function(X)
        else:
            f = self.learner.decision_function(instances.get_feature_vector().get_csr_matrix())[0]
        return f

    def set_params(self, params: Dict):
        """Set params for the model.

        Args:
            params (Dict): set of available params with updated values

        """
        self.learner.set_params(params)

    def get_available_params(self) -> Dict:
        """Get the set of params defined in the model usage.

        These are generated by the sklearn module.

        Returns:
            dictionary mapping param names to current values

        """
        return self.learner.get_params()

    def get_alg(self):
        """Return the underlying model algorithm.

        Returns:
            algorithm used to train and test instances

        """
        return self.learner



