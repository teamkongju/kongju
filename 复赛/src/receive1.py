from flask import Flask, request, jsonify
import torch
import logging
import requests
from utils import IsQuestion
from config import get_arguments
from classify import classify_single_issue


isQ = IsQuestion()

app = Flask(__name__)
app.config['DEBUG'] = True
logging.basicConfig(level=logging.DEBUG)
@app.route('/predict', methods=['POST'])
def predict():
    #app.logger.info(f'Received request data: {request.json}')
    data = request.json
    issue_title = data['issue']['title']
    issue_body = data['issue']['body']
    issue_number = data['issue']['number']
    issue_author_association = data['issue']['author_association']
    # 获取模型参数
    args, logging_args= get_arguments()
    args.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    #置信度阈值
    confidence_threshold = 0.6

    # 分类单个 issue
    label, confidence = classify_single_issue(issue_title, issue_body, issue_number, 
                                              issue_author_association, args, confidence_threshold)
    
    #打标签
    if label != "Uncertain" and confidence >= confidence_threshold:
        labels_url = data['issue']['labels_url'].replace("{/name}", "")
        headers = { 
            "Authorization": f"token YOUR_AUTHOR_TOKEN", 
            "Content-Type": "application/json" 
        }
        label_payload = {"labels": [label]}
        requests.post(labels_url, headers=headers, json=label_payload)
    else:
        app.logger.info('Uncertain result!')

    return jsonify({
        'predicted_label': label,
        'confidence': confidence
    })

if __name__ == '__main__':
    app.run(debug=True)
