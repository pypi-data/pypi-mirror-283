from imblearn.over_sampling import RandomOverSampler, SMOTENC, SMOTE, ADASYN, BorderlineSMOTE
from imblearn.under_sampling import RandomUnderSampler
from .base import BaseProcessor, ProcessorMixin


class RandomOverSamplerProcessor(RandomOverSampler, BaseProcessor, ProcessorMixin):
    """Extension of the RandomOverSampler class by imbalance-learn to fit in the fairbalance framework.
    Formally, it simply adds two functions self._process and self._unprocess used in the mitigation strategy.

    Parameters
    ----------
    prefix_sep : str, optional
        The prefix separator used in the dumlifying process. Passed to the BaseProcessor parent class.
    **kwargs :
        Argument for the imblearn.over_sampling.RandomOverSampler parent class.

    """

    def __init__(self, prefix_sep: str = "~", force: bool = False, **kwargs):
        RandomOverSampler.__init__(self, **kwargs)
        BaseProcessor.__init__(self, prefix_sep=prefix_sep, force=force)

    def _process(self, X, y, dummify_cols=None, scale_cols=None, encode_cols=None, protected_attribute=None):
        return X, y

    def _unprocess(self, X, y):
        return X, y

    def _try_fit_resample(self, X, y):

        X_resampled, y_resampled = self.fit_resample(X, y)

        return X_resampled, y_resampled


class RandomUnderSamplerProcessor(RandomUnderSampler, BaseProcessor, ProcessorMixin):
    """Extension of the RandomUnderSampler class by imbalance-learn to fit in the fairbalance framework.
    Formally, it simply adds two functions self._process and self._unprocess used in the mitigation strategy.

    Parameters
    ----------
    prefix_sep : str, optional
        The prefix separator used in the dumlifying process. Passed to the BaseProcessor parent class.
    **kwargs :
        Argument for the imblearn.under_sampling.RandomUnderSampler parent class.

    """

    def __init__(self, prefix_sep: str = "~", force: bool = False, **kwargs):
        RandomUnderSampler.__init__(self, **kwargs)
        BaseProcessor.__init__(self, prefix_sep=prefix_sep, force=force)

    def _process(self, X, y, dummify_cols=None, scale_cols=None, encode_cols=None, protected_attribute=None):
        return X, y

    def _unprocess(self, X, y):
        return X, y

    def _try_fit_resample(self, X, y):

        X_resampled, y_resampled = self.fit_resample(X, y)

        return X_resampled, y_resampled


class ADASYNProcessor(ADASYN, BaseProcessor, ProcessorMixin):
    def __init__(self, prefix_sep: str = "~", force: bool = False, **kwargs):
        ADASYN.__init__(self, **kwargs)
        BaseProcessor.__init__(self, prefix_sep=prefix_sep, force=force)

    def _process(self, X, y, dummify_cols=None, scale_cols=None, encode_cols=None, protected_attribute=None):
        # assert y.value_counts().min(
        # ) > self.k_neighbors, f"Not enough elements of value {y.value_counts().index[-1]}: only {y.value_counts().min()} but should be >= {self.k_neighbors}"
        self.k_neighbors = min(y.value_counts().min() - 1, 5)

        if self.force:
            X, y = self._force_transform_df(X, y)

        processed_X = self.dummify_scale_encode(X,
                                                dummify_cols=dummify_cols,
                                                scale_cols=scale_cols,
                                                encode_cols=encode_cols)

        return processed_X, y

    def _unprocess(self, X, y):
        unprocessed_X = self.undo_dummify_scale_encode(X)
        # unprocessed_X = X
        return unprocessed_X, y

    def _try_fit_resample(self, X, y):

        X_resampled, y_resampled = self.fit_resample(X, y)

        return X_resampled, y_resampled


class SMOTEProcessor(SMOTE, BaseProcessor, ProcessorMixin):

    def __init__(self, prefix_sep: str = "~", force: bool = False, **kwargs):
        SMOTE.__init__(self, **kwargs)
        BaseProcessor.__init__(self, prefix_sep=prefix_sep, force=force)

    def _process(self, X, y, dummify_cols=None, scale_cols=None, encode_cols=None, protected_attribute=None):
        # assert y.value_counts().min(
        # ) > self.k_neighbors, f"Not enough elements of value {y.value_counts().index[-1]}: only {y.value_counts().min()} but should be >= {self.k_neighbors}"

        self.k_neighbors = min(y.value_counts().min() - 1, 5)

        if self.force:
            X, y = self._force_transform_df(X, y)

        processed_X = self.dummify_scale_encode(X,
                                                dummify_cols=dummify_cols,
                                                scale_cols=scale_cols,
                                                encode_cols=encode_cols)

        # cat_columns_ids = [processed_X.columns.get_loc(
        #     col) for col in processed_X.columns if col not in scale_cols]
        # self.categorical_features = cat_columns_ids

        return processed_X, y

    def _unprocess(self, X, y):
        unprocessed_X = self.undo_dummify_scale_encode(X)
        # unprocessed_X = X
        return unprocessed_X, y

    def _try_fit_resample(self, X, y):
        if self.k_neighbors > 0:
            X_resampled, y_resampled = self.fit_resample(
                X, y)
        else:
            raise ValueError("Couldn't apply BalanceOutput with SMOTE: at least one class of the " +
                             "protected attribute has only one element, and SMOTE needs at least two.")

        return X_resampled, y_resampled


