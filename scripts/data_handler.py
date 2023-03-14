from transformers import pipeline

from scripts.gcs_connector import GCS_Connector


class Collector:
    pass


class Transformer:
    def __init__():
        pass

    def transform(
        input: str,
        temperature=0.6,
        max_length: int = 256,
        n_sentences: int = 1,
    ):
        """Transforms an input sentence into a longer paragraph.

        Args:
            input (str): _description_
            max_length (int, optional): _description_. Defaults to 256.
            n_sentences (int, optional): _description_. Defaults to 1.

        Returns:
            list: _description_
        """
        generator = pipeline(
            "text-generation", model="EleutherAI/gpt-neo-125M"
        )
        return generator(
            input,
            do_sample=True,
            top_k=50,
            temperature=temperature,
            max_length=max_length,
            num_return_sequences=n_sentences,
            pad_token_id=generator.tokenizer.eos_token_id,
        )[0]["generated_text"]

    def save_to_gcs(self, string: str = None, input: str = None) -> None:
        g = GCS_Connector()

        if string is None:
            if input is None:
                raise ValueError("Input string cannot be empty.")
            string = self.transform(input)
        g.write_blob_to_bucket(
            string, g.get_user_bucket(), g.create_unique_blob_name()
        )


class Distributor:
    pass
