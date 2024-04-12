import random

from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
async def get_qa():
    try:
        with open("data.csv", "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                raise HTTPException(status_code=404, detail="No QA pairs found.")
            line = lines[random.randint(0, len(lines)-1)].strip()
            qa = line.split(",")
            if len(qa) < 2:
                raise HTTPException(status_code=500, detail="QA format error.")

            str_1 = f"""
你是一个微信群聊机器人，你的工作是通过知识库的题目，让大家作答，活跃群氛围。

你会随机从知识库中的QA中出题包括选项等知识，等待用户作答

以下是你的工作流：
第一轮输出："科技猫猫出题，谁来答？"
等待用户回应

第二轮输出："{qa[0]}"
等待用户回应

第三轮输出：
你会根据知识库中的答案:"{qa[1]}"，进行判断，用户的回答是否正确

用户答对回复："恭喜你！答对了！"
用户答错回复："答错了，你还有{{N}}次机会"

N=3   
            """
            return str_1
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
