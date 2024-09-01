#pip install google-cloud-translate
import pandas as pd
from google_cnl_api import google_cnl_api
from google.cloud import translate_v2 as translate

df = pd.read_json('apod_data_2024-08-24.json')   

print(df)

content_string = df['explanation']
content_string = ' '.join(content_string)

print("-----",content_string,"-----")

tags_list = google_cnl_api(content_string)ss

# # 初始化翻譯客戶端
# translate_client = translate.Client()
# # 翻譯結果列表
# translated_array = []
# # 將每個英文短語翻譯成中文
# for text in tags_list:
#     result = translate_client.translate(text, target_language='zh-TW')
#     translated_array.append(result['translatedText'])