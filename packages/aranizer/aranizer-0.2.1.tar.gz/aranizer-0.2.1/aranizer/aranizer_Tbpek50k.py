import pkg_resources
from transformers import PreTrainedTokenizerFast

def get_tokenizer():
    """
    Initializes and returns a custom tokenizer for Arabic language processing.

    This function loads a tokenizer from a predefined file and enriches its
    vocabulary with a set of Arabic diacritics as special tokens. The tokenizer
    is based on the PreTrainedTokenizerFast class from the transformers library.

    Returns:
        PreTrainedTokenizerFast: A tokenizer with extended vocabulary to
                                 include Arabic diacritics.
    """
    # Locate the tokenizer file using pkg_resources
    tokenizer_path = pkg_resources.resource_filename(__name__, 'BPE_Moshakal_Tokenizer/TBPE_tokenizer_50.0K.json')

    # Initialize the tokenizer
    tokenizer_fast = PreTrainedTokenizerFast(tokenizer_file=tokenizer_path)


    return tokenizer_fast
