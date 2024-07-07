import gc
import torch
from pathlib import Path
from itertools import tee
from typing import Union, Iterable, List, Collection
from torch.nn import Embedding

from .utils import UTF8, read_file, read_corpus_files, batch_cut, batch_pad_mask, cut, batch_pad, pad, \
    filter_stop_words, pad_mask, load_embedding
from .stats import token_counter


# -------------------------------------------------Tokenizer class-----------------------------------------------------
class BaseTokenizer:
    """
    encode返回的是 list
    """
    SAVE_SEP = '\t'
    PAD, UNK, BOS, EOS, SEP = '<pad>', '<unk>', '<bos>', '<eos>', '<sep>'
    BACKUP_TOKENS = [PAD, UNK, BOS, EOS, SEP]

    def __init__(self, file: str = None, corpus: Iterable[str] = None, cut_corpus: Iterable[Iterable[str]] = None,
                 vocab: Collection[str] = None, min_freq=5, special_tokens: Collection[str] = None, language='cn',
                 cut_type='word', word_freq: bool = False, stop_words: Collection[str] = None, keep_punctuation=False,
                 cut_fn=None):
        """
        :param file: 语料文件，可以是文件也可以是文件夹， 如：'./train.txt'. 如果是文件夹，会读取文件夹下的所有目录和文件.
        :param corpus: 语料，每个元素是一句话，如：['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ...]
        :param cut_corpus: 语料，每个元素是是分词后的一句话，如：[['上课', '时', '学生', '手机', '响', '个', '不停'], ['家长', '拿', '发票', '让', '老师', '赔']]
        :param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
        :param min_freq: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
        :param special_tokens: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        :param word_freq: 是否统计词频
        :param stop_words: 停用词
        :param keep_punctuation: 是否保留标点符号
        :param cut_fn
        """
        self.language = language
        self.cut_type = cut_type
        self.stop_words = stop_words
        if cut_fn is None and language == 'cn' and cut_type == 'word':
            import jieba
            import logging
            jieba.setLogLevel(logging.INFO)
            self.cut_fn = jieba.lcut
        else:
            self.cut_fn = cut_fn
        self.special_tokens = self.BACKUP_TOKENS
        if special_tokens:
            self.special_tokens.extend([token for token in special_tokens if token not in self.BACKUP_TOKENS])
        if vocab:
            if stop_words:
                for word in stop_words:
                    if word in vocab:
                        vocab.remove(word)
                        
            if cut_fn is None and language == 'cn' and cut_type == 'word':
                for word in vocab:
                    jieba.add_word(word)
                    
            for token in {token for token in self.special_tokens if token in vocab}:
                vocab.remove(token)
                
            self.vocab = self.special_tokens + vocab if isinstance(vocab, List) else list(vocab)
            self.token_to_idx = {k: i for i, k in enumerate(self.vocab)}
            del vocab
            gc.collect()
            
        else:
            if file is not None and corpus is None:
                corpus = read_corpus_files(file)
            if corpus is not None:
                cut_corpus = batch_cut(corpus, language=language, cut_type=cut_type, keep_punctuation=keep_punctuation,
                                       cut_fn=self.cut_fn)
                del corpus
            if cut_corpus is not None:
                if stop_words:
                    cut_corpus = filter_stop_words(cut_corpus, stop_words)
                counter = token_counter(cut_corpus)
                sorted_token_freq = sorted(counter.items(), key=lambda kv: kv[1], reverse=True)
                self.vocab = self.special_tokens.copy()
                if min_freq > 0:
                    filter_tokens = filter(lambda kv: kv[1] >= min_freq and kv[0] not in self.vocab,
                                           sorted_token_freq)
                else:
                    filter_tokens = filter(lambda kv: kv[0] not in self.vocab, sorted_token_freq)

                if word_freq:
                    filter_tokens, filter_tokens_copy = tee(filter_tokens, 2)
                    self.word_freq = list(filter_tokens_copy)
                self.vocab += list(map(lambda kv: kv[0], filter_tokens))
                self.token_to_idx = {k: i for i, k in enumerate(self.vocab)}
                del sorted_token_freq, counter, cut_corpus
                gc.collect()
                
            else:
                raise ValueError('参数file, corpus, vocab不能同时为None.')
        self.vocab_size = len(self.vocab)
        self.pad, self.unk, self.bos, self.eos, self.sep = [self.token_to_idx[token] for token in self.BACKUP_TOKENS]

    def encode(self, sentence: str, max_length: int = None, truncation=True, padding=True, padding_side='right',
               pad_begin_end=False, keep_punctuation=False, is_split_into_words: bool = False):
        """
        :param sentence: '上课时学生手机响个不停，老师一怒之下把手机摔了'
        :param max_length:
        :param truncation:
        :param padding:
        :param padding_side:
        :param pad_begin_end:
        :param keep_punctuation: 是否保留标点符号
        :param is_split_into_words: 是否已经分词
        :return:
        """
        if isinstance(sentence, str):
            if is_split_into_words:
                tokens = self.do_encode(sentence)
            else:
                tokens = cut(sentence, self.language, self.cut_type, keep_punctuation=keep_punctuation, cut_fn=self.cut_fn)
                tokens = self.do_encode(tokens)
            if padding:
                return self.padding(tokens, max_length, truncation, padding, padding_side, pad_begin_end)
            return tokens

        raise ValueError('参数"sentence"类型错误')

    def batch_encode(self, sentences: Union[Iterable[str], Iterable[Iterable]], max_length: int = None, truncation=True,
                     padding=True, padding_side='right', pad_begin_end=False, keep_punctuation=False,
                     is_split_into_words: bool = False):
        """
        :param sentences: ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
        :param max_length:
        :param truncation:
        :param padding:
        :param padding_side:
        :param pad_begin_end:
        :param keep_punctuation: 是否保留标点符号
        :param is_split_into_words: 是否已经分词
        :return:
        """
        if isinstance(sentences, Iterable):
            if is_split_into_words:
                tokens = map(self.do_encode, sentences)
            else:
                batch_cuts = batch_cut(sentences, language=self.language, cut_type=self.cut_type,
                                       keep_punctuation=keep_punctuation, cut_fn=self.cut_fn)
                tokens = map(self.do_encode, batch_cuts)
            if padding:
                return self.padding(tokens, max_length, truncation, padding, padding_side, pad_begin_end)
            return list(tokens)

        raise ValueError('参数"sentence"类型错误')

    def do_encode(self, cut_tokens: Union[str, Iterable[str]]):
        """
        把词转换成数字
        :param cut_tokens: '学生' 或 ['学生', '手机', '老师']
        :return:
        """
        if self.stop_words:
            if isinstance(cut_tokens, str):
                return self._do_encode_stop_words(cut_tokens)
            return list(filter(lambda x: x is not None, map(self._do_encode_stop_words, cut_tokens)))
            
        if isinstance(cut_tokens, str):
            return self._do_encode(cut_tokens)
        return list(filter(lambda x: x is not None, map(self._do_encode, cut_tokens)))
    
    def _do_encode(self, cut_token: str):
        return self.token_to_idx.get(cut_token, self.unk)
    
    def _do_encode_stop_words(self, cut_token: str):
        return self.token_to_idx.get(cut_token, self.unk) if cut_token not in self.stop_words else None

    def decode(self, ids: Iterable[int], return_special_tokens=False, return_sentence=False):
        """
        :param ids: [2, 19, 27, 3, 0, 0]
        :param return_special_tokens: 是否返回'<pad>', '<unk>', '<bos>', '<eos>'等特殊字符
        :param return_sentence: 返回的是一句话还是词序列
        :return: 由return_sentence决定，返回的是 '上课时学生手机响个不停‘, 还是 ['上课', '时', '学生', '手机', ’响个, '不停']
        """
        return [self.decode(index, return_special_tokens, return_sentence) for index in ids]

    def batch_decode(self, ids: Iterable[Iterable[int]], return_special_tokens=False, return_sentence=False):
        """
        :param ids: [[2, 19, 27, 3, 0, 0], [2, 10, 3, 0, 0, 0]]
        :param return_special_tokens: 是否返回'<pad>', '<unk>', '<bos>', '<eos>'等特殊字符
        :param return_sentence: 返回的是一句话还是词序列
        :return: 由return_sentence决定，返回的是 '上课时学生手机响个不停‘, 还是 ['上课', '时', '学生', '手机', ’响个, '不停']
        """
        return [self.decode(index, return_special_tokens, return_sentence) for index in ids]

    def padding(self, tokens: Union[map, Iterable[int], Iterable[Iterable[int]]], max_length: int, truncation=True,
                padding=True, padding_side='right', pad_begin_end=False):
        """
        :param tokens: [2, 19, 27, 3] 或 [[2, 19, 27, 3], [2, 10, 3]]
        :param max_length:
        :param truncation:
        :param padding:
        :param padding_side:
        :param pad_begin_end:
        :return:
        """
        if isinstance(tokens, map) or isinstance(tokens[0], Iterable):
            return batch_pad(tokens, max_length, truncation, padding, padding_side, pad_begin_end, self.pad, self.bos, self.eos)
        return pad(tokens, max_length, truncation, padding, padding_side, pad_begin_end, self.pad, self.bos, self.eos)
    
    def add_special_tokens(self, special_tokens: Collection[str]):
        for token in special_tokens:
            if token in self.special_tokens or token in self.vocab:
                continue
            self.special_tokens.append(token)
            self.token_to_idx[token] = len(self.vocab)
            self.vocab.append(token)
            
    def add_stop_words(self, stop_words: Collection[str]):
        if not stop_words:
            return
        
        if self.stop_words is None:
            self.stop_words = stop_words if isinstance(self.stop_words, List) else list(stop_words)
            for word in stop_words:
                if word in self.vocab:
                    self.vocab.remove(word)
        else:
            if not isinstance(self.stop_words, List):
                self.stop_words = list(self.stop_words)
                
            for word in stop_words:
                if word in self.stop_words:
                    continue
                self.stop_words.append(word)
                if word in self.vocab:
                    self.vocab.remove(word)
                
        self.vocab_size = len(self.vocab)
        self.token_to_idx = {k: i for i, k in enumerate(self.vocab)}

    def get_real_vocab(self):
        """
        :return: 除去特殊字符的词表
        """
        special_token_len = len(self.special_tokens)
        idx = special_token_len - 1
        if self.special_tokens[idx] == self.vocab[idx]:
            return self.vocab[len(self.special_tokens):]
        
        for i in range(idx):
            if self.special_tokens[i] != self.vocab[i]:
                idx = i
                break
        return self.vocab[idx:len(self.vocab) + idx - special_token_len]

    def save(self, path='vocab.txt', encoding=UTF8):
        with open(path, 'w', encoding=encoding) as f:
            f.write(self.SAVE_SEP.join([self.language, self.cut_type]) + '\n')
            f.write(self.SAVE_SEP.join(self.special_tokens) + '\n')
            if self.stop_words:
                f.write(self.SAVE_SEP.join(self.stop_words) + '\n')
            else:
                f.write('\n')
            f.write('\n'.join(self.vocab))

    @classmethod
    def load(cls, path='vocab.txt', encoding=UTF8, cut_fn=None):
        with open(path, encoding=encoding) as f:
            lines = f.readlines()
        language, cut_type = lines[0].strip().split(Tokenizer.SAVE_SEP)
        special_tokens = lines[1].strip().split(Tokenizer.SAVE_SEP)
        stop_words = lines[2].strip()
        stop_words = stop_words.split(Tokenizer.SAVE_SEP) if stop_words else None
        return cls(vocab=[word.strip() for word in lines[3:]], special_tokens=special_tokens, language=language,
                   cut_type=cut_type, stop_words=stop_words, cut_fn=cut_fn)

    @classmethod
    def from_file(cls, file: str, encoding=UTF8, pattern='*', func=read_file, min_freq=0,
                  special_tokens: Collection[str] = None, language='cn', cut_type='word', word_freq=False,
                  stop_words: Collection[str] = None,cut_fn=None):
        """
        :param file: 语料文件，可以是文件也可以是文件夹， 如：'./train.txt'. 如果是文件夹，会读取文件夹下的所有目录和文件.
        :param encoding: 编码
        :param pattern: 文件后缀，当file是文件夹的时候，会根据此后缀过滤文件
        :param func: 具体读取文件的处理函数，默认是read_file，可替换。注意：其函数签名为 function_name(path: str, encoding: str) -> corpus: Iterable[str]
        :param min_freq: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
        :param special_tokens: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        :param word_freq: 是否统计词频
        :param stop_words: 停用词
        :param cut_fn
        """
        corpus = read_corpus_files(file, encoding, pattern, func)
        return cls(corpus=corpus, min_freq=min_freq, special_tokens=special_tokens, language=language,
                   cut_type=cut_type, word_freq=word_freq, stop_words=stop_words, cut_fn=cut_fn)

    @classmethod
    def from_corpus(cls, corpus: Iterable[str], min_freq=0, special_tokens: Collection[str] = None, language='cn',
                    cut_type='word', word_freq=False, stop_words: Collection[str] = None,cut_fn=None):
        """
        :param corpus: 语料，每个元素是一句话，如：['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
        :param min_freq: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
        :param special_tokens: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        :param word_freq: 是否统计词频
        :param stop_words: 停用词
        :param cut_fn
        """
        return cls(corpus=corpus, min_freq=min_freq, special_tokens=special_tokens, language=language,
                   cut_type=cut_type, word_freq=word_freq, stop_words=stop_words, cut_fn=cut_fn)

    @classmethod
    def from_cut_corpus(cls, cut_corpus: Iterable[Iterable[str]], min_freq=0, special_tokens: Collection[str] = None,
                        language='cn', cut_type='word', word_freq=False, stop_words: Collection[str] = None, cut_fn=None):
        """
        :param cut_corpus: 分词后的语料，每个元素是一句话，如：[['上课', '时', '学生', '手机', '响', '个', '不停'], ['家长', '拿', '发票', '让', '老师', '赔']]
        :param min_freq: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
        :param special_tokens: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        :param word_freq: 是否统计词频
        :param stop_words: 停用词
        :param cut_fn
        """
        return cls(cut_corpus=cut_corpus, min_freq=min_freq, special_tokens=special_tokens, language=language,
                   cut_type=cut_type, word_freq=word_freq, stop_words=stop_words, cut_fn=cut_fn)

    @classmethod
    def from_vocab(cls, vocab: Iterable[str], special_tokens: Collection[str] = None,
                   stop_words: Collection[str] = None, cut_fn=None):
        """
        :param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
        :param special_tokens: 保留token, 如 '<pad>', '<unk>'等
        :param stop_words: 停用词
        :param cut_fn
        """
        return cls(vocab=vocab, special_tokens=special_tokens, stop_words=stop_words, cut_fn=cut_fn)

    def _get_token(self, indices: Iterable[int], return_special_tokens):
        if return_special_tokens:
            return [self.vocab[i] for i in indices]
        return [self.vocab[i] for i in indices if i not in [self.pad, self.bos, self.eos, self.unk]]

    def __len__(self):
        return self.vocab_size

    def __getitem__(self, index):
        return self.vocab[index]

    # def __call__(self, sentence: Union[str, Iterable[str]], max_length: int = None, truncation=True, padding=True, padding_side='right',
    #         pad_begin_end=False, keep_punctuation=False):
    #     return self.encode(sentence, max_length, truncation, padding, padding_side, pad_begin_end, keep_punctuation)


