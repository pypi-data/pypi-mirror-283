import logging
import os

from openai import AsyncAzureOpenAI, AzureOpenAI, OpenAIError

from r2r.base import EmbeddingConfig, EmbeddingProvider, VectorSearchResult

logger = logging.getLogger(__name__)


class AzureOpenAIEmbeddingProvider(EmbeddingProvider):
    MODEL_TO_TOKENIZER = {
        "text-embedding-ada-002": "cl100k_base",
        "text-embedding-3-small": "cl100k_base",
        "text-embedding-3-large": "cl100k_base",
    }
    MODEL_TO_DIMENSIONS = {
        "text-embedding-ada-002": [512, 1536],
        "text-embedding-3-small": [512, 1536],
        "text-embedding-3-large": [256, 512, 1024, 3072],
    }

    def __init__(self, config: EmbeddingConfig):
        super().__init__(config)
        provider = config.provider
        if not provider:
            raise ValueError(
                "Must set provider in order to initialize AzureOpenAIEmbeddingProvider."
            )

        if provider != "azure-openai":
            raise ValueError(
                "AzureOpenAIEmbeddingProvider must be initialized with provider `azure`."
            )
        if not os.getenv("AZURE_OPENAI_API_KEY"):
            raise ValueError(
                "Must set AZURE_OPENAI_API_KEY in order to initialize AzureOpenAIEmbeddingProvider."
            )
        if not os.getenv("AZURE_OPENAI_ENDPOINT"):
            raise ValueError(
                "Must set AZURE_OPENAI_ENDPOINT in order to initialize AzureOpenAIEmbeddingProvider."
            )
        if not os.getenv("AZURE_DEPLOYMENT_NAME"):
            raise ValueError(
                "Must set AZURE_DEPLOYMENT_NAME in order to initialize AzureOpenAIEmbeddingProvider."
            )
        if not os.getenv("AZURE_OPENAI_API_VERSION"):
            raise ValueError(
                "Must set AZURE_OPENAI_API_VERSION in order to initialize AzureOpenAIEmbeddingProvider."
            )

        self.client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )
        self.async_client = AsyncAzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )

        if config.rerank_model:
            raise ValueError(
                "AzureOpenAIEmbeddingProvider does not support separate reranking."
            )
        self.base_model = config.base_model
        self.base_dimension = config.base_dimension

        if (
            self.base_model
            not in AzureOpenAIEmbeddingProvider.MODEL_TO_TOKENIZER
        ):
            raise ValueError(
                f"OpenAI embedding model {self.base_model} not supported."
            )
        if (
            self.base_dimension
            and self.base_dimension
            not in AzureOpenAIEmbeddingProvider.MODEL_TO_DIMENSIONS[
                self.base_model
            ]
        ):
            raise ValueError(
                f"Dimensions {self.base_dimension} for {self.base_model} are not supported"
            )

        if not self.base_model or not self.base_dimension:
            raise ValueError(
                "Must set base_model and base_dimension in order to initialize AzureOpenAIEmbeddingProvider."
            )

    def get_embedding(
        self,
        text: str,
        stage: EmbeddingProvider.PipeStage = EmbeddingProvider.PipeStage.BASE,
    ) -> list[float]:
        if stage != EmbeddingProvider.PipeStage.BASE:
            raise ValueError(
                "AzureOpenAIEmbeddingProvider only supports search stage."
            )

        try:
            return (
                self.client.embeddings.create(
                    input=[text],
                    model=self.base_model,
                    dimensions=self.base_dimension
                    or AzureOpenAIEmbeddingProvider.MODEL_TO_DIMENSIONS[
                        self.base_model
                    ][-1],
                )
                .data[0]
                .embedding
            )
        except OpenAIError as e:
            raise ValueError(
                "Error while fetching embedding from Azure OpenAI. Please check your API key and endpoint."
            ) from e

    async def async_get_embedding(
        self,
        text: str,
        stage: EmbeddingProvider.PipeStage = EmbeddingProvider.PipeStage.BASE,
    ) -> list[float]:
        if stage != EmbeddingProvider.PipeStage.BASE:
            raise ValueError(
                "AzureOpenAIEmbeddingProvider only supports search stage."
            )

        try:
            response = await self.async_client.embeddings.create(
                input=[text],
                model=self.base_model,
                dimensions=self.base_dimension
                or AzureOpenAIEmbeddingProvider.MODEL_TO_DIMENSIONS[
                    self.base_model
                ][-1],
            )
            return response.data[0].embedding
        except OpenAIError as e:
            raise ValueError(
                "Error while fetching embedding from Azure OpenAI. Please check your API key and endpoint."
            ) from e

    def get_embeddings(
        self,
        texts: list[str],
        stage: EmbeddingProvider.PipeStage = EmbeddingProvider.PipeStage.BASE,
    ) -> list[list[float]]:
        if stage != EmbeddingProvider.PipeStage.BASE:
            raise ValueError(
                "AzureOpenAIEmbeddingProvider only supports search stage."
            )

        try:
            return [
                ele.embedding
                for ele in self.client.embeddings.create(
                    input=texts,
                    model=self.base_model,
                    dimensions=self.base_dimension
                    or AzureOpenAIEmbeddingProvider.MODEL_TO_DIMENSIONS[
                        self.base_model
                    ][-1],
                ).data
            ]
        except OpenAIError as e:
            raise ValueError(
                "Error while fetching embeddings from Azure OpenAI. Please check your API key and endpoint."
            ) from e

    async def async_get_embeddings(
        self,
        texts: list[str],
        stage: EmbeddingProvider.PipeStage = EmbeddingProvider.PipeStage.BASE,
    ) -> list[list[float]]:
        if stage != EmbeddingProvider.PipeStage.BASE:
            raise ValueError(
                "AzureOpenAIEmbeddingProvider only supports search stage."
            )

        try:
            response = await self.async_client.embeddings.create(
                input=texts,
                model=self.base_model,
                dimensions=self.base_dimension
                or AzureOpenAIEmbeddingProvider.MODEL_TO_DIMENSIONS[
                    self.base_model
                ][-1],
            )
            return [ele.embedding for ele in response.data]
        except OpenAIError as e:
            raise ValueError(
                "Error while fetching embeddings from Azure OpenAI. Please check your API key and endpoint."
            ) from e

    def rerank(
        self,
        query: str,
        results: list[VectorSearchResult],
        stage: EmbeddingProvider.PipeStage = EmbeddingProvider.PipeStage.RERANK,
        limit: int = 10,
    ):
        return results[:limit]

    def tokenize_string(self, text: str, model: str) -> list[int]:
        try:
            import tiktoken
        except ImportError:
            raise ValueError(
                "Must download tiktoken library to run `tokenize_string`."
            )
        # tiktoken encoding -
        # cl100k_base - gpt-4, gpt-3.5-turbo, text-embedding-ada-002, text-embedding-3-small, text-embedding-3-large
        if model not in AzureOpenAIEmbeddingProvider.MODEL_TO_TOKENIZER:
            raise ValueError(f"OpenAI embedding model {model} not supported.")
        encoding = tiktoken.get_encoding(
            AzureOpenAIEmbeddingProvider.MODEL_TO_TOKENIZER[model]
        )
        return encoding.encode(text)
