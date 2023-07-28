import zipfile
import vcnst as c
import math
from matplotlib import pyplot as plt


class ZipSession:
    def __init__(self, zipfilename):
        self.zf = zipfile.ZipFile(zipfilename, "r")
        print('ZipFile opened')

    def __del__(self):
        self.zf.close()
        print('ZipFile closed')


zip = ZipSession('data_in/Jurim_5MHz_daksa.zip')

figwidth = c.MDPI_W_in
figheight = figwidth/math.sqrt(2)

fig = plt.figure()
plt.rcParams.update({'font.size': 7})
fig.set_figheight(figheight)
fig.set_figwidth(figwidth)
subplot_shape = (2, 4)
ax_db = plt.subplot2grid(shape=subplot_shape, loc=(0, 0), colspan=2, rowspan=1)
ax_res = plt.subplot2grid(
    shape=subplot_shape, loc=(0, 2), colspan=2, rowspan=1)


for member_file_name in zip.zf.namelist():
    legend = None

    if '2_5mhz_ppms_100K' in member_file_name:
        legend = "100 K"
    elif '1_5mhz_ppms_300K' in member_file_name:
        legend = "300 K"
    elif '3_5mhz_ppms_50K' in member_file_name:
        legend = "50 K"
    elif '6_5mhz_ppms_bez_tran_3.9K' in member_file_name:
        legend = "3.9 K (no amp.)"
        continue
    elif '5_5mhz_ppms_4.2K' in member_file_name:
        legend = "4.2 K"

    else:
        print(f"member_file_name = {member_file_name}")

    if legend is not None:
        file_contents = zip.zf.read(member_file_name)
        file_lines = file_contents.decode('ascii').splitlines()
        freq, db, ang = [], [], []
        for full_line in file_lines:
            #        print(full_line)
            line = full_line.strip(" \t\n\r")
            if '#' in line:
                continue
            if 'freq' in line:
                continue
            fields = line.split('\t')
            if len(fields) == 3:
                freq.append(float(fields[0].replace(",", "."))/1e6)
                db.append(float(fields[1].replace(",", ".")))
                ang.append(float(fields[2].replace(",", ".")))
        ax_db.plot(freq, db, label=legend)

ax_db.set(xlim=[4.990, 5.005])
ax_db.xaxis.set_ticks([4.990, 4.995, 5.000, 5.005])
ax_db.set(xlabel='$f$, MHz')
ax_db.set(ylabel='A, dB')
#ax_db.legend(loc='center left', bbox_to_anchor=(1.02, 0.43))
ax_db.legend(loc='best', handlelength=1)

ax_db.grid()

for n in range(6):
    ax_res._get_lines.get_next_color()


zipres = ZipSession('data_in/8K_with_wire_with_20kohm.zip')
for member_file_name in zipres.zf.namelist():
    legend = None

    if '082_supp15V_U' in member_file_name:
        legend = "resistor"
    elif 'sample_8K_wit' in member_file_name:
        continue
    elif '027_supp15V_Ug0p0V_Ig_Usd_0p0' in member_file_name:
        legend = "nanowire"

    else:
        print(f"member_file_name = {member_file_name}")
    if legend is not None:
        file_contents = zipres.zf.read(member_file_name)
        file_lines = file_contents.decode('ascii').splitlines()
        freq, db, ang = [], [], []
        for full_line in file_lines:
            #        print(full_line)
            line = full_line.strip(" \t\n\r")
            if '#' in line:
                continue
            if 'freq' in line:
                continue
            fields = line.split('\t')
            if len(fields) == 3:
                freq.append(float(fields[0].replace(",", "."))/1e6)
                db.append(float(fields[1].replace(",", ".")))
                ang.append(float(fields[2].replace(",", ".")))
        ax_res.semilogx(freq, db, label=legend)

#ax_db.set(xlim=[4.990, 5.005])
# ax_db.xaxis.set_ticks([4.990,4.995,5.000,5.005])
ax_res.xaxis.set_ticks([0.5, 1, 2, 5, 10])
ax_res.xaxis.set_major_formatter('{x}')
ax_res.set(xlim=[min(freq), 10])
ax_res.set(xlabel='$f$, MHz')
ax_res.set(ylabel='A, dB')
#ax_db.legend(loc='center left', bbox_to_anchor=(1.02, 0.43))
ax_res.legend(loc='best', handlelength=1)

ax_res.grid()

titles = ['(a)', '(b)']
ntitle = 0
for ax in [ax_db, ax_res]:
    ax.set_title(titles[ntitle], x=-0.19, y=1.0, pad=-11, fontweight='bold')
    ntitle += 1

plt.tight_layout()


plt.savefig(f"kvarcs_rezisto.pdf", dpi=c.DPI)
plt.close()
