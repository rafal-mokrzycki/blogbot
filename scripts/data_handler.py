from transformers import pipeline


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
        )


class Distributor:
    pass
