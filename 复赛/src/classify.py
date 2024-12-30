import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import ast
from models import BERTClass
from utils import get_benchmarks, process_urls, load, set_random_seed, CustomTextDataset, clean_body, IsQuestion
from config import get_arguments
# 加载模型和 tokenizer
def load_model(args):
    model = BERTClass(args)
    model.to(args.device)
    output_model_name = args.SAVED_MODELS_DIR + args.MODEL_NAME + "_classifier" + args.DATASET_SUFFIX + "_best.bin"
    load(model, output_model_name)
    return model

isQ=IsQuestion()
# 单个 issue 分类函数
def classify_single_issue(issue_title, issue_body, issue_number, issue_author_association,args, confidence_threshold):
    tokenizer = AutoTokenizer.from_pretrained("/root/.cache/huggingface/transformers/roberta-base")
    model = load_model(args)
    model.eval()
    
    # 预处理 issue_text
    issue_text = issue_title + " [B] " + clean_body(issue_body)
    inputs = tokenizer(issue_text, return_tensors="pt", padding='max_length', truncation=True, max_length=args.ISSUE_TEXT_MAX_LEN)
    inputs = {key: val.to(args.device) for key, val in inputs.items()}
    
    # 生成特征
    is_early_issue = 1 if issue_number < args.EARLY_ISSUE_THRESHOLD else 0
    is_opened_owner = 1 if issue_author_association == "OWNER" else 0
    is_question = isQ.predict_question(issue_title)
    
    features = torch.tensor([[is_early_issue, is_opened_owner, is_question]], dtype=torch.long).to(args.device)
    
    # 模型推理
    with torch.no_grad():
        outputs = model(inputs['input_ids'], inputs['attention_mask'], features)
    
    # 获取预测结果
    probabilities = torch.nn.functional.softmax(outputs, dim=-1)
    predicted_class = torch.argmax(probabilities, dim=1).item()
    confidence = probabilities[0][predicted_class].item()

    if confidence < confidence_threshold: 
        return "Uncertain", confidence
    label = args.INV_LABEL_MAP[predicted_class]
    return label, confidence


#测试代码
'''

if __name__ == '__main__':
    args, logging_args = get_arguments()
    set_random_seed(args.seed, is_cuda=torch.cuda.is_available())
    args.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    confidence_threshold = 0.6
    # 示例 issue
    issue_title = "improvement on stability"
    issue_body = "please upload the dataset"
    
    # 分类单个 issue
    label, confidence = classify_single_issue(issue_title, issue_body, args, confidence_threshold)
    print(f"Issue Title: {issue_title}")
    print(f"Predicted Label: {label}")
    print(f"Confidence: {confidence:.2f}")
'''
