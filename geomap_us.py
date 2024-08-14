import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from datetime import datetime
from pathlib import Path


def query_database(input_db, input_query):
    con = sqlite3.connect(input_db)
    output_df = pd.read_sql_query(input_query, con)
    con.close()
    return output_df

def save_map_to_disk(input_time, input_filename):
    output_dir = Path(Path(__file__).parents[0], 'maps', 
                    f'{input_time}_{input_filename}')
    plt.savefig(output_dir, bbox_inches="tight", pad_inches=0)
    print(f"File '{output_dir.name}' saved to: {output_dir.parent}")


#------------------------------------------------------------------------------
# PART 0: Define global constants
#------------------------------------------------------------------------------

# Databases with reference and statisticalinfo
ref_db = Path(Path(__file__).parents[0], 'resources', 'definitions.db')
stats_db = Path(Path(__file__).parents[0], 'resources', 'statistics.db')

# Geopackage file
src_geopackage = Path(Path(__file__).parents[0], 'resources', 
                      'cb_2023_us_state_500k',
                      'cb_2023_us_state_500k.shp')

# Directory for fonts
font_jp_dir = Path("C:/Windows", "Fonts", "msgothic.ttc")
fon_num_dir = Path("C:/Windows", "Fonts", "tahoma.ttf")

# Set font
plt.rcParams['font.family'] = "MS Gothic"

# Set region definition
region = "census_region"

# Set timestamp
timestamp = datetime.now().astimezone().strftime(f"%y%m%dT%H%M%S%z")


#------------------------------------------------------------------------------
# PART 1: Import data
#------------------------------------------------------------------------------

# Connect to database
df_info = query_database(ref_db, "SELECT * FROM states_territories")
df_stats = query_database(stats_db, "SELECT * FROM united_states")

# Import geopackage file
gdf_raw = gpd.read_file(src_geopackage)


#------------------------------------------------------------------------------
# PART 2: Preprecess data for downstream analysis
#------------------------------------------------------------------------------

# Remove overseas territories from map
df_50 = df_info.loc[df_info["territory"]==0]
gdf_50 = gdf_raw.loc[gdf_raw["NAME"].isin(df_50["name"].to_list())]

# Limit to continental United States
gdf_48 = gdf_50.loc[~gdf_50["NAME"].isin(["Alaska", "Hawaii"])]


#------------------------------------------------------------------------------
# PART 3: Save map of the United States with color-coded regions
#------------------------------------------------------------------------------

# Assign colors to different regions of the United States
state_list = gdf_48["NAME"].tolist()
state_dict = {f"{item}":
              f"{df_50.loc[df_50['name']==item, 'census_region'].values[0]}"
              for item in state_list}
color_list = [state_dict[key] for key in state_dict]

# Add assigned colors to geodataframe
gdf_48 = gdf_48.assign(color=color_list)

# Generate map
fig, ax = plt.subplots(figsize=(18,12))
gdf_48.plot(ax=ax, column='color', linewidth=0.2, edgecolor='white', 
            legend=True, categorical=True, cmap='tab10')
ax.set_axis_off()
fig.tight_layout()

# Save map as svg file
save_map_to_disk(timestamp, 'usa_regions.svg')


#------------------------------------------------------------------------------
# PART 4: Save map of the United States with selected states
#------------------------------------------------------------------------------

# Select specific groups of states
state_list = gdf_48["NAME"].tolist()
set_1 = {x[0] for x in df_stats.loc[df_stats["lived"]==1,["name"]].values}
set_2 = {x[0] for x in df_stats.loc[df_stats["overnight"]==1,["name"]].values}
set_3 = {x[0] for x in df_stats.loc[df_stats["visited"]==1,["name"]].values}
set_3 = set_3-set_2-set_1
set_2 = set_2-set_1

# Generate map
fig, ax = plt.subplots(figsize=(18,12))
gdf_48.plot(ax=ax, linewidth=0.2, facecolor='gainsboro', edgecolor='snow')

# Plot colors for selected categories
gdf_48.loc[gdf_48['NAME'].isin(set_1)].plot(
    ax=ax, linewidth=0.2, facecolor="#3399FF", edgecolor='snow')
gdf_48.loc[gdf_48['NAME'].isin(set_2)].plot(
    ax=ax, linewidth=0.2, facecolor="#FF9933", edgecolor='snow')
gdf_48.loc[gdf_48['NAME'].isin(set_3)].plot(
    ax=ax, linewidth=0.2, facecolor="#FFCC9A", edgecolor='snow')
ax.set_axis_off()
fig.tight_layout()

# Save map as svg file
save_map_to_disk(timestamp, 'usa_selected.svg')