class BorderSMOTEProcessor(BorderlineSMOTE, BaseProcessor, ProcessorMixin):
    def __init__(self, prefix_sep: str = "~", force: bool = False, **kwargs):
        BorderlineSMOTE.__init__(self, **kwargs)
        BaseProcessor.__init__(self, prefix_sep=prefix_sep, force=force)

    def _process(self, X, y, dummify_cols=None, scale_cols=None, encode_cols=None, protected_attribute=None):
        # assert y.value_counts().min(
        # ) > self.k_neighbors, f"Not enough elements of value {y.value_counts().index[-1]}: only {y.value_counts().min()} but should be >= {self.k_neighbors}"
        self.k_neighbors = min(y.value_counts().min() - 1, 5)

        if self.force:
            X, y = self._force_transform_df(X, y)

        processed_X = self.dummify_scale_encode(X,
                                                dummify_cols=dummify_cols,
                                                scale_cols=scale_cols,
                                                encode_cols=encode_cols)

        # cat_columns_ids = [processed_X.columns.get_loc(
        #     col) for col in processed_X.columns if col not in scale_cols]
        # self.categorical_features = cat_columns_ids

        return processed_X, y

    def _unprocess(self, X, y):
        unprocessed_X = self.undo_dummify_scale_encode(X)
        # unprocessed_X = X
        return unprocessed_X, y

    def _try_fit_resample(self, X, y):

        if self.k_neighbors > 0:
            X_resampled, y_resampled = self.fit_resample(
                X, y)
        else:
            raise ValueError("Couldn't apply BalanceOutput with BorderlineSMOTE: at least one class of the " +
                             "protected attribute has only one element, and BorderlineSMOTE needs at least two.")

        return X_resampled, y_resampled


class SMOTENCProcessor(SMOTENC, BaseProcessor, ProcessorMixin):
    """Extension of the SMOTENC class by imbalance-learn to fit in the fairbalance framework.
    Formally, it simply adds two functions self._process and self._unprocess used in the mitigation strategy.

    Parameters
    ----------
    prefix_sep : str, optional
        The prefix separator used in the dumlifying process. Passed to the BaseProcessor parent class.
    **kwargs :
        Argument for the imblearn.over_sampling.SMOTENC parent class.

    """

    def __init__(self, prefix_sep: str = "~", force: bool = False, **kwargs):
        SMOTENC.__init__(self, categorical_features=[], **kwargs)
        BaseProcessor.__init__(self, prefix_sep=prefix_sep, force=force)

    def _process(self, X, y, dummify_cols=None, scale_cols=None, encode_cols=None, protected_attribute=None):
        # assert y.value_counts().min(
        # ) > self.k_neighbors, f"Not enough elements of value {y.value_counts().index[-1]}: only {y.value_counts().min()} but should be >= {self.k_neighbors}"
        # processed_X = self.dummify_scale_encode(X,
        #                                         dummify_cols=dummify_cols,
        #                                         scale_cols=scale_cols,
        #                                         encode_cols=encode_cols)
        # cat_columns_ids = [processed_X.columns.get_loc(
        #     col) for col in processed_X.columns if col not in scale_cols]
        # self.categorical_features = cat_columns_ids
        # self.k_neighbors = min(y.value_counts().min(), 6)
        # self.set_params({"k_neighbors": min(y.value_counts().min(), 6)})
        self.k_neighbors = min(y.value_counts().min() - 1, 5)

        if self.force:
            X, y = self._force_transform_df(X, y)

        cat_columns_ids = [X.columns.get_loc(
            col) for col in X.columns if col not in scale_cols]
        self.categorical_features = cat_columns_ids

        processed_X = X
        return processed_X, y

    def _unprocess(self, X, y):
        # unprocessed_X = self.undo_dummify_scale_encode(X)
        unprocessed_X = X
        return unprocessed_X, y

    def _try_fit_resample(self, X, y):

        if self.k_neighbors > 0:
            X_resampled, y_resampled = self.fit_resample(
                X, y)
        else:
            raise ValueError("Couldn't apply BalanceOutput with BorderlineSMOTE: at least one class of the " +
                             "protected attribute has only one element, and BorderlineSMOTE needs at least two.")

        return X_resampled, y_resampled
