import torch
from torch import nn
from ._cnn import CNNLayer


class CNNEmbedding(nn.Module):
	
	def __init__(self, embed_dim: int, seq_length: int = 16, out_channels: int = None, kernel_sizes=(2, 3, 4),
	             activation=nn.ReLU(inplace=True), embedding=None, vocab_size: int = None):
		"""
		:param embed_dim: word embedding维度
		:param seq_length: 句子序列长度
		:param out_channels: CNN out_channels
		:param kernel_sizes: size of each CNN kernel
		:param activation: CNN 激活函数
		:param embedding: 输入的embedding，可以是nn.Embedding，torch.Tensor，list
		:param vocab_size: vocab size
		"""
		super().__init__()
		if embedding is None:
			assert vocab_size, 'vocab_size must be ge 0'
			self.embedding = nn.Embedding(vocab_size, embed_dim)
		elif isinstance(embedding, nn.Embedding):
			self.embedding = embedding
		elif isinstance(embedding, torch.Tensor):
			self.embedding = nn.Embedding.from_pretrained(embedding)
		else:
			self.embedding = nn.Embedding.from_pretrained(torch.tensor(embedding, dtype=torch.float))
		
		out_channels = out_channels or embed_dim
		self.cnn = CNNLayer(embed_dim, seq_length, out_channels, kernel_sizes, activation)
	
	def forward(self, input_ids: torch.LongTensor):
		embeddings = self.embedding(input_ids)
		return self.cnn(embeddings)
