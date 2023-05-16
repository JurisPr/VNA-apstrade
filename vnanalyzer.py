import os
import zipfile
import sqlite3
import vcnst as c
import apstrada
from matplotlib import pyplot as plt
import numpy as np
from subprocess import check_output
import matplotlib.cm as cm
from scipy import interpolate

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

    def create_tables_sample_N(self):
        self.cur.execute(f"""DROP TABLE IF EXISTS {c.FILE_TABLE}""")
        print(f"old {c.FILE_TABLE} table deleted")
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {c.FILE_TABLE}(
            {c.COL_MEMBER_FILE_NAME} TEXT PRIMARY KEY,
            {c.COL_KELVIN} FLOAT NOT NULL,
            {c.COL_VGATE} FLOAT NOT NULL,
            {c.COL_V_SOURCE_DRAIN} FLOAT NOT NULL,
            {c.COL_SAMPLE_ID} TEXT NOT NULL,
            {c.COL_PEAK_MHZ} FLOAT,
            {c.COL_PEAK_DB} FLOAT
            )""")
        print(f"new {c.FILE_TABLE} table created")


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


def fill_files_table_sample_N():
    global xfile

    for member_file_name in zip.zf.namelist():

        kelvin = None
        vGate = None
        vSourceDrain = None
        sampleID = None

        if "237_supp15V_Ug0p0V_Ig0p01nA__Usd_0p05V_po0_9K+Isd_025uA" in member_file_name:
            xfile = member_file_name
            print(xfile)

        if not member_file_name.endswith(".csv"):
            continue
        if '050_' in member_file_name:
            continue
        if '012_' in member_file_name:
            continue
        if '011_' in member_file_name:
            continue
        if '036_' in member_file_name:
            continue

        if '_9K' in member_file_name:
            kelvin = 9.0
        elif '_8K' in member_file_name:
            kelvin = 8.0
        elif '_6K' in member_file_name:
            kelvin = 6.0

        if 'Usd_0p05V' in member_file_name:
            vSourceDrain = 0.05
        elif 'Usd_0p04V' in member_file_name:
            vSourceDrain = 0.04

        if 'Ug0p0V' in member_file_name:
            vGate = 0.0
        elif 'Ug-8p0V' in member_file_name:
            vGate = -8.0
        elif 'Ug-7p0V' in member_file_name:
            vGate = -7.0
        elif 'Ug-6p0V' in member_file_name:
            vGate = -6.0
        elif 'Ug-5p0V' in member_file_name:
            vGate = -5.0
        elif 'Ug-4p0V' in member_file_name:
            vGate = -4.0
        elif 'Ug-3p0V' in member_file_name:
            vGate = -3.0
        elif 'Ug-2p0V' in member_file_name:
            vGate = -2.0
        elif 'Ug-1p0V' in member_file_name:
            vGate = -1.0
        elif 'Ug8p0V' in member_file_name:
            vGate = 8.0
        elif 'Ug7p0V' in member_file_name:
            vGate = 7.0
        elif 'Ug6p0V' in member_file_name:
            vGate = 6.0
        elif 'Ug5p0V' in member_file_name:
            vGate = 5.0
        elif 'Ug4p0V' in member_file_name:
            vGate = 4.0
        elif 'Ug3p0V' in member_file_name:
            vGate = 3.0
        elif 'Ug2p0V' in member_file_name:
            vGate = 2.0
        elif 'Ug1p0V' in member_file_name:
            vGate = 1.0
        elif 'Ug3p0V' in member_file_name:
            vGate = 3.0

        if 'Planais' in member_file_name:
            sampleID = 'Planais'
        elif 'nowire' in member_file_name:
            sampleID = 'nowire'
        elif '0677uA.' in member_file_name or '0659uA.' in member_file_name:
            sampleID = 'sample_N'

        if kelvin is None or vGate is None or vSourceDrain is None or sampleID is None:
            print(f"member_file_name = {member_file_name}")
        else:
            db.cur.execute(f"""INSERT INTO {c.FILE_TABLE}
                    ({c.COL_MEMBER_FILE_NAME},{c.COL_KELVIN},{c.COL_VGATE},{c.COL_V_SOURCE_DRAIN},{c.COL_SAMPLE_ID})
                    VALUES (?,?,?,?,?)""",
                           [member_file_name, kelvin, vGate, vSourceDrain, sampleID])


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
    print(temperatures)


sample_IDs = []


def select_distinct_sample_IDs():
    global sample_IDs
    db.cur.execute(f"""SELECT DISTINCT
                    {c.COL_SAMPLE_ID}
            FROM    {c.FILE_TABLE}
            ORDER BY {c.COL_SAMPLE_ID}
            """)
    for sel_id in db.cur.fetchall():
        sample_IDs.append(sel_id[0])
    print(sample_IDs)


#            {c.COL_VGATE} FLOAT NOT NULL,
#            {c.COL_V_SOURCE_DRAIN} FLOAT NOT NULL,
#            {c.COL_SAMPLE_ID} TEXT NOT NULL


def load_csv(member_file_name):
    file_contents = zip.zf.read(member_file_name)
    file_lines = file_contents.decode('ascii').splitlines()
    col1, col2, col3 = [], [], []
    for full_line in file_lines:
        #        print(full_line)
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


page_no = 2000


def plot_spectra_sample_N():
    global page_no
    for sample_id in sample_IDs:
        db.cur.execute(f"""SELECT DISTINCT
                    {c.COL_KELVIN}
            FROM    {c.FILE_TABLE}
            WHERE {c.COL_SAMPLE_ID} = ?
            ORDER BY {c.COL_KELVIN}
            """, [sample_id])
        temps_k = []
        for sel_k in db.cur.fetchall():
            temps_k.append(sel_k[0])
        for kelvin in temps_k:
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
                shape=subplot_shape, loc=(1, 2), colspan=2, rowspan=1)
            ax_zoomin = plt.subplot2grid(
                shape=subplot_shape, loc=(1, 0), colspan=2, rowspan=1)

            axs = (ax_db, ax_delta, ax_ang, ax_zoomin)

            db.cur.execute(f"""SELECT
                        {c.COL_MEMBER_FILE_NAME},
                        {c.COL_VGATE}
                FROM    {c.FILE_TABLE}
                WHERE {c.COL_KELVIN} = ? AND {c.COL_SAMPLE_ID} = ?
                ORDER BY {c.COL_VGATE} DESC
                """, [kelvin, sample_id])
            sel_file_vgates = db.cur.fetchall()
            sum = None
            for sel_file_vgate in sel_file_vgates:
                member_file_name = sel_file_vgate[0]
                #print (member_file_name)
                vGate = sel_file_vgate[1]
                csv = load_csv(member_file_name)

                f = np.array(csv['col1'])*1E-6
                dB = csv['col2']
                ang = csv['col3']
                ax_db.plot(
                    f, dB, label=f"Vg={vGate}V", color=cm.jet(vGate/16.0+0.5))

                f_min, f_max = 1.48, 1.58
                peak_i = np.where((f >= f_min) & (f <= f_max))

                p = np.polyfit(f[peak_i], np.array(dB)[peak_i], 6,)
                f_peak = np.linspace(f_min, f_max, num=101)
                db_peak = np.polyval(p, f_peak)

                d1 = np.polyder(p, 1)
                r1 = np.roots(d1)
                d2 = np.polyder(p, 2)
                if sample_id == 'sample_N':
                    real_roots_i = np.where(
                        np.isreal(r1) & (np.polyval(d2, r1) > 0))
                    if len(real_roots_i) != 1:
                        print(
                            "##########################################################")
                    print(real_roots_i)
                    f_0 = np.real(r1[real_roots_i][0])
                    db_0 = np.polyval(p, f_0)
                    ax_zoomin.plot(
                        f_0, db_0, '+', color=cm.jet(vGate/16.0+0.5))

                    db.cur.execute(f"""UPDATE {c.FILE_TABLE}
                            SET
                                {c.COL_PEAK_MHZ} = ?,
                                {c.COL_PEAK_DB} = ?
                            WHERE
                                {c.COL_MEMBER_FILE_NAME} = ?""",
                                   [f_0, db_0, member_file_name])


#                tck = interpolate.splrep(f, dB)
#                db_peak =interpolate.splev(f_peak, tck)

#                db_peak=np.interp(f_peak,f, dB,)

                ax_zoomin.plot(
                    f_peak, db_peak, label=f"Vg={vGate}V", color=cm.jet(vGate/16.0+0.5))

                print(peak_i)

                if sum is None:
                    sum = np.array(dB)
                else:
                    sum += dB

            xcsv = load_csv(xfile)
            xf = np.array(xcsv['col1'])*1E-6
            xdB = xcsv['col2']
            ax_db.plot(
                xf, xdB, '--', label=xfile.split('/')[1][:10], color='k')

            mean = sum/len(sel_file_vgates)
            for sel_file_vgate in sel_file_vgates:
                member_file_name = sel_file_vgate[0]
                vGate = sel_file_vgate[1]
                csv = load_csv(member_file_name)
                f = np.array(csv['col1'])*1E-6
                dB = csv['col2']

                delta = dB-mean

                ax_delta.plot(
                    f, delta, label=f"Vg={vGate}V", color=cm.jet(vGate/16.0+0.5))

                ax_ang.plot(
                    f, delta, label=f"Vg={vGate}V", color=cm.jet(vGate/16.0+0.5))

                ax_zoomin.plot(
                    f, dB, '.', color=cm.jet(vGate/16.0+0.5))  # , label=f"Vg={vGate}V"

            subplot_titles = (
                f"T={kelvin}K", 'subtracted mean', "Zoom in Delta", "Zoom in")
            y_labels = ('A, dB', 'ΔA, dB', 'ΔA, dB', 'A, dB')

            for ref_type_n in range(4):
                axs[ref_type_n].set(xlabel='$f$, MHz')
                axs[ref_type_n].title.set_text(subplot_titles[ref_type_n])
                axs[ref_type_n].set(ylabel=y_labels[ref_type_n])
                axs[ref_type_n].legend(loc="best")
                axs[ref_type_n].grid()

                if ref_type_n == 2:
                    axs[ref_type_n].set(xlim=[1, 2])
                    axs[ref_type_n].set(ylim=[-0.5, 0.5])
                elif ref_type_n == 3:
                    axs[ref_type_n].set(xlim=[1.475, 1.6])
                    axs[ref_type_n].set(ylim=[-43.5, -40])
                else:
                    axs[ref_type_n].set(
                        xlim=[min(f), max(f)])

                if ref_type_n == 0:
                    axs[ref_type_n].set(ylim=[-50, -10])
                if ref_type_n == 1:
                    axs[ref_type_n].set(ylim=[-3.5, 3.5])

            plt.tight_layout()
#            plt.show()

            plt.savefig(f"{OUTFOLDER}/page{page_no}.pdf", dpi=c.DPI)
            plt.close()


def plot_analysis_sample_N():
    global page_no
    page_no += 1
    fig = plt.figure()
    plt.rcParams.update({'font.size': 8})
    fig.set_figheight(c.A4_short_in)
    fig.set_figwidth(c.A4_long_in)
    subplot_shape = (2, 4)

    ax_db6 = plt.subplot2grid(
        shape=subplot_shape, loc=(0, 0), colspan=2, rowspan=1)
    ax_f6 = plt.subplot2grid(
        shape=subplot_shape, loc=(0, 2), colspan=2, rowspan=1)
    ax_db8 = plt.subplot2grid(
        shape=subplot_shape, loc=(1, 0), colspan=2, rowspan=1)
    ax_f8 = plt.subplot2grid(
        shape=subplot_shape, loc=(1, 2), colspan=2, rowspan=1)

    axs = (ax_db6, ax_f6, ax_db8, ax_f8)

    sample_id = 'sample_N'
    db.cur.execute(f"""SELECT DISTINCT
                    {c.COL_KELVIN}
            FROM    {c.FILE_TABLE}
            WHERE {c.COL_SAMPLE_ID} = ?
            ORDER BY {c.COL_KELVIN}
            """, [sample_id])
    for sel_kelvin in db.cur.fetchall():
        db.cur.execute(f"""SELECT
                        {c.COL_VGATE},
                        {c.COL_PEAK_MHZ},
                        {c.COL_PEAK_DB}
                FROM    {c.FILE_TABLE}
                WHERE {c.COL_KELVIN} = ? AND {c.COL_SAMPLE_ID} = ?
                ORDER BY {c.COL_VGATE}
                """, [sel_kelvin[0], sample_id])
        vGate = []
        peak_MHz = []
        peak_dB = []
        for rez in db.cur.fetchall():
            vGate.append(rez[0])
            peak_MHz.append(rez[1])
            peak_dB.append(rez[2])

        print(sel_kelvin[0])
        if sel_kelvin[0] == 8.0:
            ax_db, ax_f = ax_db8, ax_f8
        else:
            ax_db, ax_f = ax_db6, ax_f6

        ax_db.plot(vGate, peak_dB, "o", color='k')
        p = np.polyfit(vGate, peak_dB, 1)
        rho = np.corrcoef(vGate, peak_dB)
        vGends = [vGate[0], vGate[-1]]
        dBends = np.polyval(p, vGends)
        ax_db.plot(vGends, dBends, color='k')
        ax_db.text(vGends[0], dBends[1], "$\\rho$ = " +
                   "{:.3f}".format(rho[0, 1]), size=10)

        ax_db.title.set_text(f"T={sel_kelvin[0]}")

        ax_db.set(ylabel='A, dB')
        ax_f.plot(vGate, peak_MHz, "o", color='k')

        pf = np.polyfit(vGate, peak_MHz, 1)
        rhof = np.corrcoef(vGate, peak_MHz)
        vGendsf = [vGate[0], vGate[-1]]
        fends = np.polyval(pf, vGendsf)
        ax_f.plot(vGendsf, fends, color='k')
        ax_f.text(vGendsf[0], fends[1], "$\\rho$ = " +
                  "{:.3f}".format(rhof[0, 1]), size=10)

        ax_f.title.set_text(f"T={sel_kelvin[0]}")
        ax_f.set(ylabel='f, MHz')
    for ax in axs:
        ax.grid()
        ax.set(xlabel='$V_g$, V')

    plt.tight_layout()
#            plt.show()

    plt.savefig(f"{OUTFOLDER}/page{page_no}.pdf", dpi=c.DPI)
    plt.close()
#    axs = (ax_db6, ax_f6, ax_db8, ax_f8)
#
#
#


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
        y_labels = ('A, dB', 'ΔA, dB', 'ΔA, dB')

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


def combine_pdf_files(pdffilename):
    check_output(
        f"pdftk {OUTFOLDER}\\*.pdf cat output {pdffilename}", shell=True).decode()

matrix = {}

def plot_cor_no_f():
    global page_no
    page_no += 1
    fig = plt.figure()
    plt.rcParams.update({'font.size': 8})
    fig.set_figheight(c.A4_short_in)
    fig.set_figwidth(c.A4_long_in)
    subplot_shape = (2, 4)

    ax_db_6 = plt.subplot2grid(
        shape=subplot_shape, loc=(0, 0), colspan=2, rowspan=1)
    ax_db_8 = plt.subplot2grid(
        shape=subplot_shape, loc=(0, 2), colspan=2, rowspan=1)

    ax_ang_6 = plt.subplot2grid(
        shape=subplot_shape, loc=(1, 0), colspan=2, rowspan=1)
    ax_ang_8 = plt.subplot2grid(
        shape=subplot_shape, loc=(1, 2), colspan=2, rowspan=1)

    axs = (ax_db_6, ax_db_8, ax_ang_6, ax_ang_8)

    sample_id = 'sample_N'
    print("++++++++++++++++++ plot_cor_no_f")
    db.cur.execute(f"""SELECT DISTINCT
                    {c.COL_KELVIN}
            FROM    {c.FILE_TABLE}
            WHERE {c.COL_SAMPLE_ID} = ?
            ORDER BY {c.COL_KELVIN}
            """, [sample_id])
    ax_num = -1
    for sel_kelvin in db.cur.fetchall():
        ax_num += 1
        kelvin = sel_kelvin[0]
        print(kelvin)
        matrix[kelvin] = {}
        db.cur.execute(f"""SELECT
                    {c.COL_MEMBER_FILE_NAME},
                    {c.COL_VGATE}
            FROM    {c.FILE_TABLE}
            WHERE {c.COL_KELVIN} = ? AND {c.COL_SAMPLE_ID} = ?
            ORDER BY {c.COL_VGATE} DESC
            """, [kelvin, sample_id])
        sel_file_vgates = db.cur.fetchall()
        matrix[kelvin]['Vg'] = []
        matrix[kelvin]['dB'] = []
        matrix[kelvin]['ang'] = []
        matrix[kelvin]['f'] = []
        matrix[kelvin]['rho_dB'] = []
        matrix[kelvin]['rho_ang'] = []

        for sel_file_vgate in sel_file_vgates:
            member_file_name = sel_file_vgate[0]
            print(member_file_name)
            vGate = sel_file_vgate[1]
            matrix[kelvin]['Vg'].append(vGate)
            matrix[kelvin]['dB'].append([])
            matrix[kelvin]['ang'].append([])
            csv = load_csv(member_file_name)
            f_Hz = csv['col1']
            dB = csv['col2']
            ang = csv['col3']
            for i in range(len(f_Hz)):
                matrix[kelvin]['dB'][-1].append(dB[i])
                matrix[kelvin]['ang'][-1].append(ang[i])
        for i in range(len(f_Hz)):
            matrix[kelvin]['f'].append(f_Hz[i]*1E-6)
            x_Vg = []
            y_dB = []
            y_ang = []
            for k in range(len(matrix[kelvin]['Vg'])):
                x_Vg.append(matrix[kelvin]['Vg'][k])
                y_dB.append(matrix[kelvin]['dB'][k][i])
                y_ang.append(matrix[kelvin]['ang'][k][i])
            rho_dB = np.corrcoef(x_Vg, y_dB)
            matrix[kelvin]['rho_dB'].append(rho_dB[0, 1])
            rho_ang = np.corrcoef(x_Vg, y_ang)
            matrix[kelvin]['rho_ang'].append(rho_ang[0, 1])

        axs[ax_num].plot(matrix[kelvin]['f'], matrix[kelvin]['rho_dB'])
        axs[ax_num].set(ylabel=r'$\rho_{A}$')

        axs[ax_num+2].plot(matrix[kelvin]['f'], matrix[kelvin]['rho_ang'])
        axs[ax_num+2].set(ylabel=r'$\rho_{\phi}$')

        axs[ax_num].title.set_text(f"Vg - Amplitude correlation, T={sel_kelvin[0]}")
        axs[ax_num+2].title.set_text(f"Vg - Pase correlation, T={sel_kelvin[0]}")

    for ax in axs:
        ax.grid()
        ax.set(xlabel='$f$, MHz')
        ax.set(xlim=[min(matrix[kelvin]['f']), max(matrix[kelvin]['f'])])
        ax.set(ylim=[-1, 1])

    plt.tight_layout()
#            plt.show()

    plt.savefig(f"{OUTFOLDER}/page{page_no}.pdf", dpi=c.DPI)
    plt.close()

    # print(matrix)
