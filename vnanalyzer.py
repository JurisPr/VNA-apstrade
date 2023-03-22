import os
import zipfile
import sqlite3
import vcnst as c
import apstrada
from matplotlib import pyplot as plt
import numpy as np
from subprocess import check_output

if __name__ == "__main__":
    apstrada.main()


def prepare_clean_output_folder(folder_name):
    global OUTFOLDER
    OUTFOLDER = folder_name
    if os.path.exists(OUTFOLDER):
        for f in os.listdir(OUTFOLDER):
            os.remove(os.path.join(OUTFOLDER, f))
    else:
        os.mkdir(OUTFOLDER)
    print(f"OUTFOLDER = {OUTFOLDER}")


class ZipSession:
    def __init__(self, zipfilename):
        self.zf = zipfile.ZipFile(zipfilename, "r")
        print('ZipFile opened')

    def __del__(self):
        self.zf.close()
        print('ZipFile closed')


def open_ZipSession(zipfilename):
    global zip
    zip = ZipSession(zipfilename)


class SQLiteSession:

    def __init__(self, dbfilename):
        self.con = sqlite3.connect(f"{OUTFOLDER}/{dbfilename}")
        self.cur = self.con.cursor()
        self.cur.execute("PRAGMA foreign_keys = ON")
        print('SQLite opened')

    def __del__(self):
        self.con.commit()
        print('DB committed')

    def create_tables(self):
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {c.FILE_TABLE}(
            {c.COL_MEMBER_FILE_NAME} TEXT PRIMARY KEY,
            {c.COL_KELVIN} FLOAT NOT NULL,
            {c.COL_VGATE} FLOAT NOT NULL
            )""")
        print('tables created')


def open_SQLiteSession(dbfilename):
    global db
    db = SQLiteSession(dbfilename)
    db.create_tables()


def show_zip_contents():
    for member_file_name in zip.zf.namelist():
        print(f"member_file_name = {member_file_name}")


def fill_files_table():
    for member_file_name in zip.zf.namelist():
        kelvin = None
        vGate = None

#        if '211'in member_file_name:
#            continue

        if '_6p3K_' in member_file_name:
            kelvin = 6.3
        elif '_7K_' in member_file_name:
            kelvin = 7.0
        elif '_9K_' in member_file_name:
            kelvin = 9.0
        elif '_10K_' in member_file_name:
            kelvin = 10.0
        elif '_12K_' in member_file_name:
            kelvin = 12.0
        elif '_15K_' in member_file_name:
            kelvin = 15.0
        elif '_20K_' in member_file_name:
            kelvin = 20.0
        elif '_25K_' in member_file_name:
            kelvin = 25.0
        elif '_30K_' in member_file_name:
            kelvin = 30.0
        elif '_34K_' in member_file_name:
            kelvin = 34.0
        elif '_40K_' in member_file_name:
            kelvin = 40.0
            continue
        elif '_60K_' in member_file_name:
            kelvin = 60.0
        elif '_80K_' in member_file_name:
            kelvin = 80.0
        elif '_100K_' in member_file_name:
            kelvin = 100.0
            continue
        elif '_120K_' in member_file_name:
            kelvin = 120.0
        elif '_140K_' in member_file_name:
            kelvin = 140.0
        elif '_160K_' in member_file_name:
            kelvin = 160.0

        if '_Ug-5p0V' in member_file_name:
            vGate = -5.0
        elif '_Ug5p0V' in member_file_name:
            vGate = 5.0
        elif '_Ug0p0V' in member_file_name:
            vGate = 0.0
        elif '_U0p0V' in member_file_name:
            vGate = 0.0
        elif '_Ug4p0V' in member_file_name:
            vGate = 4.0
        elif '_Ug-4p0V' in member_file_name:
            vGate = -4.0
        elif '_Ug3p0V' in member_file_name:
            vGate = 3.0
        elif '_Ug-3p0V' in member_file_name:
            vGate = -3.0
        elif '_Ug-2p0V' in member_file_name:
            vGate = -2.0

        if kelvin is None or vGate is None:
            print(f"member_file_name = {member_file_name}")
        else:
            db.cur.execute(f"""INSERT INTO {c.FILE_TABLE}
                    ({c.COL_MEMBER_FILE_NAME},{c.COL_KELVIN},{c.COL_VGATE})
                    VALUES (?,?,?)""",
                           [member_file_name, kelvin, vGate])


temperatures = []


def select_distinct_temperatures():
    global temperatures
    db.cur.execute(f"""SELECT DISTINCT
                    {c.COL_KELVIN}
            FROM    {c.FILE_TABLE}
            ORDER BY {c.COL_KELVIN}
            """)
    for sel_kelvin in db.cur.fetchall():
        temperatures.append(sel_kelvin[0])


def load_csv(member_file_name):
    file_contents = zip.zf.read(member_file_name)
    file_lines = file_contents.decode('ascii').splitlines()
    col1, col2, col3 = [], [], []
    for full_line in file_lines:
        line = full_line.strip(" \t\n\r")
        if '#' in line:
            continue
        if 'freq' in line:
            continue
        fields = line.split('\t')
        if len(fields) == 3:
            col1.append(float(fields[0].replace(",", ".")))
            col2.append(float(fields[1].replace(",", ".")))
            col3.append(float(fields[2].replace(",", ".")))
    return {'col1': col1,
            'col2': col2,
            'col3': col3}


def plot_spectra():
    page_no = 1000
    for kelvin in temperatures:
        page_no += 1
        fig = plt.figure()
        plt.rcParams.update({'font.size': 8})
        fig.set_figheight(c.A4_short_in)
        fig.set_figwidth(c.A4_long_in)
        subplot_shape = (2, 4)

        ax_db = plt.subplot2grid(
            shape=subplot_shape, loc=(0, 0), colspan=2, rowspan=1)
        ax_delta = plt.subplot2grid(
            shape=subplot_shape, loc=(0, 2), colspan=2, rowspan=1)
        ax_ang = plt.subplot2grid(
            shape=subplot_shape, loc=(1, 1), colspan=2, rowspan=1)
        axs = (ax_db, ax_delta, ax_ang)

        db.cur.execute(f"""SELECT
                    {c.COL_MEMBER_FILE_NAME},
                    {c.COL_VGATE}
            FROM    {c.FILE_TABLE}
            WHERE {c.COL_KELVIN} = ?
            ORDER BY {c.COL_VGATE}
            """, [kelvin])
        sum = None
        sel_file_vgates = db.cur.fetchall()
        for sel_file_vgate in sel_file_vgates:
            member_file_name = sel_file_vgate[0]
            vGate = sel_file_vgate[1]
            csv = load_csv(member_file_name)
            f = np.array(csv['col1'])*1E-6
            dB = csv['col2']
            ang = csv['col3']

            ax_db.plot(
                f, dB, label=f"{member_file_name.split('/')[-1]}")
            ax_ang.plot(
                f, ang, label=f"Vg={vGate}V")

            if sum is None:
                sum = np.array(dB)
            else:
                sum += dB

        mean = sum/len(sel_file_vgates)
        for sel_file_vgate in sel_file_vgates:
            member_file_name = sel_file_vgate[0]
            vGate = sel_file_vgate[1]
            csv = load_csv(member_file_name)
            f = np.array(csv['col1'])*1E-6
            dB = csv['col2']

            delta = dB-mean

            ax_delta.plot(
                f, delta, label=f"Vg={vGate}V")

        subplot_titles = (f"T={kelvin}K", 'subtracted mean', "phase")
        y_labels = ('A, dB', 'A, dB', 'angle, deg')

        for ref_type_n in range(3):
            axs[ref_type_n].set(xlabel='$f$, MHz')
            axs[ref_type_n].title.set_text(subplot_titles[ref_type_n])
            axs[ref_type_n].set(ylabel=y_labels[ref_type_n])
            axs[ref_type_n].legend(loc="best")
            axs[ref_type_n].grid()

            axs[ref_type_n].set(
                xlim=[min(f), max(f)])

        plt.tight_layout()
        # plt.show()
        plt.savefig(f"{OUTFOLDER}/page{page_no}.pdf", dpi=c.DPI)
        plt.close()


def combine_pdf_files():
    check_output(
            f"pdftk {OUTFOLDER}\\*.pdf cat output {OUTFOLDER}\\1all_spectra.pdf", shell=True).decode()