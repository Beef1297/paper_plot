import paper_plot as pplt
from data import Data

d = Data(
    "sample_data.xlsx",
    xaxis="condition1", yaxis="response",
    hue="condition2", col="condition3"
)

fig, ax = pplt.initialize(figsize=(5, 5))

# d.change_xy_axes()
pplt.bar(ax, d, vertical=True)
pplt.arrange_xaxis(ax, d)
pplt.arrange_yaxis(ax, d, tick_interval=1)
pplt.display_process(fig)