import logging
from typing import List, Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

from autogluon.common.features.types import S_IMAGE_BYTEARRAY, S_IMAGE_PATH, S_TEXT, S_TEXT_SPECIAL

from .abstract import AbstractFeatureGenerator
from .binned import BinnedFeatureGenerator

logger = logging.getLogger(__name__)


class TextSpecialFeatureGenerator(AbstractFeatureGenerator):
    """
    TextSpecialFeatureGenerator generates text specific features from incoming raw text features.
    These include word counts, character counts, symbol counts, capital letter ratios, and much more.
    Features generated by this generator will have 'text_special' as a special type.

    Parameters
    ----------
    symbols : List[str], optional
        List of string symbols to compute counts and ratios for as features.
        If not specified, defaults to ['!', '?', '@', '%', '$', '*', '&', '#', '^', '.', ':', ' ', '/', ';', '-', '=']
    min_occur_ratio : float, default 0.01
        Minimum ratio of symbol occurrence to consider as a feature.
        If a symbol appears in fewer than 1 in 1/min_occur_ratio samples, it will not be used as a feature.
    min_occur_offset : int, default 10
        Minimum symbol occurrences to consider as a feature. This is added to the threshold calculated from min_occur_ratio.
    bin_features : bool, default True
        If True, adds a BinnedFeatureGenerator to the front of post_generators such that all features generated from this generator are then binned.
        This is useful for 'text_special' features because it lowers the chance models will overfit on the features and reduces their memory usage.
    post_drop_duplicates : bool, default True
        Identical to AbstractFeatureGenerator's post_drop_duplicates, except it is defaulted to True instead of False.
        This helps to clean the output of this generator when symbols aren't present in the data.
    **kwargs :
        Refer to AbstractFeatureGenerator documentation for details on valid keyword arguments.
    """

    def __init__(
        self, symbols: List[str] = None, min_occur_ratio=0.01, min_occur_offset=10, bin_features: bool = True, post_drop_duplicates: bool = True, **kwargs
    ):
        super().__init__(post_drop_duplicates=post_drop_duplicates, **kwargs)
        if symbols is None:
            symbols = ["!", "?", "@", "%", "$", "*", "&", "#", "^", ".", ":", " ", "/", ";", "-", "="]
        self._symbols = symbols  # Symbols to generate count and ratio features for.
        self._symbols_per_feature = {}
        self._min_occur_ratio = min_occur_ratio
        self._min_occur_offset = min_occur_offset
        if bin_features:
            self._post_generators = [BinnedFeatureGenerator()] + self._post_generators

    def _fit_transform(self, X: DataFrame, **kwargs) -> Tuple[DataFrame, dict]:
        self._symbols_per_feature = self._filter_symbols(X, self._symbols)
        self._feature_names_dict = self._compute_feature_names_dict()
        X_out = self._transform(X)
        type_family_groups_special = {S_TEXT_SPECIAL: list(X_out.columns)}
        return X_out, type_family_groups_special

    def _transform(self, X: DataFrame) -> DataFrame:
        return self._generate_features_text_special(X)

    def _compute_feature_names_dict(self) -> dict:
        feature_names = {}
        for feature in self.features_in:
            feature_names_cur = {}
            for feature_name_base in ["char_count", "word_count", "capital_ratio", "lower_ratio", "digit_ratio", "special_ratio"]:
                feature_names_cur[feature_name_base] = f"{feature}.{feature_name_base}"
            symbols = self._symbols_per_feature[feature]
            for symbol in symbols:
                feature_names_cur[symbol] = {"count": f"{feature}.symbol_count.{symbol}", "ratio": f"{feature}.symbol_ratio.{symbol}"}
            feature_names[feature] = feature_names_cur
        return feature_names

    @staticmethod
    def get_default_infer_features_in_args() -> dict:
        return dict(required_special_types=[S_TEXT], invalid_special_types=[S_IMAGE_PATH, S_IMAGE_BYTEARRAY])

    def _filter_symbols(self, X: DataFrame, symbols: list) -> dict:
        symbols_per_feature = {}
        if self.features_in:
            num_samples = len(X)
            symbol_occur_threshold = min(np.ceil(self._min_occur_offset + num_samples * self._min_occur_ratio), np.ceil(num_samples / 2))
            for text_feature_name in self.features_in:
                above_threshold_symbols = []
                text_feature = X[text_feature_name].astype(str)
                for symbol in symbols:
                    symbol_occur_count = text_feature.str.contains(symbol, regex=False).sum()
                    if symbol_occur_count >= symbol_occur_threshold:
                        above_threshold_symbols.append(symbol)
                symbols_per_feature[text_feature_name] = np.array(above_threshold_symbols)
        return symbols_per_feature

    def _generate_features_text_special(self, X: DataFrame) -> DataFrame:
        if self.features_in:
            X_text_special_combined = {}
            for text_feature in self.features_in:
                X_text_special_combined = self._generate_text_special(
                    X[text_feature], text_feature, symbols=self._symbols_per_feature[text_feature], X_dict=X_text_special_combined
                )
            X_text_special_combined = pd.DataFrame(X_text_special_combined, index=X.index)
        else:
            X_text_special_combined = pd.DataFrame(index=X.index)
        return X_text_special_combined

    def _generate_text_special(self, X: Series, feature: str, symbols: list, X_dict: dict) -> dict:
        fn = self._feature_names_dict[feature]
        X_str = X.astype(str)

        X_no_ws = X_str.str.replace(" ", "")
        X_no_ws_text_len = X_no_ws.str.len()

        char_count = X_str.str.len()

        X_dict[fn["char_count"]] = char_count.to_numpy(dtype=np.uint32)
        X_dict[fn["word_count"]] = X_str.str.split().str.len().to_numpy(dtype=np.uint32)
        X_dict[fn["capital_ratio"]] = X_no_ws.str.count("[A-Z]").divide(X_no_ws_text_len, fill_value=0.0).fillna(0.0).to_numpy(dtype=np.float32)
        X_dict[fn["lower_ratio"]] = X_no_ws.str.count("[a-z]").divide(X_no_ws_text_len, fill_value=0.0).fillna(0.0).to_numpy(dtype=np.float32)
        X_dict[fn["digit_ratio"]] = X_no_ws.str.count("[0-9]").divide(X_no_ws_text_len, fill_value=0.0).fillna(0.0).to_numpy(dtype=np.float32)
        X_dict[fn["special_ratio"]] = X_no_ws.str.count(r"[^\w]").divide(X_no_ws_text_len, fill_value=0.0).fillna(0.0).to_numpy(dtype=np.float32)

        for symbol in symbols:
            symbol_count = X_str.str.count("\\" + symbol)
            X_dict[fn[symbol]["count"]] = symbol_count.to_numpy(dtype=np.uint32)
            X_dict[fn[symbol]["ratio"]] = symbol_count.divide(char_count, fill_value=0.0).fillna(0.0).to_numpy(dtype=np.float32)

        return X_dict

    def _remove_features_in(self, features: list):
        super()._remove_features_in(features)
        if self._symbols_per_feature:
            for feature in features:
                if feature in self._symbols_per_feature:
                    self._symbols_per_feature.pop(feature)
