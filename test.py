import pandas as pd

data = {"Name": ["Nguyen Gia Huy", "Phan Gia Thanh"], "Score": [7.7, 6.3]}
df = pd.DataFrame(data)

min_diff = float('inf')
min_name = None
for name, score in df[['Name', 'Score']].values:
    diff = abs(score - 6.2)
    if diff < min_diff:
        min_diff = diff
        min_name = name

print(min_name)
