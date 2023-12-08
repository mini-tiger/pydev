from rouge import Rouge
import decimal
pred = '武汉市长江大桥'
ideal = '武汉长江大桥'

# Rouge()按空格分隔gram，所以要在中文的字和字之间加上空格
pred, ideal = ' '.join(pred), ' '.join(ideal)

# 计算字粒度的rouge-1、rouge-2、rouge-L
rouge = Rouge()
rouge_scores = rouge.get_scores(hyps=pred, refs=ideal,avg=False)
a=rouge_scores[0]["rouge-l"]["f"]
print("rouge-l" in rouge_scores[0])
print(a)
dec = decimal.Decimal(a)
print(dec.quantize(decimal.Decimal('0.00'), rounding=decimal.ROUND_DOWN))

from rouge import Rouge
import jieba

pred = '武汉市长江大桥'
ideal = '武汉长江大桥'

# 采用jieba分词
pred = ' '.join(jieba.cut(pred, HMM=False))
ideal = ' '.join(jieba.cut(ideal, HMM=False))

# 计算词粒度的rouge-1、rouge-2、rouge-L
rouge = Rouge()
rouge_scores = rouge.get_scores(hyps=pred, refs=ideal)
print(rouge_scores)