from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from qwen import Qwen

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # 允许所有路由，所有源
import dashscope

dashscope.api_key=""
llm = Qwen()
def ask_model(question):
    response = llm._call(question)
    return response

@app.route('/ask', methods=['POST', 'OPTIONS'])
def ask():
    print(f"Received {request.method} request")  # 打印请求方法
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "POST":
        print(f"Received data: {request.json}")  # 打印接收到的数据
        user_question = request.json['question']
        question = rf'''
        请根据用户提问以及提供的数据生成echarts的图表所需要的x轴数据和y轴数据，例如：{{
          "xAxis":['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          "yAxis":[150, 230, 224, 218, 135, 147, 260],
        }}
        直接生成json结果，不要返回其他内容。


        提供的数据如下：
        data =  [('负面反馈', 110, '2023-07'), ('负面反馈', 34, '2023-08'), ('负面反馈', 31, '2023-09'), ('负面反馈', 31, '2023-10'), ('负面反馈', 24, '2023-11'), ('负面反馈', 16, '2023-12'), ('负面反馈', 1, '2024-01'), ('负面反馈', 1, '2024-04')]
        用户的提问：{user_question}
        '''
      # [('中性反馈'，145),("无效反馈",125),("正面反馈"，1077),("负面反馈"，647)]
        # [('负面反馈', 11, '2023-07'), ('负面反馈', 34, '2023-08'), ('负面反馈', 31, '2023-09'), ('负面反馈', 31, '2023-10'), ('负面反馈', 24, '2023-11'), ('负面反馈', 16, '2023-12'), ('负面反馈', 1, '2024-01'), ('负面反馈', 1, '2024-04')]
        # [('上海', 11, '2023-07'), ('负面反馈', 34, '2023-08'), ('负面反馈', 31, '2023-09'), ('负面反馈', 31, '2023-10'), ('负面反馈', 24, '2023-11'), ('负面反馈', 16, '2023-12'), ('负面反馈', 1, '2024-01'), ('负面反馈', 1, '2024-04')]
        response = ask_model(question)
        return _corsify_actual_response(jsonify(response))
    else:
        raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/')
def home():
    return "Server is running!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5001)  # 允许外部访问
