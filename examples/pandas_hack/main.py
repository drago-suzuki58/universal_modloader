import time

import numpy as np
import pandas as pd


def complicated_math(row):
    # Heavy computation simulation
    time.sleep(0.01)
    return row["A"] * row["B"] + np.log(row["C"] + 1)


def process_data():
    print("Loading data...")
    column_index = pd.Index(["A", "B", "C"])
    df = pd.DataFrame(
        np.random.randint(0, 100, size=(500, 3)),
        columns=column_index,
    )

    print("Starting heavy processing...")
    df["D"] = df.apply(complicated_math, axis=1)

    print("Saving data...")
    df.to_csv("output.csv", index=False)
    print("Done.")


if __name__ == "__main__":
    process_data()
