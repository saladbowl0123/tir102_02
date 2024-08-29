from google.cloud import bigquery
from google.cloud.bigquery import SchemaField, SourceFormat

tables_schema = {
    "APoD": [
        bigquery.SchemaField("date", "DATE", mode="NULLABLE", description="日期"),
        bigquery.SchemaField("media_type", "STRING", mode="NULLABLE", description="媒體類型"),
        bigquery.SchemaField("title", "STRING", mode="NULLABLE", description="標題"),
        bigquery.SchemaField("URL", "STRING", mode="NULLABLE", description="網址"),
        bigquery.SchemaField("copyright", "STRING", mode="NULLABLE", description="版權信息"),
    ],
    "Constellations": [
        bigquery.SchemaField("ConstellationID", "INTEGER", mode="REQUIRED", description="星座ID"),
        bigquery.SchemaField("ConstellationName", "STRING", mode="NULLABLE", description="星座名稱"),
        bigquery.SchemaField("MainStarName", "STRING", mode="NULLABLE", description="主星名稱"),
        bigquery.SchemaField("StartDate", "DATETIME", mode="NULLABLE", description="開始日期"),
        bigquery.SchemaField("EndDate", "DATETIME", mode="NULLABLE", description="結束日期"),
    ],
    "Planet": [
        bigquery.SchemaField("Planet_ID", "INTEGER", mode="REQUIRED", description="行星ID"),
        bigquery.SchemaField("NAME", "STRING", mode="REQUIRED", description="行星名稱"),
        bigquery.SchemaField("MASS", "FLOAT", mode="NULLABLE", description="質量"),
        bigquery.SchemaField("DIAMETER", "INTEGER", mode="NULLABLE", description="直徑"),
        bigquery.SchemaField("DENSITY", "INTEGER", mode="NULLABLE", description="密度"),
        bigquery.SchemaField("GRAVITY", "FLOAT", mode="NULLABLE", description="重力"),
        bigquery.SchemaField("Escape_Vel", "FLOAT", mode="NULLABLE", description="逃逸速度"),
        bigquery.SchemaField("Rotation_Period", "FLOAT", mode="NULLABLE", description="自轉周期"),
        bigquery.SchemaField("Length_of_Day", "FLOAT", mode="NULLABLE", description="日長"),
        bigquery.SchemaField("Distance_from_Sun", "FLOAT", mode="NULLABLE", description="距離太陽"),
        bigquery.SchemaField("PERIHELION", "FLOAT", mode="NULLABLE", description="近日點"),
        bigquery.SchemaField("Orbital_Period", "FLOAT", mode="NULLABLE", description="公轉周期"),
        bigquery.SchemaField("Orbital_Velocity", "FLOAT", mode="NULLABLE", description="公轉速度"),
        bigquery.SchemaField("Orbital_Inclination", "FLOAT", mode="NULLABLE", description="公轉傾角"),
        bigquery.SchemaField("Orbital_Eccentricity", "FLOAT", mode="NULLABLE", description="公轉偏心率"),
        bigquery.SchemaField("Obliquity_to_Orbit", "FLOAT", mode="NULLABLE", description="軌道傾角"),
        bigquery.SchemaField("Mean_Temperature", "INTEGER", mode="NULLABLE", description="平均溫度"),
        bigquery.SchemaField("Surface_Pressure", "FLOAT", mode="NULLABLE", description="表面壓力"),
        bigquery.SchemaField("Number_of_Moons", "INTEGER", mode="NULLABLE", description="衛星數量"),
        bigquery.SchemaField("Ring_System", "BOOLEAN", mode="NULLABLE", description="是否有環系統"),
        bigquery.SchemaField("Global_Magnetic_Field", "BOOLEAN", mode="NULLABLE", description="是否有全球磁場"),
    ],
    "Satellite": [
        bigquery.SchemaField("Satellite_ID", "STRING", mode="REQUIRED", description="衛星ID"), 
        bigquery.SchemaField("NAME", "STRING", mode="NULLABLE", description="衛星名稱"),
        bigquery.SchemaField("Satellite_of", "INTEGER", mode="NULLABLE", description="行星ID"),
        bigquery.SchemaField("Orbital_Speed", "FLOAT", mode="NULLABLE", description="軌道速度"),
        bigquery.SchemaField("Period", "FLOAT", mode="NULLABLE", description="軌道周期"),
        bigquery.SchemaField("Orbital_Radius", "FLOAT", mode="NULLABLE", description="軌道半徑"),
    ],
    "Shower2024": [
        bigquery.SchemaField("Shower_ID", "STRING", mode="REQUIRED", description="流星雨ID"),  
        bigquery.SchemaField("NAME", "STRING", mode="NULLABLE", description="流星雨名稱"),
        bigquery.SchemaField("Start_Date", "DATETIME", mode="NULLABLE", description="開始日期"),
        bigquery.SchemaField("End_Date", "DATETIME", mode="NULLABLE", description="結束日期"),
        bigquery.SchemaField("Maximum_Date", "DATETIME", mode="NULLABLE", description="最大日期"),
        bigquery.SchemaField("Solar_Longitude", "FLOAT", mode="NULLABLE", description="太陽經度"),
        bigquery.SchemaField("Right_Ascension", "STRING", mode="NULLABLE", description="赤緯"),
        bigquery.SchemaField("Declination", "FLOAT", mode="NULLABLE", description="赤經"),
        bigquery.SchemaField("Velocity", "FLOAT", mode="NULLABLE", description="速度"),
        bigquery.SchemaField("r_Population_Index", "FLOAT", mode="NULLABLE", description="流星雨人口指數"),
        bigquery.SchemaField("Max_ZHR", "INTEGER", mode="NULLABLE", description="最大ZHR"),
        bigquery.SchemaField("Time_bestseen", "DATETIME", mode="NULLABLE", description="最佳觀賞時間"),
        bigquery.SchemaField("Moon", "INTEGER", mode="NULLABLE", description="月亮影響"),
    ],
    "Comet": [
        bigquery.SchemaField("Comet_ID", "STRING", mode="REQUIRED", description="彗星ID"),  
        bigquery.SchemaField("NAME", "STRING", mode="NULLABLE", description="彗星名稱"),
        bigquery.SchemaField("Orbital_Period", "FLOAT", mode="NULLABLE", description="公轉周期"),
        bigquery.SchemaField("Perihelion_Date", "DATETIME", mode="NULLABLE", description="近日點日期"),
        bigquery.SchemaField("Perihelion_Distance", "FLOAT", mode="NULLABLE", description="近日點距離"),
        bigquery.SchemaField("Semi_Major_Axis", "FLOAT", mode="NULLABLE", description="半長軸"),
        bigquery.SchemaField("Orbital_Eccentricity", "FLOAT", mode="NULLABLE", description="公轉偏心率"),
        bigquery.SchemaField("Orbital_Inclination", "FLOAT", mode="NULLABLE", description="公轉傾角"),
        bigquery.SchemaField("Absolute_Magnitude", "FLOAT", mode="NULLABLE", description="絕對星等"),
    ],
    "tag": [
        bigquery.SchemaField("id", "INTEGER", mode="REQUIRED", description="ID"),
        bigquery.SchemaField("date","DATE", mode="REQUIRED", description="日期"),
        bigquery.SchemaField("tag_en", "STRING", mode="REQUIRED", description="標籤"),
        bigquery.SchemaField("tag_zhTW", "STRING", mode="REQUIRED", description="標籤"),
    ],
    "unit": [
        bigquery.SchemaField("UnitID", "INTEGER", mode="REQUIRED", description="單位ID"),
        bigquery.SchemaField("Unit", "STRING", mode="REQUIRED", description="單位名稱")
    ],
    # "measurement": [
    #     bigquery.SchemaField("MeasurementID", "INTEGER", mode="REQUIRED", description="測量ID"),
    #     bigquery.SchemaField("Value", "FLOAT", mode="REQUIRED", description="測量值"),
    #     bigquery.SchemaField("UnitID", "INTEGER", mode="REQUIRED", description="單位ID")
    # ],
    "conversion_to_meter": [
        bigquery.SchemaField("UnitID", "INTEGER", mode="REQUIRED", description="單位ID"),
        bigquery.SchemaField("MeterConversion", "FLOAT", mode="REQUIRED", description="轉換為公尺的係數")
    ]

}

