import random
from os.path import join
from typing import Tuple, List

import arff
from snapshottest import TestCase

from src import DEFAULT_DIR
from src.XPLAIN_explainer import XPLAIN_explainer
from src.XPLAIN_explanation import XPLAIN_explanation
from src.dataset import Dataset


def load_arff(filename: str) -> Dataset:
    with open(filename, 'r') as f:
        a = arff.load(f)
        dataset = Dataset(a['data'], a['attributes'])

        return dataset


def import_dataset(dataset_name: str, explain_indices: List[int],
                   random_explain_dataset: bool) -> Tuple[Dataset, Dataset, List[str]]:
    assert dataset_name.endswith("arff")

    dataset = load_arff(dataset_name)

    dataset_len = len(dataset)
    training_indices = list(range(dataset_len))

    if random_explain_dataset:
        random.seed(1)
        # small dataset
        MAX_SAMPLE_COUNT = 100
        if dataset_len < (2 * MAX_SAMPLE_COUNT):
            samples = int(0.2 * dataset_len)
        else:
            samples = MAX_SAMPLE_COUNT

        # Randomly pick some instances to remove from the training dataset and use in the
        # explain dataset
        explain_indices = list(random.sample(training_indices, samples))
    for i in explain_indices:
        training_indices.remove(i)

    training_dataset = Dataset(dataset._decoded_df.iloc[training_indices], dataset.columns)

    explain_dataset = Dataset(dataset._decoded_df.iloc[explain_indices], dataset.columns)

    return training_dataset, explain_dataset, \
           [str(i) for i in explain_indices]


def import_datasets(dataset_name: str, explain_indices: List[int],
                    random_explain_dataset: bool) -> Tuple[Dataset, Dataset, List[str]]:
    """
    :param dataset_name: path of the dataset file
    :param explain_indices: indices of the instances to be added in the explain dataset
    :param random_explain_dataset: randomly sample 300 rows from the _explain.arff file to make the
                                   explain, will make `explain_indices` futile
    :return:
    """
    assert (dataset_name[-4:] == "arff")

    explain_dataset_name = dataset_name[:-5] + "_explain.arff"

    pd_training_dataset = load_arff(dataset_name)
    pd_explain_dataset = load_arff(explain_dataset_name)

    len_explain_dataset = len(pd_explain_dataset)

    if random_explain_dataset:
        random.seed(7)
        explain_indices = list(random.sample(range(len_explain_dataset), 300))

    pd_explain_dataset = Dataset(pd_explain_dataset._decoded_df.iloc[explain_indices],
                                 pd_explain_dataset.columns)

    return pd_training_dataset, pd_explain_dataset, [str(i) for i in
                                                     explain_indices]


def get_classifier(classifier_name: str):
    if classifier_name == "sklearn_nb":
        from sklearn.naive_bayes import MultinomialNB

        skl_clf = MultinomialNB()

        return skl_clf

    elif classifier_name == "sklearn_rf":
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import OneHotEncoder

        pipe = make_pipeline(OneHotEncoder(), RandomForestClassifier(random_state=42))
        skl_clf = pipe

        return skl_clf

    elif classifier_name == "nn_label_enc":
        from sklearn.neural_network import MLPClassifier

        skl_clf = MLPClassifier(random_state=42, max_iter=1000)

        return skl_clf

    elif classifier_name == "nn_onehot_enc":
        from sklearn.neural_network import MLPClassifier
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import OneHotEncoder

        pipe = make_pipeline(OneHotEncoder(), MLPClassifier(random_state=42, max_iter=1000))
        skl_clf = pipe

        return skl_clf

    else:
        raise ValueError("Classifier not available")


def get_explanation(dataset_name: str, classifier_name: str) -> XPLAIN_explanation:
    explain_dataset_indices = []
    if dataset_name in [join(DEFAULT_DIR, "datasets/adult_d.arff"),
                        join(DEFAULT_DIR, "datasets/compas-scores-two-years_d.arff")]:
        training_dataset, explain_dataset, explain_indices = import_datasets(
            dataset_name, explain_dataset_indices, True)
    else:
        training_dataset, explain_dataset, explain_indices = import_dataset(
            dataset_name, explain_dataset_indices, True)

    explainer = XPLAIN_explainer(dataset_name, get_classifier(classifier_name),
                                 training_dataset, explain_dataset, explain_indices,
                                 random_explain_dataset=True)

    instance = explainer.explain_dataset.get_decoded(0)

    cc = explainer.explain_dataset.class_column_name()
    target_class = instance[cc]

    return explainer.explain_instance(instance, target_class=target_class)


class TestGet_explanation(TestCase):
    def test_get_explanation_zoo_random_forest(self):
        e = get_explanation(join(DEFAULT_DIR, "datasets/zoo.arff"), "sklearn_rf")
        self.assertMatchSnapshot((
            e.XPLAIN_explainer_o,
            e.diff_single,
            e.map_difference,
            e.k,
            e.error,
            e.instance,
            e.target_class,
            e.instance_class_index,
            e.prob
        ))

    def test_get_explanation_zoo_naive_bayes(self):
        e = get_explanation(join(DEFAULT_DIR, "datasets/zoo.arff"), "sklearn_nb")
        self.assertMatchSnapshot((
            e.XPLAIN_explainer_o,
            e.diff_single,
            e.map_difference,
            e.k,
            e.error,
            e.instance,
            e.target_class,
            e.instance_class_index,
            e.prob
        ))

    def test_get_explanation_adult_naive_bayes(self):
        e = get_explanation(join(DEFAULT_DIR, "datasets/adult_d.arff"), "sklearn_nb")
        self.assertMatchSnapshot((
            e.XPLAIN_explainer_o,
            e.diff_single,
            e.map_difference,
            e.k,
            e.error,
            e.instance,
            e.target_class,
            e.instance_class_index,
            e.prob
        ))