class Tokenizer(BaseTokenizer):
    """
    encode返回的是 {'input_ids': list} 或 {'input_ids': list, 'mask_ids': list}
    """

    def __init__(self, file: str = None, corpus: Iterable[str] = None, cut_corpus: Iterable[Iterable[str]] = None,
                 vocab: Iterable[str] = None, min_freq=10, special_tokens: Collection[str] = None, language: str = 'cn',
                 cut_type: str = 'word', word_freq: bool = False, stop_words: Collection[str] = None, cut_fn=None):
        """
        :param file: 语料文件， 如：'./train.csv'
        :param corpus: 语料，每个元素是一句话，如：['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ...]
        :param cut_corpus: 语料，每个元素是是分词后的一句话，如：[['上课', '时', '学生', '手机', '响', '个', '不停'], ['家长', '拿', '发票', '让', '老师', '赔']]
        :param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
        :param min_freq: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
        :param special_tokens: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        :param word_freq: 是否统计词频
        :param stop_words: 停用词
        :param cut_fn
        """
        super().__init__(file=file, corpus=corpus, cut_corpus=cut_corpus, vocab=vocab, min_freq=min_freq,
                         special_tokens=special_tokens,language=language, cut_type=cut_type,
                         word_freq=word_freq, stop_words=stop_words, cut_fn=cut_fn)

    def encode_plus(self, sentence: Union[str, Iterable[str], Iterable[Iterable]], max_length: int = None, truncation=True, padding=True, padding_side='right',
            pad_begin_end=False, keep_punctuation=False, return_mask=False, is_split_into_words=False):
        """
        :param sentence: '上课时学生手机响个不停，老师一怒之下把手机摔了' 或 ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
        :param max_length:
        :param truncation:
        :param padding:
        :param padding_side:
        :param pad_begin_end:
        :param keep_punctuation: 是否保留标点符号
        :param return_mask: 是否返回 mask_ids
        :param is_split_into_words: 是否已经分词
        :return:
        """
        if isinstance(sentence, str):
            if is_split_into_words:
                tokens = self.do_encode(sentence)
            else:
                tokens = cut(sentence, self.language, self.cut_type, keep_punctuation=keep_punctuation, cut_fn=self.cut_fn)
                tokens = self.do_encode(tokens)
            return self.padding_plus(tokens, max_length, truncation, padding, padding_side, pad_begin_end, return_mask)

        raise ValueError('参数"sentence"类型错误')

    def batch_encode_plus(self, sentences: Union[str, Iterable[str], Iterable[Iterable]], max_length: int = None, truncation=True, padding=True, padding_side='right',
            pad_begin_end=False, keep_punctuation=False, return_mask=False, is_split_into_words=False):
        """
        :param sentences: ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
        :param max_length:
        :param truncation:
        :param padding:
        :param padding_side:
        :param pad_begin_end:
        :param keep_punctuation: 是否保留标点符号
        :param return_mask: 是否返回 mask_ids
        :param is_split_into_words: 是否已经分词
        :return:
        """
        if isinstance(sentences, Iterable):
            if is_split_into_words:
                tokens = map(self.do_encode, sentences)
            else:
                batch_cuts = batch_cut(sentences, language=self.language, cut_type=self.cut_type,
                                       keep_punctuation=keep_punctuation, cut_fn=self.cut_fn)
                tokens = map(self.do_encode, batch_cuts)
            return self.padding_plus(tokens, max_length, truncation, padding, padding_side, pad_begin_end, return_mask)

        raise ValueError('参数"sentence"类型错误')

    def padding_plus(self, tokens: Union[map, Iterable[int], Iterable[Iterable[int]]], max_length: int, truncation=True, padding=True,
            padding_side='right', pad_begin_end=False, return_mask=False):
        """
        :param tokens: [2, 19, 27, 3] 或 [[2, 19, 27, 3], [2, 10, 3]]
        :param max_length:
        :param truncation:
        :param padding:
        :param padding_side:
        :param pad_begin_end:
        :return:
        """
        if isinstance(tokens, map) or isinstance(tokens[0], Iterable):
            if return_mask:
                return batch_pad_mask(tokens, max_length, truncation, padding, padding_side, pad_begin_end, self.pad, self.bos, self.eos)
            return {'input_ids': batch_pad(tokens, max_length, truncation, padding, padding_side, pad_begin_end, self.pad, self.bos, self.eos)}

        if return_mask:
            return pad_mask(tokens, max_length, truncation, padding, padding_side, pad_begin_end, self.pad, self.bos, self.eos)
        return {'input_ids': pad(tokens, max_length, truncation, padding, padding_side, pad_begin_end, self.pad, self.bos, self.eos)}

    def __call__(self, sentence: Union[str, Iterable[str]], max_length: int = None, truncation=True, padding=True, padding_side='right',
            pad_begin_end=False, keep_punctuation=False, return_mask=False, is_split_into_words=False):
        return self.encode_plus(sentence, max_length, truncation, padding, padding_side, pad_begin_end, keep_punctuation,
                                return_mask, is_split_into_words)


