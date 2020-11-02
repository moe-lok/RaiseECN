import cx_Oracle


def get_cust_order(lotId):
    print("getting customer order...")
    dsn_tns = cx_Oracle.makedsn('ADGTVMODS6.ad.analog.com', '1526', service_name='p2pll')
    conn = cx_Oracle.connect(user=r'long', password='PASSWD', dsn=dsn_tns)

    c = conn.cursor()

    c.execute("""
            SELECT
                plldba.actl.custordernumber
            FROM
                plldba.actl
            WHERE
                plldba.actl.lotid = '""" + lotId + """'""")  # use triple quotes if you want to spread your query across multiple lines

    row = c.fetchone()
    conn.close()

    if row is None:
        print("lot " + lotId + " does not exists...")
        return None
    else:
        print(row[0])
        return row[0]


def get_mfg_site(item):
    print("get mfg site...")
    cust_order = get_cust_order(item)
    if cust_order is not None:
        mfg_site = "AD" + cust_order.split('-')[0]
        return mfg_site

    return None


def main():
    print("main")
    items = []
    while True:  # taking multiple line input for tap stds
        line = input()

        if line == "done":
            break
        if line:
            if "not received at" in line and line.strip() in items:
                idx = items.index(line.strip())
                del items[idx:idx + 3]
                items.append(line.strip())
            else:
                items.append(line.strip())
            print(line)

    items = [i for i in items if i]# to remove empty strings in list
    print(items)
    print(len(items))

    parts = []
    lots = []
    mfg_sites = []

    str1 = ""

    for i, item in enumerate(items):
        if "Part =" in item:
            parts.append(item.split()[2])

        if "Lot " in item:
            lots.append(item.split()[1])

        if (i + 1) % 3 == 0:
            str1 += item + "\n" + "\n"
        else:
            str1 += item + "\n"

    f = open("output.txt", "w")
    f.write(str1)
    f.close()

    part_lot = dict(zip(parts, lots))

    for key in part_lot:
        mfg_sites.append(get_mfg_site(part_lot[key]))

    print(parts)
    print(lots)
    print(part_lot)
    print(mfg_sites, "\n")

    for i, part in enumerate(part_lot):
        print(part + "\t" + mfg_sites[i] + "\tadd supplier id\tADP2")


if __name__ == "__main__":
    main()
