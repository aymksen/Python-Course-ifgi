# exercise_4_2.py

layer    = iface.activeLayer()
features = layer.selectedFeatures()

out_csv = os.path.join(folder, "SchoolReport.csv")

with open(out_path, 'w', encoding='utf-8') as f:
    f.write("Name;X;Y\n")
    for feat in features:
        name = feat["Name"]
        pt   = feat.geometry().asPoint()
        f.write(f"{name};{pt.x()};{pt.y()}\n")

print(f"Wrote {len(features)} records to {out_path}")
