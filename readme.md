### Start Fast API
**Please ensure that you define the "cache_dir" path first in src/.env.**
```bash
cd src/
python3 api_hf.py
```

### Start Docker
**Please ensure that you define the "your_model_path" first in run.sh**
```
bash run.sh
```

### visualglm 多gpu推理遇到的runtime error：
```
forward
    inputs_embeds = torch.cat([pre_txt_emb, image_embeds, post_txt_emb], dim=1)
RuntimeError: Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cuda:2! (when checking argument for argument tensors in method wrapper_CUDA_cat)
```
#### 暫時的解決方式：
##### 方法1
1. 開啟錯誤的cache路徑檔案
```
nano /root/.cache/huggingface/modules/transformers_modules/THUDM/visualglm-6b/f4f759acde0926fefcd35e2c626e08adb452eff8/modeling_chatglm.py
```
2. 修改forward方法，在torch.cat(...) 前面插入以下code，讓不同的emb指定到同一個device
```
pre_txt_emb = pre_txt_emb.to('cuda:0')
image_embeds = image_embeds.to('cuda:0')
post_txt_emb = post_txt_emb.to('cuda:0')
```
##### 方法2
1. 使用前一方法修改並存起來，docker執行時把錯誤的cache覆蓋過去。
```
COPY modeling_chatglm.py /root/.cache/huggingface/modules/transformers_modules/THUDM/visualglm-6b/f4f759acde0926fefcd35e2c626e08adb452eff8/modeling_chatglm.py
```

## Request
### Curl
1. Local image
``` bash
echo -n "{\"image\":\"$(base64 path/to/example.jpg)\",\"text\":\"描述这张图片\",\"history\":[]}" | curl -X POST -H "Content-Type: application/json" -d @- http://127.0.0.1:8080
```

2. URL
```bash
echo -n "{\"image\":\"https://img2.momoshop.com.tw/goodsimg/0010/719/337/10719337_O.jpg?t=1676624006\",\"text\":\"描述这张图片\",\"history\":[]}" | curl -X POST -H "Content-Type: application/json" -d @- http://127.0.0.1:8080
```

### Response
```
{
"result":"这张照片展示了一个人在体育馆里做倒立动作。他似乎正在体操或竞技项目中表演这项技巧，周围有其他运动员和观众观看。背景中有一个篮球架，这表明这可能是一个运动场馆。照片中还有一瓶水和一张椅子，表明这个人可能正在进行某种体育项目的训练或比赛。",
"history":[('描述这张图片','这张照片展示了一个人在体育馆里做倒立动作。他似乎正在体操或竞技项目中表演这项技巧，周围有其他运动员和观众观看。背景中有一个篮球架，这表明这可能是一个运动场馆。照片中还有一瓶水和一张椅子，表明这个人可能正在进行某种体育项目的训练或比赛。')],
"status":200,
"time":"2023-07-03 10:20:43"
}
```
#   v i s u a l G L M 
 
 
