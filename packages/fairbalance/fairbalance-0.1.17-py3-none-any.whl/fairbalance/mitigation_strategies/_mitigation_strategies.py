from .base import BaseMitigationStrategy
import pandas as pd
import copy
import warnings


class BalanceOutput(BaseMitigationStrategy):
    """
    Balances the outputs of the dataset with no regards to the protected attributes.

    Parameters
    ----------
    processor : processors.BaseProcessor
        Defines the sampling method to balance the output.
        Object must inherit from the processors.BaseProcessor class.
        Current available sampling methods are RandomOverSamplerProcessor, SMOTENCProcessor and
        RandomUnderSamplingProcessor.

    """

    def __init__(self, processor=None):
        super().__init__(processor)

    def _resample_single_attr(self,
                              X,
                              y,
                              protected_attribute=None,
                              cont_columns=None,
                              cat_columns=None
                              ):

        if protected_attribute and (protected_attribute not in cat_columns):
            cat_columns.append(protected_attribute)

        X_processed, y_processed = self.processor.process(X,
                                                          y,
                                                          scale_cols=cont_columns,
                                                          dummify_cols=cat_columns,
                                                          protected_attribute=protected_attribute)

        X_resampled, y_resampled = self.processor._try_fit_resample(
            X_processed, y_processed)

        X_final, y_final = self.processor.unprocess(X_resampled, y_resampled)

        X_final = X_final.reset_index(drop=True)
        y_final = y_final.reset_index(drop=True)

        return X_final, y_final


class BalanceAttributes(BaseMitigationStrategy):
    """
    Balances the protected attributes given to the balance() method with no regards to the output.

    Parameters
    ----------
    processor : processors.BaseProcessor
        Defines the sampling method to balance the output.
        Object must inherit from the processors.BaseProcessor class.
        Current available sampling methods are RandomOverSamplerProcessor, SMOTENCProcessor and
        RandomUnderSamplingProcessor.

    """

    def __init__(self, processor=None):
        super().__init__(processor)

    def _resample_single_attr(self,
                              X,
                              y,
                              protected_attribute=None,
                              cont_columns=None,
                              cat_columns=None
                              ):

        assert protected_attribute is not None, "Protected attribute(s) needs to be defined"

        dummify_cols = [
            column for column in cat_columns if column != protected_attribute]

        # Isolate protected attribute and put target in df
        protected_attribute_column = X[protected_attribute]
        X = X.drop(columns=[protected_attribute])
        X.loc[:, y.columns[0]] = y

        # new_cat_columns = [
        #     column for column in X_processed if column not in cont_columns]
        # cat_columns_ids = [X_processed.columns.get_loc(
        #     col_name) for col_name in new_cat_columns]

        # self.processor.set_categorical_features(cat_columns_ids)

        X_processed, protected_attribute_column_processed = self.processor.process(X,
                                                                                   protected_attribute_column,
                                                                                   scale_cols=cont_columns,
                                                                                   dummify_cols=dummify_cols,
                                                                                   protected_attribute=protected_attribute)

        # self.processor.k_neighbors = min(
        #     protected_attribute_column.value_counts().min(), 6)

        X_resampled, protected_attribute_resampled = self.processor._try_fit_resample(
            X_processed, protected_attribute_column_processed)

        X_final, protected_attribute_final = self.processor.unprocess(
            X_resampled, protected_attribute_resampled)

        # put protected attribute in df and isolate target
        X_final.loc[:, protected_attribute] = protected_attribute_final
        y_final = X_final[[y.columns[0]]]
        X_final = X_final.drop(columns=[y.columns[0]])

        X_final = X_final.reset_index(drop=True)
        y_final = y_final.reset_index(drop=True)
        return X_final, y_final