class TokenEmbedding(Tokenizer):
    """
    可以传入已经训练好的embedding文件路径，也可以embedding数据, encode返回的是 {'input_ids': list} 或 {'input_ids': list, 'mask_ids': list}
    """

    def __init__(self, file: str = None, vocab: Iterable[str] = None, embedding: Iterable[Iterable[float]] = None, special_tokens=[],
            language='cn', cut_type='word', func=load_embedding, is_large_file=False, cut_fn=None):
        """
        :param file: embedding文件， 如：'./sgns.weibo.word.bz2'
        :param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']，与embedding必须同时传入
        :param embedding: [[0.2548, -0.6879, 0.2578],[0.2548, -0.6879, 0.2578],[0.2548, -0.6879, 0.2578]]与vocab必须同时传入
        :param special_tokens: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        :param func: 具体读取文件的处理函数，load_embedding，可替换。
               注意：其函数签名为 function_name(path: str, is_large_file: bool) -> (vocab: list[str], embedding: list[list[float]])
        :param is_large_file: 是否是大文件
        """
        if file:
            assert Path(file).is_file(), 'file必须是具体文件,不能是文件夹'
            vocab, embedding = func(file, is_large_file)
        elif not vocab or not embedding:
            raise ValueError('参数"path"为空的情况下，"vocab"和"embedding"不能为空.')
        super().__init__(vocab=vocab, special_tokens=special_tokens, language=language, cut_type=cut_type, cut_fn=cut_fn)
        special_tokens = self.special_tokens.copy()
        special_tokens.reverse()
        self.embed_dim = len(embedding[0])
        for token in special_tokens:
            embedding = [[self.do_encode(token)] * self.embed_dim] + embedding
        self.embedding = Embedding.from_pretrained(torch.tensor(embedding, dtype=torch.float))
        del embedding
        gc.collect()

    def __call__(self, sentence: Union[str, Iterable[str], Iterable[Iterable]], max_length: int = None, truncation=True,
                 padding=True, padding_side='right', pad_begin_end=False, keep_punctuation=False,
                 is_split_into_words: bool = False):
        input_ids = self.batch_encode(sentence, max_length, truncation, padding, padding_side, pad_begin_end,
                                      keep_punctuation, is_split_into_words)
        return self.embedding(torch.tensor(input_ids, dtype=torch.long))

    @classmethod
    def from_file(cls, file: str, func=load_embedding, is_large_file=False, special_tokens=[], language='cn', cut_type='word', cut_fn=None):
        """
        :param file: embedding文件， 如：'./sgns.weibo.word.bz2'. 注意：必须是单一文件，不能是文件夹。
        :param func: 具体读取文件的处理函数，load_embedding，可替换。注意：其函数签名为 function_name(path: str, is_large_file: bool) -> [vocab], [[embedding]]
        :param is_large_file: 是否是大文件
        :param special_tokens: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        :param cut_fn
        """
        return cls(file=file, special_tokens=special_tokens, language=language, cut_type=cut_type, func=func, is_large_file=is_large_file, cut_fn=cut_fn)

    @classmethod
    def from_vocab_embedding(cls, vocab: Iterable[str], embedding: Iterable[Iterable[float]], large_file=False, special_tokens=[], language='cn',
            cut_type='word', cut_fn=None):
        """
        :param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
        :param embedding: [[0.2548, -0.6879, 0.2578],[0.2548, -0.6879, 0.2578],[0.2548, -0.6879, 0.2578]]
        :param large_file: 是否是大文件
        :param special_tokens: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        :param cut_fn
        """
        return cls(vocab=vocab, embedding=embedding, large_file=large_file, special_tokens=special_tokens,
                   language=language, cut_type=cut_type, cut_fn=cut_fn)

    @classmethod
    def load(cls, path='vocab.txt', encoding=UTF8, cut_fn=None):
        raise NotImplementedError("Please use Tokenizer instead.")


