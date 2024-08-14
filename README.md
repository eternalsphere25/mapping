## Overview
This repository contains code that generates geographic maps of various countries listed below.

## Region Definitions

### United States:
* Regions are as defined by the [United States Census Bureau](https://www.census.gov/programs-surveys/economic-census/guidance-geographies/levels.html)  
* Territories are as defined by the [United States Department of the Interior](https://www.doi.gov/library/internet/insular)
* Former territories are as defined by various departments:
  * Philipines: 
    * [United States Department of State](https://history.state.gov/countries/philippines)
    * [Central Intelligenca Agency (CIA)](https://www.cia.gov/the-world-factbook/countries/philippines/)
  * Panama Canal Zone:
    * [Library of Congress](https://guides.loc.gov/chronicling-america-panama-canal)

### Japan:
* Regions are as defined as follows:
  * 7 Regions:
    * Traditional
    * [NHK](https://www.stat.go.jp/data/shugyou/1997/3-1.html)
  * 8 Regions:
    * Traditional
  * 10 Regions:
    * [Cabinet Office of Japan](https://www5.cao.go.jp/j-j/cr/cr16/chr16_04.html)
    * [Statistics Bureau of Japan](https://www.stat.go.jp/data/shugyou/1997/3-1.html)
  * 11 Regions:
    * [Cabinet Office of Japan](https://www5.cao.go.jp/j-j/cr/cr16/chr16_04.html)

### World
* Regions are defined as follows:
  * [United Nations Statistics Division](https://unstats.un.org/unsd/methodology/m49/)
  * [UNESCO](https://unesdoc.unesco.org/ark:/48223/pf0000148165)

## External Dependencies
* [GeoPandas](https://geopandas.org/en/stable/)
* [Matplotlib](https://matplotlib.org/)
* [pandas](https://pandas.pydata.org/)

## Geopackage Data Download Links
* [United States](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html)
* [Japan](https://www.gsi.go.jp/kankyochiri/gm_jpn.html)

## Map Color Information
Map colors can be found on the package websites:
* https://matplotlib.org/stable/gallery/color/named_colors.html
* https://gropandas.org/en/stabe/docs/user_guide/mapping.html

## Schema for 'statistics.db'
The 'statistics.db' file is not included for privacy reasons. A new one can be
generated using the schema below:
* Table name: Country name (ex. 'united_states')
* Table columns:
  * id (ex. '0')
  * name (ex. 'Hawaii')
  * visited (0=False, 1=True)
  * overnight (0=False, 1=True)
  * lived (0=False, 1=True)