from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn import base
import numpy as np
from sklearn.externals import six
from mlxtend.classifier import StackingCVClassifier

# Sklearn has hardcoded limits for repr outputs which is obviously not desirable for recreating, so this needs to be
# overriden without the limits

def _pprint(params, offset=0, printer=repr):
    """
    From: https://github.com/scikit-learn/scikit-learn/blob/51a765a/sklearn/base.py
    With line 142-143 removed
    """
    # Do a multi-line justified repr:
    options = np.get_printoptions()
    np.set_printoptions(precision=5, threshold=64, edgeitems=2)
    params_list = list()
    this_line_length = offset
    line_sep = ',\n' + (1 + offset // 2) * ' '
    for i, (k, v) in enumerate(sorted(six.iteritems(params))):
        if type(v) is float:
            # use str for representing floating point numbers
            # this way we get consistent representation across
            # architectures and versions.
            this_repr = '%s=%s' % (k, str(v))
        else:
            # use repr of the rest
            this_repr = '%s=%s' % (k, printer(v))
        if i > 0:
            if (this_line_length + len(this_repr) >= 75 or '\n' in this_repr):
                params_list.append(line_sep)
                this_line_length = len(line_sep)
            else:
                params_list.append(', ')
                this_line_length += 2
        params_list.append(this_repr)
        this_line_length += len(this_repr)

    np.set_printoptions(**options)
    lines = ''.join(params_list)
    # Strip trailing space to avoid nightmare in doctests
    lines = '\n'.join(l.rstrip(' ') for l in lines.split('\n'))
    return lines


base._pprint = _pprint


'''
Scikit learn doesnt allow varags as inputs, 
so we need to define the two cases of our voting classifier.
(3, and 5 inputs). TODO: Can we improve this?
'''

class StackingBaseClassifier(StackingCVClassifier):

    def __repr__(self):
        return "StackingCVClassifier(classifiers=" + repr(self.classifiers) + ", meta_classifier="\
               + repr(self.meta_classifier) + ")"

    __str__ = __repr__

class Stacking3Classifier(StackingBaseClassifier):

    def __init__(self, clf1, clf2, clf3, meta_classifier):
        super().__init__(classifiers=[clf1, clf2, clf3], meta_classifier=meta_classifier)


class Stacking5Classifier(StackingBaseClassifier):

    def __init__(self, clf1, clf2, clf3, cl4, clf5, meta_classifier):
        super().__init__(classifiers=[clf1, clf2, clf3, cl4, clf5], meta_classifier=meta_classifier)


def named_estimators(*classifiers):
    return [("Est" + str(idx), clf) for idx, clf in enumerate(classifiers)]

class VotingBaseClassifier(VotingClassifier):

    def __init__(self, estimators):
        super().__init__(estimators=estimators)

    def __repr__(self):
        # When recreating, we can just make a VotingClassifier now
        return "VotingClassifier(estimators=" + repr(self.estimators) + ")"

    __str__ = __repr__

class VotingBaseRegressor(VotingRegressor):

    def __init__(self, estimators):
        super().__init__(estimators=estimators)

    def __repr__(self):
        # When recreating, we can just make a VotingClassifier now
        return "VotingRegressor(estimators=" + repr(self.estimators) + ")"

    __str__ = __repr__


class Voting3Classifier(VotingBaseClassifier):
    def __init__(self, clf1, clf2, clf3):
        estimators = named_estimators(clf1, clf2, clf3)
        super().__init__(estimators=estimators)


class Voting5Classifier(VotingBaseClassifier):
    def __init__(self, clf1, clf2, clf3, clf4, clf5):
        estimators = named_estimators(clf1, clf2, clf3, clf4, clf5)
        super().__init__(estimators=estimators)


class Voting3Regressor(VotingBaseRegressor):
    def __init__(self, clf1, clf2, clf3):
        estimators = named_estimators(clf1, clf2, clf3)
        super().__init__(estimators=estimators)


class Voting5Regressor(VotingBaseRegressor):
    def __init__(self, clf1, clf2, clf3, clf4, clf5):
        estimators = named_estimators(clf1, clf2, clf3, clf4, clf5)
        super().__init__(estimators=estimators)
