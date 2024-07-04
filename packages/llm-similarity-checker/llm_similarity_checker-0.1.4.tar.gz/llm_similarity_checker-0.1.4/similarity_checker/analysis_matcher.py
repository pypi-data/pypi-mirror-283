import joblib
import torch
from torch.nn.functional import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import os


class AnalysisMatcher:
    """
    Class for sentence similarity analysis using transformer models.

    Attributes:
        tokenizer (AutoTokenizer): Tokenizer for tokenizing input sentences.
        model (AutoModel): Transformer model for computing sentence embeddings.
    """

    def __init__(self, tokenizer_path=None, model_path=None):
        """
        Initializes the AnalysisMatcher instance.

        Args:
            tokenizer_path (str, optional): Path to tokenizer file if loading from file.
            model_path (str, optional): Path to model file if loading from file.
        """
        if tokenizer_path and model_path:
            self.tokenizer = joblib.load(tokenizer_path)
            self.model = joblib.load(model_path)
        else:
            self.load_from_pretrained()

    def load_from_pretrained(self, model_name='tum-nlp/NegMPNet'):
        """
        Loads tokenizer and model from a pretrained model or saves them if not already loaded.

        Args:
            model_name (str, optional): Name of the pretrained model to load.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

        # Create the directory if it doesn't exist
        if not os.path.exists("trained_models/"):
            os.makedirs("trained_models/")
            print(f"Directory created: trained_models/")
        else:
            print(f"Directory already exists: trained_models/")

        joblib.dump(self.tokenizer, 'trained_models/tokenizer.joblib')
        joblib.dump(self.model, 'trained_models/model.joblib')

    def mean_pooling(self, model_output, attention_mask) -> torch.Tensor:
        """
        Perform mean pooling of token embeddings with attention mask for correct averaging.

        Args:
            model_output (tuple): A tuple containing the model outputs. Typically, the first element
                                 (model_output[0]) should contain the token embeddings.
            attention_mask (torch.Tensor): Tensor indicating the attention mask. Should be of shape
                                           (batch_size, sequence_length) with 0s for padding tokens
                                           and 1s for non-padding tokens.

        Returns:
            torch.Tensor: Mean-pooled embeddings for each input sequence in the batch.
                          Shape: (batch_size, embedding_dim)
        """
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()

        # Calculate sum of token embeddings across sequence while considering the attention mask
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)

        # Calculate the total number of non-padding tokens in each sequence
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)

        # Compute mean embeddings by dividing the sum by the number of tokens
        mean_embeddings = sum_embeddings / sum_mask

        return mean_embeddings

    def get_sentence_embedding(self, sentences: list[str]) -> torch.Tensor:
        """
        Computes sentence embeddings for a list of sentences using the loaded model.

        Args:
            sentences (list[str]): List of input sentences.

        Returns:
            torch.Tensor: Sentence embeddings for each input sentence.
                          Shape: (batch_size, embedding_dim)
        """
        inputs = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Perform pooling. In this case, mean pooling.
        sentence_embeddings = self.mean_pooling(outputs, inputs['attention_mask'])

        return sentence_embeddings

    def match(self, sentence1: str, sentence2: str, threshold: float = 0.6) -> tuple[float, bool]:
        """
        Computes similarity score between two sentences and compares it against a threshold.

        Args:
            sentence1 (str): First input sentence.
            sentence2 (str): Second input sentence.
            threshold (float, optional): Similarity threshold for matching. Defaults to 0.6.

        Returns:
            tuple[float, bool]: Similarity score between sentence1 and sentence2,
                                 and a boolean indicating if the score is above the threshold.
        """
        sentences = [sentence1, sentence2]
        sentence_embeddings = self.get_sentence_embedding(sentences)
        similarity_score = cosine_similarity(sentence_embeddings[0].unsqueeze(0), sentence_embeddings[1].unsqueeze(0))
        return similarity_score.item(), similarity_score.item() > threshold
