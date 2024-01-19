import os
import pandas as pd


SPEED_LIMIT = 15
csv_path = os.path.join(os.getcwd(), "dataset/switch_speed_data.csv")
speed = pd.read_csv(csv_path, parse_dates=["hfk_in"])
speed["#week"] = speed["hfk_in"].dt.isocalendar()["week"]
speed["#day"] = speed["hfk_in"].dt.isocalendar()["day"]

overspeed = speed[speed["speed"] > SPEED_LIMIT]
straight_overspeed = overspeed[overspeed["is_straight"] == True]
turning_overspeed = overspeed[overspeed["is_straight"] == False]
assert len(overspeed) == len(straight_overspeed) + len(turning_overspeed)

# # bottom-right corner: top-N table
# # straight position overspeeding
# number_straight_overspeed_records_per_switch = straight_overspeed[
# 	["switch_number", "line"]
# ].groupby("switch_number").count()
# number_straight_overspeed_records_per_switch.sort_values(
# 	by="line", ascending=False, inplace=True)
# number_straight_overspeed_records_per_switch.reset_index(inplace=True)
# number_straight_overspeed_records_per_switch.columns = [
# 	"switch number (straight)", "count (straight)"
# ]
# # turning position overspeeding
# number_turning_overspeed_records_per_switch = turning_overspeed[
# 	["switch_number", "line"]
# ].groupby("switch_number").count()
# number_turning_overspeed_records_per_switch.sort_values(
# 	by="line", ascending=False, inplace=True)
# number_turning_overspeed_records_per_switch.reset_index(inplace=True)
# number_turning_overspeed_records_per_switch.columns = [
# 	"switch number (turning)", "count (turning)"
# ]
# # concatenate
# number_overspeed_records_per_switch = pd.concat(
# 	[number_straight_overspeed_records_per_switch.iloc[:10],
# 	 number_turning_overspeed_records_per_switch.iloc[:10]],
# 	axis=1,
# )
#
#
