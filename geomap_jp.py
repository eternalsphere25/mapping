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

def remove_kurils(input_gdf):
    output_gdf = input_gdf.loc[(input_gdf["laa"] != "shikotan-mura")
                               & (input_gdf["laa"] != "Shikotan-mura")
                               & (input_gdf["laa"] != "Tomari Mura")
                               & (input_gdf["laa"] != "Ruyabetsu Mura")
                               & (input_gdf["laa"] != "Rubetsu Mura")
                               & (input_gdf["laa"] != "Shana Mura")
                               & (input_gdf["laa"] != "Shibetoro Mura")]
    
    output_gdf = output_gdf.drop([24,25,26,27,28,29,30,32,33])
    return output_gdf

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
src_geofile = Path(Path(__file__).parents[0], 'resources', 'gadm41_JPN.gpkg')
src_shapefile = Path(Path(__file__).parents[0], 'resources', 
                     'gm-jpn-all_u_2_2', 'polbnda_jpn.shp')

# Directory for fonts
font_jp_dir = Path("C:/Windows", "Fonts", "msgothic.ttc")
fon_num_dir = Path("C:/Windows", "Fonts", "tahoma.ttf")

# Set font
plt.rcParams['font.family'] = "MS Gothic"

# Set region definition
region = "region_10"

# Set stance on the Southern Kuril Islands (disputed between Japan and Russia)
kurils = True

# Set timestamp
timestamp = datetime.now().astimezone().strftime(f"%y%m%dT%H%M%S%z")


#------------------------------------------------------------------------------
# PART 1: Import data
#------------------------------------------------------------------------------

# Connect to databases
df_info = query_database(ref_db, "SELECT * FROM prefectures")
df_stats = query_database(stats_db, "SELECT * FROM japan")

# Import geopackage file
gdf_raw = gpd.read_file(src_shapefile)


#------------------------------------------------------------------------------
# PART 2: Preprecess data for downstream analysis
#------------------------------------------------------------------------------

# Remove Southern Kuril Islands if set to do so
if kurils == False:
    gdf_raw = remove_kurils(gdf_raw)

# Merge all municipalities to the prefectural level
gdf_pref = gdf_raw.copy().drop(columns=["f_code", "coc", "laa", "pop", 
                                        "ypc", "adm_code", "salb", "soc"])
gdf_pref = gdf_pref.dissolve(by="nam", aggfunc='sum').reset_index()

# Convert prefecture names from English to Japanese
df_info["order"] = range(len(df_info))
gdf_pref_jp = gdf_pref.merge(df_info, left_on="nam", right_on="name_en")
gdf_pref_jp = gdf_pref_jp[
    ["order", "name", f"{region}", "geometry"]].sort_values(by=["order"])
gdf_pref_jp = gdf_pref_jp[
    ["name", f"{region}", "geometry"]].reset_index(drop=True)


#------------------------------------------------------------------------------
# PART 3: Save map of Japan with color-coded prefectures
#------------------------------------------------------------------------------

# Assign colors to different regions of Japan
pref_list = gdf_pref_jp[f"{region}"]
color_list = ["北海道" if item == "北海道地方"
              else "東北" if item == "東北地方"
              else "関東" if item == "関東地方"
              else "北陸" if item == "北陸地方"
              else "東海" if item == "東海地方"
              else "近畿" if item == "近畿地方"
              else "中国" if item == "中国地方"
              else "四国" if item == "四国地方"
              else "九州" if item == "九州地方"
              else "沖縄" for item in pref_list]
gdf_pref_jp["color"] = color_list

# Generate map
fig, ax = plt.subplots(figsize=(18,12))
gdf_pref_jp.plot(ax=ax, column='color', linewidth=0.2, edgecolor='white', 
                 legend=True, categorical=True, cmap='tab10')
ax.set_axis_off()
fig.tight_layout()

# Save map as svg file
save_map_to_disk(timestamp, 'japan_prefectures.svg')


#------------------------------------------------------------------------------
# PART 4: Save map of Japan with selected prefectures
#------------------------------------------------------------------------------

# Select specific groups of prefectures
pref_list = gdf_pref_jp[f"{region}"]
set_1 = {x[0] for x in df_stats.loc[df_stats["lived"]==1,["name"]].values}
set_2 = {x[0] for x in df_stats.loc[df_stats["overnight"]==1,["name"]].values}
set_3 = {x[0] for x in df_stats.loc[df_stats["visited"]==1,["name"]].values}
set_3 = set_3-set_2-set_1
set_2 = set_2-set_1

# Generate map
fig, ax = plt.subplots(figsize=(18,12))
gdf_pref_jp.plot(ax=ax, linewidth=0.2, facecolor='gainsboro', edgecolor='snow')

# Plot colors for selected categories
gdf_pref_jp.loc[gdf_pref_jp['name'].isin(set_1)].plot(
    ax=ax, linewidth=0.2, facecolor="#3399FF", edgecolor='snow')
gdf_pref_jp.loc[gdf_pref_jp['name'].isin(set_2)].plot(
    ax=ax, linewidth=0.2, facecolor="#FF9933", edgecolor='snow')
gdf_pref_jp.loc[gdf_pref_jp['name'].isin(set_3)].plot(
    ax=ax, linewidth=0.2, facecolor="#FFCC9A", edgecolor='snow')
ax.set_axis_off()
fig.tight_layout()

# Save map as svg file
save_map_to_disk(timestamp, 'japan_selected.svg')