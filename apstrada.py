import vnanalyzer as h
import vcnst as c


def process_X_d3():
    h.open_ZipSession('data_in/013_X_d3_Jurim.zip')
    h.open_SQLiteSession('013_X_d3.sqlite3')

    # h.show_zip_contents()
    h.fill_files_table()
    h.select_distinct_temperatures()
    h.plot_spectra()
    h.combine_pdf_files('013_X_d3.pdf')


def process_sample_N():
    h.open_ZipSession('data_in/2023-03-14_013_N_X.zip')
    h.open_SQLiteSession('sample_N.sqlite3')
    h.db.create_tables_sample_N()
    # h.show_zip_contents()
    h.fill_files_table_sample_N()
#    h.select_distinct_temperatures()
    h.select_distinct_sample_IDs()
    h.plot_spectra_sample_N()
    h.plot_analysis_sample_N()
    h.plot_cor_no_f()

    h.combine_pdf_files('sample_N.pdf')


def main():
    h.prepare_clean_output_folder('data_out')
    process_sample_N()


if __name__ == "__main__":
    main()
