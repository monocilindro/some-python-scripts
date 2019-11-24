import csv

filepath = '/home/theo/Desktop/P406_sfmuav_unregistered_group1_densified_point_cloud_part_15_info.txt'
plot_reference_table = '/home/theo/Desktop/plot_info_reference.csv'
with open(filepath) as f:
    for x in f:
        if "GTCitationGeoKey" in x:
            if "WGS 84" in x:
                wgs = "84"
            if "UTM zone 10N" in x:
                utm = "10n"
            if "UTM zone 11N" in x:
                utm = "11n"
            with open(plot_reference_table, 'a') as ref:
                ref_headers = ['wgs', 'utm']
                ref_row = [wgs, utm]
                writer = csv.DictWriter(ref, fieldnames=ref_headers)
                writer.writeheader()
                writer.writerow({'wgs' : wgs, 'utm' : utm})
            ref.close()
f.close()