class BalanceOutputForAttributes(BaseMitigationStrategy):
    """
    Balances the outputs of the protected attributes given to the balance().

    Parameters
    ----------
    processor : processors.BaseProcessor
        Defines the sampling method to balance the output.
        Object must inherit from the processors.BaseProcessor class.
        Current available sampling methods are RandomOverSamplerProcessor, SMOTENCProcessor and
        RandomUnderSamplingProcessor.


    """

    def __init__(self, processor=None):
        super().__init__(processor)

    def _resample_single_attr(self,
                              X: pd.DataFrame,
                              y: pd.DataFrame,
                              protected_attribute: list = None,
                              cont_columns: list = None,
                              cat_columns: list = None
                              ):

        assert protected_attribute, "Protected attribute(s) needs to be defined"

        # set empty DataFrames
        X_final = pd.DataFrame(columns=X.columns)
        y_final = pd.DataFrame(columns=y.columns, dtype=y.dtypes[y.columns[0]])

        highest_r, class_with_highest_r = self._highest_ratio(
            X, y, protected_attribute)
        self.processor.sampling_strategy = highest_r
        classes = list(X[protected_attribute].unique())

        for class_ in classes:
            # keep only the rows with given class
            class_df = X[X[protected_attribute] == class_]
            class_target = y[X[protected_attribute] == class_]

            if class_ != class_with_highest_r:
                # resample the target for this class
                if len(class_target[y.columns[0]].unique()) > 1:
                    # self.processor.set_params({"k_neighbors": min(
                    #     class_target.value_counts().min(), 6)})
                    X_processed, y_processed = self.processor.process(
                        class_df, class_target, scale_cols=cont_columns, dummify_cols=cat_columns,
                        protected_attribute=protected_attribute)
                    try:
                        X_resampled, y_resampled = self.processor._try_fit_resample(
                            X_processed, y_processed)
                    except ValueError:
                        # When cant oversample because ratio is too close
                        X_resampled, y_resampled = X_processed, y_processed
                    X_class_final, y_class_final = self.processor.unprocess(
                        X_resampled, y_resampled)
                else:
                    X_class_final = class_df
                    y_class_final = class_target

                # append the resampled class in final dfs
                X_final = pd.concat(
                    [X_final, X_class_final], ignore_index=True)
                y_final = pd.concat([y_final, y_class_final])

            else:
                X_final = pd.concat([X_final, class_df], ignore_index=True)
                y_final = pd.concat([y_final, class_target])

        X_final = X_final.reset_index(drop=True)
        y_final = y_final.reset_index(drop=True)
        return X_final, y_final


class CompleteBalance():
    """
    Balances the classes of the given protected attributes and their output.

    Parameters
    ----------
    processor : processors.BaseProcessor
        Defines the sampling method to balance output of the protected attribute(s).
        Object must inherit from the processors.BaseProcessor class.
        Current available sampling methods are RandomOverSamplerProcessor, SMOTENCProcessor and
        RandomUnderSamplingProcessor.
    second_processor : processors.BaseProcessor
        Defines the sampling method to balance classes of the protected attribute(s). .
        Object must inherit from the processors.BaseProcessor class.
        If None, uses the same sampler as the first one.
        Current available sampling methods are RandomOverSamplerProcessor, SMOTENCProcessor and
        RandomUnderSamplingProcessor.
    """

    def __init__(self, processor=None, second_processor=None):
        self.first_mitig = BalanceOutputForAttributes(processor=processor)
        if second_processor:
            self.second_mitig = BalanceAttributes(processor=second_processor)
        else:
            self.second_mitig = BalanceAttributes(
                processor=copy.deepcopy(processor))

    def resample(self,
                 X: pd.DataFrame,
                 y: pd.DataFrame,
                 protected_attributes: list = None,
                 cont_columns: list = None,
                 cat_columns: list = None
                 ):

        print("BOFA")
        X_inter, y_inter = self.first_mitig.resample(X=X,
                                                     y=y,
                                                     protected_attributes=protected_attributes,
                                                     cont_columns=cont_columns,
                                                     cat_columns=cat_columns
                                                     )

        # print(X_inter)
        # print(y_inter)

        print("BA")
        X_final, y_final = self.second_mitig.resample(X=X_inter,
                                                      y=y_inter,
                                                      protected_attributes=protected_attributes,
                                                      cont_columns=cont_columns,
                                                      cat_columns=cat_columns
                                                      )

        return X_final, y_final
