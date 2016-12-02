#!/env/bin python

filename = "vsfm_cm_dim_1D.gcp"
with(open(filename, "r")) as fn:
    content = fn.readlines()
    for line in content:
        lst = line.strip().split()
        lst[1] = str(round(float(lst[1]) + 1006290000, 2))
        lst[2] = str(round(float(lst[2]) - 467520000, 2))
        lst[3] = str(round(float(lst[3]) - 60400, 2))
        print(" ".join(lst))
