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
                      'WorldPolygons_11_3_1_BETA_30Apr2024',
                      'WorldPolygons11_3_1.gpkg')

# Directory for fonts
font_jp_dir = Path("C:/Windows", "Fonts", "msgothic.ttc")
fon_num_dir = Path("C:/Windows", "Fonts", "tahoma.ttf")

# Set font
plt.rcParams['font.family'] = "MS Gothic"

# Set region definition
region = "census_region"

# Set timestamp
timestamp = datetime.now().astimezone().strftime(f"%y%m%dT%H%M%S%z")

# Show all rows in pandas dataframe
pd.set_option("display.max_rows", None)


#------------------------------------------------------------------------------
# PART 1: Import data
#------------------------------------------------------------------------------

# Connect to database
df_info = query_database(ref_db, "SELECT * FROM states_territories")
df_stats = query_database(stats_db, "SELECT * FROM united_states")

# Import geopackage file
gdf_raw = gpd.read_file(src_geopackage, layer='DoS_WP_11_3_1_G99_5')
print(gpd.list_layers(src_geopackage))


#------------------------------------------------------------------------------
# PART 2: Preprecess data for downstream analysis
#------------------------------------------------------------------------------

print(gdf_raw.columns)
gdf_world = gdf_raw[['WP_Name', 'DOS_Short']]
print(gdf_world)

country_list = ['United States', 'Japan', 'Philippines',
                'Mongolia', 'United Kingdom', 'Taiwan', 'Palau',
                'Colombia', 'Australia']

#not_here_list = ['Vietnam', 'Bangladesh', 'Egypt', 'Singapore', 'China', 
#                 'Italy', 'Germany']

# Generate map
fig, ax = plt.subplots(figsize=(18,12))
gdf_raw.plot(ax=ax, linewidth=0.2, facecolor='gainsboro', edgecolor='snow')

"""
gdf_raw.loc[gdf_raw['DOS_Short'].isin(country_list)].plot(
    ax=ax, linewidth=0.2, facecolor="#3399FF", edgecolor='snow')
#gdf_raw.loc[gdf_raw['DOS_Short'].isin(not_here_list)].plot(
#    ax=ax, linewidth=0.2, facecolor="#FF9933", edgecolor='snow')
"""

ax.set_axis_off()
fig.tight_layout()
#plt.show()

# Save map as svg file
save_map_to_disk(timestamp, 'world_selected.svg')