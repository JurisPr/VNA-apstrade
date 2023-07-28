import zipfile
import vcnst as c
import math
from matplotlib import pyplot as plt
import matplotlib.cm as cm


class ZipSession:
    def __init__(self, zipfilename):
        self.zf = zipfile.ZipFile(zipfilename, "r")
        print('ZipFile opened')

    def __del__(self):
        self.zf.close()
        print('ZipFile closed')


zip = ZipSession('data_in/atk_no_temp.zip')

figwidth = c.MDPI_W_in
figheight = figwidth/math.sqrt(2)

fig = plt.figure()
plt.rcParams.update({'font.size': 7})
fig.set_figheight(figheight)
fig.set_figwidth(figwidth)
subplot_shape = (2, 4)
ax_db = plt.subplot2grid(shape=subplot_shape, loc=(0, 0), colspan=2, rowspan=1)
ax_temp = plt.subplot2grid(shape=subplot_shape, loc=(0, 2), colspan=2, rowspan=1)


gudspec = []

for member_file_name in zip.zf.namelist():
    legend = None
    temp_K = None

    if '120_supp15V_Ug0p0V_Usd_0p05V_po0_200K' in member_file_name:
        legend = "200 K"
        temp_K = 200
    elif '150_supp15V_Ug0p0V_Usd_0p05V_po0_300K' in member_file_name:
        legend = "300 K"
        temp_K = 300
    elif '133_supp15V_Ug0p0V_Usd_0p05V_po0_250K' in member_file_name:
        legend = "250 K"
        temp_K = 250
    elif '109_supp15V_Ug0p0V_Usd_0p05V_po0_150K' in member_file_name:
        legend = "150 K"
        temp_K = 150
    elif '164_supp15V_Ug0p0V_Usd_0p05V_po0_100' in member_file_name:
        legend = "100 K"
        temp_K = 100

    elif '004_supp15V_Ug0V_Usd_0p05V_po0_5K' in member_file_name:
        legend = "5 K"
        temp_K = 5

    elif '016_supp15V_Ug0p0V_Usd_0p05V_po0_5p8K_bck' in member_file_name:
        continue
        legend = "5.8 K"
        temp_K = 5.8
    elif '029_supp15V_Ug0V_Usd_0p05V_po0_10K' in member_file_name:
        
        legend = "10 K"
        temp_K = 10
    elif '042_supp15V_Ug0V_Usd_0p05V_po0_15K' in member_file_name:
        legend = "15 K"
        temp_K = 15
    elif '055_supp15V_Ug0V_Usd_0p05V_po0_30K' in member_file_name:
        legend = "30 K"
        temp_K = 30
    elif '068_supp15V_Ug0V_Usd_0p05V_po0_50K' in member_file_name:
        continue
        legend = "50 K"
        temp_K = 50
    elif '079_supp15V_Ug0V_Usd_0p05V_po0_70K' in member_file_name:
        legend = "70 K"
        temp_K = 70
    elif '096_supp15V_Ug0p0V_Usd_0p05V_po0_100K' in member_file_name:
        continue
        legend = "100 K"
        temp_K = 100

    elif '148_supp15V_Ug0p0V_Usd_0p05V_po0_290K_Isg_0p1nA' in member_file_name:
        continue
        legend = "290 K"
        temp_K = 290

    elif '149_supp15V_Ug0p0V_Usd_0p05V_po0_295K_Isg_0p1nA' in member_file_name:
        continue
        legend = "295 K"
        temp_K = 295

    elif '161_supp15V_Ug0p0V_Usd_0p0V_po0_180K_ISD_' in member_file_name:
        continue
        legend = "180 K"
        temp_K = 180

    elif '162_supp0V_Ug0p0V_Usd_0p0V_po0_150K_ISD_' in member_file_name:
        continue

    elif '163_supp0V_Ug0p0V_Usd_0p0V_po-40_150K_ISD_.csv' in member_file_name:
        continue

    elif '165_supp15V_Ug0p0V_Usd_0p05V_po0_80K_ISD_0p34uQ.csv' in member_file_name:
        legend = "80 K"
        temp_K = 80

    elif '166_supp15V_Ug0p0V_Usd_0p05V_po0_50K_ISD_0p28uQ.csv' in member_file_name:
        legend = "50 K"
        temp_K = 50

    elif '167_supp15V_Ug0p0V_Usd_0p05V_po0_30K_ISD_0p25uA.csv' in member_file_name:
        continue
        legend = "30 K"
        temp_K = 30

    elif '168_supp15V_Ug0p0V_Usd_0p05V_po0_5p3K_ISD_0p26uA.csv' in member_file_name:
        continue
        legend = "5.3 K"
        temp_K = 5.3

    elif '169_supp15V_Ug0p0V_Usd_0p05V_po0_4p7K' in member_file_name:
        continue
        legend = "4.7 K"
        temp_K = 4.7
    else:
        print(f"member_file_name = {member_file_name}")

    if legend is not None:
        spec_info = [temp_K, member_file_name, legend]
        gudspec.append(spec_info)

gudspec.sort(reverse=True)
peak_T, peak_f = [], []
for spec in gudspec:
    temp_K = spec[0]
    member_file_name = spec[1]
    legend = spec[2]

    file_contents = zip.zf.read(member_file_name)
    file_lines = file_contents.decode('ascii').splitlines()
    freq, db, ang = [], [], []
    freq_subset, db_subset = [], []
    for full_line in file_lines:
        #        print(full_line)
        line = full_line.strip(" \t\n\r")
        if '#' in line:
            continue
        if 'freq' in line:
            continue
        fields = line.split('\t')
        if len(fields) == 3:
            f = float(fields[0].replace(",", "."))/1e6
            d = float(fields[1].replace(",", "."))
            a = float(fields[2].replace(",", "."))
            freq.append(f)
            db.append(d)
            ang.append(a)
            if f > 0.5 and f < 2:
                freq_subset.append(f)
                db_subset.append(d)

    ax_db.semilogx(freq, db, label=legend, linewidth=0.5,
                   color=cm.jet(temp_K/300))
#    ax_db.semilogx(freq_subset, db_subset, linewidth=1,
    # color=cm.jet(temp_K/300))

    i = db_subset.index(min(db_subset))

    ax_db.semilogx(freq_subset[i], db_subset[i], '.',
                   color=cm.jet(temp_K/300))
    peak_T.append(temp_K)
    peak_f.append(freq_subset[i])

ax_temp.plot(peak_T,peak_f,'.')
ax_temp.grid()

ax_db.set(ylim=[-60, -10])
ax_db.set(xlim=[0.1, 10])
# ax_db.xaxis.set_ticks([4.990,4.995,5.000,5.005])
ax_db.xaxis.set_major_formatter('{x}')
ax_db.set(xlabel='$f$, MHz')
ax_db.set(ylabel='A, dB')
ax_db.legend(loc='center left', bbox_to_anchor=(1.02, 0.43))
#ax_db.legend(loc='best', handlelength=1)

ax_db.grid()

# plt.tight_layout()
plt.savefig(f"tempera.pdf", dpi=c.DPI)
plt.close()
