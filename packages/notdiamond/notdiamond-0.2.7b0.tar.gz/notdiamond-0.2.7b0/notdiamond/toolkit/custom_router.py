import json
import tempfile
from collections import OrderedDict
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import requests

from notdiamond.exceptions import ApiError
from notdiamond.llms.llm import NDLLM
from notdiamond.llms.provider import NDLLMProvider
from notdiamond.settings import ND_BASE_URL, NOTDIAMOND_API_KEY
from notdiamond.types import NDApiKeyValidator


class CustomRouter:
    """
    Implementation of CustomRouter class, used to train custom routers using custom datasets.
    """

    language: str = "english"
    """The language that the dataset is in. Default is 'english'."""

    maximize: bool = True
    """Whether the training objective is maximizing. Default to True."""

    api_key: Optional[str] = None
    """
    API key required for making calls to NotDiamond.
    You can get an API key via our dashboard: https://app.notdiamond.ai
    If an API key is not set, it will check for NOTDIAMOND_API_KEY in .env file.
    """

    def __init__(
        self,
        language: str = "english",
        maximize: bool = True,
        api_key: Optional[str] = None,
    ):
        if api_key is None:
            api_key = NOTDIAMOND_API_KEY
        NDApiKeyValidator(api_key=api_key)

        self.api_key = api_key
        self.language = language
        self.maximize = maximize

    def _request_train_router(
        self,
        prompt_column: str,
        dataset_file: str,
        llm_providers: List[NDLLMProvider],
        preference_id: Optional[str],
    ) -> str:
        url = f"{ND_BASE_URL}/v2/pzn/trainCustomRouter"

        files = {"dataset_file": open(dataset_file, "rb")}

        payload = {
            "language": self.language,
            "llm_providers": json.dumps(
                [provider.prepare_for_request() for provider in llm_providers]
            ),
            "prompt_column": prompt_column,
            "maximize": self.maximize,
            "preference_id": preference_id,
        }

        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = requests.post(
            url=url, headers=headers, data=payload, files=files
        )
        if response.status_code != 200:
            raise ApiError(
                f"ND backend error status code: {response.status_code}, {response.text}"
            )

        preference_id = response.json()["preference_id"]
        return preference_id

    def _prepare_joint_dataset(
        self,
        dataset: Dict[str, pd.DataFrame],
        prompt_column: str,
        response_column: str,
        score_column: str,
    ) -> Tuple[pd.DataFrame, List[NDLLMProvider]]:
        a_provider = list(dataset.keys())[0]
        prompts = dataset[a_provider].get(prompt_column, None)
        if prompts is None:
            raise ValueError(f"Prompt column {prompt_column} not found in df.")
        prompts = prompts.to_list()

        llm_providers = []
        joint_dataset = {prompt_column: prompts}
        for provider, df in dataset.items():
            llm_providers.append(provider)

            responses = df.get(response_column, None)
            if responses is None:
                raise ValueError(
                    f"Response column {response_column} not found in df."
                )
            responses = responses.to_list()
            joint_dataset[f"{provider}/response"] = responses

            scores = df.get(score_column, None)
            if scores is None:
                raise ValueError(
                    f"Score column {score_column} not found in df."
                )
            scores = scores.to_list()
            joint_dataset[f"{provider}/score"] = scores

        joint_df = pd.DataFrame(joint_dataset)

        llm_providers = NDLLM._parse_llm_providers_data(llm_providers)
        return joint_df, llm_providers

    def fit(
        self,
        dataset: Dict[str, pd.DataFrame],
        prompt_column: str,
        response_column: str,
        score_column: str,
        preference_id: Optional[str] = None,
    ) -> str:
        """
        Method to train a custom router using provided dataset.

        Parameters:
            dataset (Dict[str, pandas.DataFrame]): The dataset to train a custom router.
                Each key in the dictionary should be in the form of <provider>/<model>.
            prompt_column (str): The column name in each DataFrame corresponding
                to the prompts used to evaluate the LLM.
            response_column (str): The column name in each DataFrame corresponding
                to the response given by the LLM for a given prompt.
            score_column (str): The column name in each DataFrame corresponding
                to the score given to the response from the LLM.
            preference_id (Optional[str], optional): If specified, the custom router
                associated with the preference_id will be updated with the provided dataset.

        Raises:
            ApiError: When the NotDiamond API fails
            ValueError: When parsing the provided dataset fails
            UnsupportedLLMProvider: When a provider specified in the dataset is not supported.

        Returns:
            str:
                preference_id: the preference_id associated with the custom router.
                    Use this preference_id in your routing calls to use the custom router.
        """

        joint_df, llm_providers = self._prepare_joint_dataset(
            dataset, prompt_column, response_column, score_column
        )

        with tempfile.NamedTemporaryFile(suffix=".csv") as joint_csv:
            joint_df.to_csv(joint_csv.name, index=False)
            preference_id = self._request_train_router(
                prompt_column, joint_csv.name, llm_providers, preference_id
            )

        return preference_id

    def _eval_custom_router(
        self,
        client: NDLLM,
        llm_providers: List[NDLLMProvider],
        joint_df: pd.DataFrame,
        prompt_column: str,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        eval_results = OrderedDict()
        eval_results[prompt_column] = []
        eval_results["session_id"] = []
        provider_score_columns = []

        for provider in llm_providers:
            provider_score = f"{provider.provider}/{provider.model}/score"
            eval_results[provider_score] = []
            provider_score_columns.append(provider_score)

            provider_response = (
                f"{provider.provider}/{provider.model}/response"
            )
            eval_results[provider_response] = []

        eval_results["notdiamond/score"] = []
        eval_results["notdiamond/response"] = []

        nd_score = None
        for _, row in joint_df.iterrows():
            prompt = row[prompt_column]
            eval_results[prompt_column].append(prompt)

            session_id, nd_provider = client.chat.completions.model_select(
                messages=[{"role": "user", "content": prompt}],
            )
            eval_results["session_id"].append(session_id)

            for provider in llm_providers:
                provider_score = row[
                    f"{provider.provider}/{provider.model}/score"
                ]
                eval_results[
                    f"{provider.provider}/{provider.model}/score"
                ].append(provider_score)

                provider_response = row[
                    f"{provider.provider}/{provider.model}/response"
                ]
                eval_results[
                    f"{provider.provider}/{provider.model}/response"
                ].append(provider_response)

                if (
                    provider.provider == nd_provider.provider
                    and provider.model == nd_provider.model
                ):
                    nd_score = provider_score
                    nd_response = provider_response

            if nd_score is None:
                raise ValueError(
                    f"""
                    Custom router returned {nd_provider.provider}/{nd_provider.model}
                    which is not in the set of models in the test dataset
                    """
                )

            eval_results["notdiamond/score"].append(nd_score)
            eval_results["notdiamond/response"].append(nd_response)

        eval_results_df = pd.DataFrame(eval_results)

        best_average_provider = None
        best_average_score = -(2 * int(self.maximize) - 1) * np.inf
        for provider in llm_providers:
            provider_avg_score = eval_results_df[
                f"{provider.provider}/{provider.model}/score"
            ].mean()
            if self.maximize:
                if provider_avg_score > best_average_score:
                    best_average_score = provider_avg_score
                    best_average_provider = (
                        f"{provider.provider}/{provider.model}"
                    )
            else:
                if provider_avg_score < best_average_score:
                    best_average_score = provider_avg_score
                    best_average_provider = (
                        f"{provider.provider}/{provider.model}"
                    )

        nd_average_score = eval_results_df["notdiamond/score"].mean()

        eval_stats = OrderedDict()
        eval_stats["Best Average Provider"] = [best_average_provider]
        eval_stats["Best Provider Average Score"] = [best_average_score]
        eval_stats["Not Diamond Average Score"] = [nd_average_score]
        eval_stats_df = pd.DataFrame(eval_stats)
        return eval_results_df, eval_stats_df

    def eval(
        self,
        dataset: Dict[str, pd.DataFrame],
        prompt_column: str,
        response_column: str,
        score_column: str,
        preference_id: str,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Method to evaluate a custom router using provided dataset.

        Parameters:
            dataset (Dict[str, pandas.DataFrame]): The dataset to train a custom router.
                Each key in the dictionary should be in the form of <provider>/<model>.
            prompt_column (str): The column name in each DataFrame corresponding
                to the prompts used to evaluate the LLM.
            response_column (str): The column name in each DataFrame corresponding
                to the response given by the LLM for a given prompt.
            score_column (str): The column name in each DataFrame corresponding
                to the score given to the response from the LLM.
            preference_id (str): The preference_id associated with the custom router
                returned from .fit().

        Raises:
            ApiError: When the NotDiamond API fails
            ValueError: When parsing the provided dataset fails
            UnsupportedLLMProvider: When a provider specified in the dataset is not supported.

        Returns:
            Tuple[pandas.DataFrame, pandas.DataFrame]:
                eval_results_df: A DataFrame containing all the prompts, responses of each provider
                    (indicated by column <provider>/<model>/response), scores of each provider
                    (indicated by column <provider>/<model>/score), and notdiamond custom router
                    response and score (indicated by column notdiamond/response and notdiamond/score).
                eval_stats_df: A DataFrame containing the "Best Average Provider" computed from the
                    provided dataset, the "Best Provider Average Score" achieved by the "Best Average Provider",
                    and the "Not Diamond Average Score" achieved through custom router.
        """

        joint_df, llm_providers = self._prepare_joint_dataset(
            dataset, prompt_column, response_column, score_column
        )

        client = NDLLM(
            llm_providers=llm_providers,
            api_key=self.api_key,
            preference_id=preference_id,
        )

        eval_results_df, eval_stats_df = self._eval_custom_router(
            client, llm_providers, joint_df, prompt_column
        )
        return eval_results_df, eval_stats_df
