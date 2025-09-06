import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/spurs_2023_2024_matchlog.csv")
print(df[["date", "round"]].head())

df_clean = df.dropna(subset=["result"])

x = df_clean["passes_progressive_distance"]
y = df_clean["carries_progressive_distance"]

result_colors = {"W": "green", "D": "orange", "L": "red"}
colors = df_clean["result"].map(result_colors)

plt.scatter(x, y, c=colors)

plt.xlabel("Progressive Passes Distance")
plt.ylabel("Progressive Carries Distance")
plt.title("Progressive Passes vs Carries Distance by Match Result")

min_val = min(x.min(), y.min())
max_val = max(x.max(), y.max())

plt.xlim(min_val, max_val)
plt.ylim(min_val, max_val)

plt.savefig("result/passvscarry.png")
plt.show()