# if __name__ == '__main__':
    # file_name = './article.txt'
    # text = read_file(file_name)

    import pandas as pd
    import matplotlib.pyplot as plt

    # DATA_PATH = r'D:\Study\kkb\代码实战课\week1\toutiao-text-classify\dataset\train.csv'
    # df = pd.read_csv(DATA_PATH)  # ['label']  ['sentence']

    # show_label_category_count(df['label'])
    # show_sentence_len_hist(df['sentence'], language='cn', cut_type='word', bins=50, scope=(0, 30))
    # show_token_freq_plot(df['sentence'], language='cn', cut_type='word', scope=(0, 8000))

    # tokenizer = Tokenizer(corpus=df['sentence'].values, min_freq=10, language='cn', cut_type='word')
    # tokenizer = BaseTokenizer.from_corpus(df['sentence'].values)
    # tokenizer.save()

    # sent = ('上课时学生手机响个不停，老师一怒之下把手机摔了，家长拿发票让老师赔，大家怎么看待这种事？', '老师一怒之下把手机摔了')
    # tokenizer = BaseTokenizer.load()
    # d = tokenizer.encode(sent, max_length=30, keep_punctuation=True, pad_begin_end=True)
    # print(d)
    # print(tokenizer.decode(d, return_special_tokens=False, return_sentence=True))
    # tokenizer = Tokenizer.load()
    # # print(type(tokenizer))
    # # # print(len(tokenizer))
    # # # print(tokenizer.vocab[:20])
    # # # print(tokenizer.special_tokens)
    # # # print(tokenizer.encode(['the', 'my']))
    # #
    # print(tokenizer.vocab[:20])
    # print(sent)
    # e = tokenizer(sent, max_length=30, keep_punctuation=True, pad_begin_end=True)
    # print(e)
    # d = tokenizer.decode(e)
    # print(d)

    # print(tokenizer.decode(d['input_ids'], return_special_tokens=False, return_sentence=True))
    # print(tokenizer.decode(d['input_ids']))

    # tk = [[101, 2198, 5125, 3198, 7313, 4764, 3221, 4507, 102, 7313, 4764, 3221, 4507, 102, 4764, 3221],
    #       [101, 2198, 5125, 3198, 7313, 4764, 3221, 4507, 102]]
    # r = tokenizer.padding(tk, max_length=15, truncation=True, padding_side='right', pad_begin_end=True)
    # print(r)

    # PATH = r'D:\Study\kkb\代码实战课\week1\toutiao-text-classify\dataset\sgns.weibo.word.bz2'
    # tokenizer = TokenEmbedding(PATH)
    # tokenizer = TokenEmbedding.from_file(PATH, is_large_file=False)
    # d = tokenizer.encode(sent, max_length=30, keep_punctuation=True, pad_begin_end=True)
    # print(d)
    # print(tokenizer.decode(d['input_ids'], return_special_tokens=False, return_sentence=True))
    # print(tokenizer.decode(d['input_ids']))
    #
    # tk = [[101, 2198, 5125, 3198, 7313, 4764, 3221, 4507, 102, 7313, 4764, 3221, 4507, 102, 4764, 3221],
    #       [101, 2198, 5125, 3198, 7313, 4764, 3221, 4507, 102]]
    # r = tokenizer.padding(tk, max_length=15, truncation=True, padding_side='right', pad_begin_end=True)
    # print(r)

    # print(batch_pad_mask(tk))

    # tokenizer = BaseTokenizer.from_file('./', pattern='*.txt', language='en')
    # print(tokenizer.vocab)

    # for f in get_files(r'D:\tmp'):
    #     print(f)

    # for line in read_large_file('./article.txt'):
    #     print(line)