User_tables_schema = {
    "Users": [
        bigquery.SchemaField("user_id", "INTEGER", mode="REQUIRED", description="用戶唯一ID"),
        bigquery.SchemaField("user_name", "STRING", mode="NULLABLE", description="用戶名稱"),
        bigquery.SchemaField("email", "STRING", mode="NULLABLE", description="用戶電子郵件"),
        bigquery.SchemaField("login_device", "STRING", mode="NULLABLE", description="登陸裝置"),
        bigquery.SchemaField("status_id", "INTEGER", mode="REQUIRED", description="狀態ID"),
        bigquery.SchemaField("group_id", "INTEGER", mode="NULLABLE", description="用戶所屬群組ID")
    ],

    "Status": [
        bigquery.SchemaField("status_id", "INTEGER", mode="REQUIRED", description="狀態ID"),
        bigquery.SchemaField("status_description", "STRING", mode="REQUIRED", description="狀態描述"),
        bigquery.SchemaField("last_updated", "DATETIME", mode="NULLABLE", description="最後更新時間"),
        bigquery.SchemaField("last_updated_by", "INTEGER", mode="NULLABLE", description="最後更新的用戶ID")
    ],

    "UserStatusRecords": [
        bigquery.SchemaField("user_id", "INTEGER", mode="REQUIRED", description="用戶ID"),
        bigquery.SchemaField("status_id", "INTEGER", mode="REQUIRED", description="狀態ID"),
        bigquery.SchemaField("status_update_date", "DATETIME", mode="REQUIRED", description="狀態更新時間")
    ],

    "Groups": [
        bigquery.SchemaField("group_id", "INTEGER", mode="REQUIRED", description="群組ID"),
        bigquery.SchemaField("status_id", "INTEGER", mode="REQUIRED", description="群組狀態ID"),
        bigquery.SchemaField("member_count", "INTEGER", mode="NULLABLE", description="成員數量")
    ],

    "QueryRecords": [
        bigquery.SchemaField("query_record_id", "INTEGER", mode="REQUIRED", description="查詢紀錄唯一ID"),
        bigquery.SchemaField("user_id", "INTEGER", mode="REQUIRED", description="用戶ID"),
        bigquery.SchemaField("group_id", "INTEGER", mode="NULLABLE", description="群組ID"),
        bigquery.SchemaField("query_time", "DATETIME", mode="REQUIRED", description="查詢時間"),
        bigquery.SchemaField("query_content", "STRING", mode="NULLABLE", description="查詢內容")
    ],

    "ResponseMessages": [
        bigquery.SchemaField("response_message_id", "INTEGER", mode="REQUIRED", description="回傳訊息唯一ID"),
        bigquery.SchemaField("query_record_id", "INTEGER", mode="REQUIRED", description="查詢紀錄唯一ID"),
        bigquery.SchemaField("response_time", "DATETIME", mode="REQUIRED", description="回覆時間"),
        bigquery.SchemaField("response_content", "STRING", mode="REQUIRED", description="回覆內容")
    ]
}
