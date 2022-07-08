from pathlib import Path
import pandas as pd
import plotly.express as px


WD = Path(__file__).parent


def read_csv(file: Path) -> pd.DataFrame:
    df = pd.read_csv(file, header=1, usecols=[0, 1])
    df["model"] = file.stem[:-4]
    return df


files = list(WD.rglob("*hrr.csv"))
df = pd.concat([read_csv(f) for f in files])
fig = px.line(
    df,
    x="Time",
    y="HRR",
    color="model",
    line_dash="model",
    category_orders={
        "model": [
            "hrrpua_500_hrr",
            "hrrpua_1000_hrr",
            "hrrpua_1500_hrr",
        ]
    },
)
fig.write_image(WD / "hrr.png")
