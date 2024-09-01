#pip install google-cloud-translate
import os
import time
import pandas as pd
from google_cnl_api import google_cnl_api
from google.cloud import translate_v2 as translate

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\T14 Gen 3\Downloads\my-project-tir102-753ec9549127.json"

# df = pd.read_json('apod_data_1995-06-16_1997-12-31.json')   

def entity_to_tags(df):

    # 儲存每次迴圈中創建的 DataFrame 的列表
    dataframes = []

    # for i in range(0, len(df)):
    for i in range(0,len(df)):
        content_string = df.iloc[i]['explanation']
        if content_string == "":
            continue
        else:
            fig_date = df.iloc[i]['date']
            # print("-----",content_string,"-----")
            tags_list = google_cnl_api(content_string)

            # 初始化翻譯客戶端
            translate_client = translate.Client()
            # 翻譯結果列表
            translated_array = []
            # 將英文翻譯成中文
            for text in tags_list:
                max_retries = 3
                delay = 5
                translation_successful = False

                while not translation_successful:
                    try:
                        result = translate_client.translate(text, target_language='zh-TW')
                        # print(result)
                        translated_array.append(result['translatedText'])
                        translation_successful = True  # 成功後跳出循環

                    except Exception as e:
                        max_retries -= 1 # 剩餘的重試次數
                        if max_retries <= 0:
                            translated_array.append(None)
                            break  # 終止重試並處理下個關鍵字
                        else:
                            print(f"連線失敗，重試中... ({max_retries}/{max_retries})")
                            time.sleep(delay)  # 等待後重試
                            


            print("---------------",i," ",fig_date,"------------------")
            # print(len(tags_list))
            # print(len(translated_array))

            # print(len(tags_list))
            # print(len(translated_array))
            df_tags=pd.DataFrame({
                'tags_en' : tags_list,
                'tags_zhTW' : translated_array 
            })

            # 在 DataFrame 最前面插入一個 date 欄位，值為 fig_date
            df_tags.insert(0, 'date', fig_date)
            # print(df_tags)
            dataframes.append(df_tags)

    # 合併所有 DataFrame
    df_combined = pd.concat(dataframes, ignore_index=True)

    print(df_combined)
    return df_combined