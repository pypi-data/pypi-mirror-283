# clinical_listings/listings.py
from .loader import load_csv, load_excel, load_sql, load_sas
from .formatting import format_titles, format_headers, format_footers, format_listing

def create_listing_from_csv(file_path, **kwargs):
    data = load_csv(file_path)
    return format_listing(data, **kwargs)

def create_listing_from_excel(file_path, **kwargs):
    data = load_excel(file_path)
    return format_listing(data, **kwargs)

def create_listing_from_sql(connection_string, query, **kwargs):
    data = load_sql(connection_string, query)
    return format_listing(data, **kwargs)

def create_listing_from_sas(file_path, **kwargs):
    data = load_sas(file_path)
    return format_listing(data, **kwargs)

