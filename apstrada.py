import vnanalyzer as h
import vcnst as c

def main():
    h.prepare_clean_output_folder('data_out')
    h.open_ZipSession('data_in/013_X_d3_Jurim.zip')
    h.open_SQLiteSession('013_X_d3.sqlite3')

    # h.show_zip_contents()
    h.fill_files_table()
    h.select_distinct_temperatures()
    h.plot_spectra()
    h.combine_pdf_files()

if __name__ == "__main__":
    main()
