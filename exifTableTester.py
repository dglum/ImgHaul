import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import exifread

paths = ["H:\Dev\ImgHaul\DSC_6236.JPG", "H:\Dev\ImgHaul\DSC_6927.JPG", "H:\Dev\ImgHaul\DSC_7855.JPG"]
mm = {}

for file in paths:
    f = open(file, 'rb')
    tags = exifread.process_file(f)
    if len(tags) == 0:
        break
    elif tags["EXIF FocalLength"] not in mm.keys():
        mm[int(str(tags["EXIF FocalLength"]))] = 1
    else:
        mm[int(str(tags["EXIF FocalLength"]))] += 1
      
fig, ax = plt.subplots() 

plt.xlabel("Focal Length in mm", fontsize=12)
plt.ylabel("Occurrences", fontsize=12)
plt.title("Focal Length Distribution", fontsize=16)

ax.bar(mm.keys(), mm.values())
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()



