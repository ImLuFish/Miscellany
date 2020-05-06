import pandas as pd

l = pd.date_range("2019-1-1", "2019-12-31", freq="D")
df = pd.DataFrame({"date": l.array})
df["year"] = df["date"].apply(lambda x: x.year)
df["month"] = df["date"].apply(lambda x: x.month)
df["day"] = df["date"].apply(lambda x: x.day)