import pandas as pd

# 讀取所有 CSV 文件
df1 = pd.read_csv("accident1_info.csv", encoding='utf-8')
df2 = pd.read_csv("accident2_info.csv", encoding='utf-8')
df3 = pd.read_csv("accident3_info.csv", encoding='utf-8')

# 合併 DataFrame
merged_df = pd.concat([df1, df2, df3], ignore_index=True)

# 根據路段和事故類別分组，並計算每個組內的行數
grouped_df1 = merged_df.groupby(
    ['RoadSection', 'Class']).size().reset_index(name='事故數量')
grouped_df2 = merged_df.groupby(
    ['RoadSection', 'Direction']).size().reset_index(name='事故數量')

# 使用 pivot_table 將事故類別作為列，路段作為索引，並填充每個單元格的值為對應事故類型的數量
pivot_table_df1 = grouped_df1.pivot_table(
    index='RoadSection', columns='Class', values='事故數量', fill_value=0, aggfunc='first')
pivot_table_df2 = grouped_df2.pivot_table(
    index='RoadSection', columns='Direction', values='事故數量', fill_value=0, aggfunc='first')

# 將事故數量列添加到新的 DataFrame
pivot_table_df1['事故數量'] = grouped_df1.groupby('RoadSection')['事故數量'].sum()

# 重新排列列的順序，將'事故數量'列移到'路段'列後面
pivot_table_df1 = pivot_table_df1.reindex(
    columns=['事故數量'] + pivot_table_df1.columns[:-1].tolist())

# 合併(加入方向)
merged_pivot_table_df = pd.concat([pivot_table_df1, pivot_table_df2], axis=1)

# 事故數量多到少排列
merged_pivot_table_df = merged_pivot_table_df.sort_values(
    by='事故數量', ascending=False)

result_file_name = 'accident_count.csv'

# 保存結果到新的 CSV 文件
merged_pivot_table_df.to_csv(result_file_name, encoding='utf-8-sig')

print(f"結果已保存到 {result_file_name} 文件中。")
