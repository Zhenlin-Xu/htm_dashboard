import pandas as pd
import plotly
import plotly.express as px

SPEED_LIMIT = 15

data = plotly.data.gapminder()

speed = pd.read_csv("./dataset/switch_speed_data.csv", )
overspeed = speed[speed["speed"] > SPEED_LIMIT]
straight_overspeed = overspeed[overspeed["is_straight"] == True]
turning_overspeed = overspeed[overspeed["is_straight"] == False]
assert len(overspeed) == len(straight_overspeed) + len(turning_overspeed)

# Overview
# top-right corner: histogram
number_records_per_speed = speed[
	["line", "speed", "is_straight", "month",]
].groupby(["is_straight", "speed"]).count()
number_records_per_speed = number_records_per_speed.reset_index()
number_records_per_speed.set_index("speed", inplace=True)

# bottom-right corner: top-N table
# straight position overspeeding
number_straight_overspeed_records_per_switch = straight_overspeed[
	["switch_number", "line"]
].groupby("switch_number").count()
number_straight_overspeed_records_per_switch.sort_values(
	by="line", ascending=False, inplace=True)
number_straight_overspeed_records_per_switch.reset_index(inplace=True)
number_straight_overspeed_records_per_switch.columns = [
	"switch number (straight)", "count (straight)"
]
# turning position overspeeding
number_turning_overspeed_records_per_switch = turning_overspeed[
	["switch_number", "line"]
].groupby("switch_number").count()
number_turning_overspeed_records_per_switch.sort_values(
	by="line", ascending=False, inplace=True)
number_turning_overspeed_records_per_switch.reset_index(inplace=True)
number_turning_overspeed_records_per_switch.columns = [
	"switch number (turning)", "count (turning)"
]
# concatenate
number_overspeed_records_per_switch = pd.concat(
	[number_straight_overspeed_records_per_switch.iloc[:10],
	 number_turning_overspeed_records_per_switch.iloc[:10]],
	axis=1,
)


# SPATIAL ANALYSIS
# TRAMLINE
# top - barplot
number_straight_overspeed_records_per_line = straight_overspeed[
	["line", "switch_number", "speed"]
].groupby("line").count()
number_straight_overspeed_records_per_line.sort_values(
	by="switch_number", ascending=False, inplace=True)
number_straight_overspeed_records_per_line.reset_index(inplace=True)
number_straight_overspeed_records_per_line["direction"] = "straight"
number_turning_overspeed_records_per_line = turning_overspeed[
	["line", "switch_number", "speed"]
].groupby("line").count()
number_turning_overspeed_records_per_line.sort_values(
	by="switch_number", ascending=False, inplace=True)
number_turning_overspeed_records_per_line.reset_index(inplace=True)
number_turning_overspeed_records_per_line["direction"] = "turning"
# concatenate
number_overspeed_records_per_line = pd.concat(
	[number_straight_overspeed_records_per_line,
	 number_turning_overspeed_records_per_line],
)
# TRAMLINE + SPEED
# bottom - cumulative plot and barplot
n_str_os_per_speed_per_line = straight_overspeed[
	["line", "speed", "vehicle"]
].groupby(["line", "speed"]).count()
n_str_os_per_speed_per_line.reset_index(inplace=True)
n_str_os_per_speed_per_line["direction"] = "straight"
n_trn_os_per_speed_per_line = turning_overspeed[
	["line", "speed", "vehicle"]
].groupby(["line", "speed"]).count()
n_trn_os_per_speed_per_line.reset_index(inplace=True)
n_trn_os_per_speed_per_line["direction"] = "turning"
# concatenate
n_os_per_speed_per_line = pd.concat(
	[n_str_os_per_speed_per_line,
	 n_trn_os_per_speed_per_line],
)