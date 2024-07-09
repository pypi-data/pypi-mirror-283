# clinical_listings/utils.py
from fpdf import FPDF
import pandas as pd

class PDF(FPDF):
    def header(self):
        if hasattr(self, 'title'):
            self.set_font('Courier', 'B', 12)
            self.cell(0, 10, self.title, 0, 1, 'C')
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Courier', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def table(self, dataframe):
        self.set_font('Courier', '', 8)
        col_widths = [self.get_string_width(col) for col in dataframe.columns]
        col_widths = [max(w, 20) for w in col_widths]

        for i, col in enumerate(dataframe.columns):
            self.cell(col_widths[i], 10, col, 1)
        self.ln()

        for _, row in dataframe.iterrows():
            for i, value in enumerate(row):
                self.cell(col_widths[i], 10, str(value), 1)
            self.ln()

def save_to_pdf(dataframe: pd.DataFrame, file_path: str, title: str = "Clinical Trial Listing"):
    pdf = PDF()
    pdf.add_page()
    pdf.title = title
    pdf.table(dataframe)
    pdf.output(file_path)

# Update the create_listing_from_csv function to include title
def create_listing_from_csv(file_path, **kwargs):
    data = load_csv(file_path)
    formatted_listing = format_listing(data, **kwargs)
    return formatted_listing
