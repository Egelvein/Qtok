
class TokenizerMetricsCalculation:

    def __init__(self, vocab, stats, core_tokens, singletons):
        self.vocab = vocab
        self.stats = stats
        self.core_tokens = core_tokens
        self.singletons = singletons

        self.__len_vocab = len(self.vocab)
        self.__space_start = len(self.stats["space_start"])
        self.__percent_space_start = (self.__space_start / self.__len_vocab) * 100
        self.__core_tokens_in_tokenizer = self.core_tokens_representation()
        self.__percent_core_tokens = (self.__core_tokens_in_tokenizer / len(self.core_tokens)) * 100
        # self.singletons
        self.__percent_singletons = (self.singletons / self.__space_start) * 100

    def core_tokens_representation(self):
        core_tokens_in_tokenizer: int = 0
        for token in self.vocab:
            if token in self.core_tokens:
                core_tokens_in_tokenizer += 1
        return core_tokens_in_tokenizer

    # def metrics_calculation(self):
    #     self.__len_vocab = len(self.vocab)
    #     self.__space_start = len(self.stats["space_start"])
    #     self.__percent_space_start = (self.__space_start / self.__len_vocab) * 100
    #     self.__core_tokens_in_tokenizer = self.core_tokens_representation()
    #     self.__percent_core_tokens = (self.__core_tokens_in_tokenizer / self.core_tokens) * 100
    #     # self.singletons
    #     self.__percent_singletons = (self.singletons / self.__space_start) * 100

    def get_metrics(self):
        return self.__len_vocab, self.__space_start, self.__percent_space_start, self.__core_tokens_in_tokenizer,\
            self.__percent_core_tokens, self.singletons, self.__percent_singletons
