import geopandas as gpd

def filter(src, dst):
    # Load the GeoJSON file
    gdf = gpd.read_file(src)

    # List of year columns (adjust range if needed)
    year_columns = [str(year) for year in range(1980, 2024)]

    # Check if all year columns exist in gdf, if not, filter the list
    year_columns = [col for col in year_columns if col in gdf.columns]

    # Create a mask: True where all year values are zero (or null)
    # If you need to treat nulls, you can fill them or adjust conditions.
    mask = (gdf[year_columns].fillna(0) == 0).all(axis=1)

    # Invert the mask to keep rows that have at least one non-zero year value
    filtered_gdf = gdf[~mask]

    # Save the filtered geodataframe to a new GeoJSON file
    filtered_gdf.to_file(dst, driver="GeoJSON")

main_path = "C:/Users/carolvfs/Box/carolina/work/Projects/CLEETS/Visualization/urban-planner-files/yearly_files"
src_files = ["Yearly_tmin.json", "Yearly_tmax.json", "Yearly_prcp.json"]
dst_files = ["Yearly_tmin_filtered.json", "Yearly_tmax_filtered.json", "Yearly_prcp_filtered.json"]

for i in range(0, 3):
    src = f"{main_path}/{src_files[i]}"
    dst = f"{main_path}/{dst_files[i]}"

    filter(src, dst)

