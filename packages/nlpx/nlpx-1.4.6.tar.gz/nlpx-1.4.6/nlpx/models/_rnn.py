import torch
from torch import nn


class RNNLayer(nn.Module):
	"""
	Examples
	--------
	>>> from nlpx.text_token import Tokenizer
	>>> from nlpx.models import RNNAttention
	>>> tokenizer = Tokenizer(corpus)
	>>> classifier = RNNLayer(embed_dim)
	"""
	
	def __init__(self, embed_dim: int, hidden_size: int = 64, num_layers: int = 1, rnn=nn.GRU, drop_out: float = 0.0,
	             batch_norm=False):
		"""
		:param embed_dim: RNN的input_size，word embedding维度
		:param hidden_size: RNN的hidden_size, RNN隐藏层维度
		:param num_layers: RNN的num_layers, RNN层数
		:param num_layers: RNN的num_layers, RNN层数
		:param rnn: 所用的RNN模型：GRU和LSTM，默认是GRU
		:param drop_out：
		:param batch_norm：是否批正则化
		"""
		
		super().__init__()
		self.batch_norm = batch_norm
		self.rnn = rnn(input_size=embed_dim, hidden_size=hidden_size, num_layers=num_layers, bidirectional=True,
		               batch_first=True, dropout=drop_out)
		if batch_norm:
			self.norm = nn.BatchNorm1d(num_features=(hidden_size << 1))
			
	def forward(self, inputs: torch.Tensor):
		"""
		:param inputs: [(batch_size, sequence_length, embed_dim)]
		:return: [(batch_size, sequence_length, 2 * hidden_size)]
		"""
		output, _ = self.rnn(inputs)  # [(batch_size, sequence_length, 2 * hidden_size)]
		if self.batch_norm:
			output = self.norm(output.transpose(2, 1)).transpose(2, 1)
		return output
