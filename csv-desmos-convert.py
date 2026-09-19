import csv

def export_desmos_lists(
    csv_path: str,
    y_field: str,
    x_fields: list[str],
    output_path: str
):
    # Read CSV data
    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        all_headers = [h.strip() for h in reader.fieldnames]
        
        # Verify requested columns exist
        needed_fields = [y_field] + x_fields
        missing = [col for col in needed_fields if col not in all_headers]
        if missing:
            raise ValueError(f"Columns not found in CSV: {missing}")

        data = {col: [] for col in needed_fields}
        for row in reader:
            for col in needed_fields:
                val = row[col].strip()
                try:
                    num = float(val) if "." in val else int(val)
                    data[col].append(str(num))
                except ValueError:
                    data[col].append("NaN")  # Keeps list indices aligned

    lines = []

    # Format Fixed Y-Axis List
    y_vals = ", ".join(data[y_field])
    lines.append(f"Y = [{y_vals}]")
    lines.append("")

    # Format Candidate X-Axis Lists
    piecewise_cases = []
    labels = []

    for idx, col in enumerate(x_fields, start=1):
        x_vals = ", ".join(data[col])
        lines.append(f"X_{idx} = [{x_vals}]")
        piecewise_cases.append(f"s = {idx}: X_{idx}")
        labels.append(f"{idx}: {col}")

    # Generate Desmos expressions for switching and regression
    lines.append("")
    lines.append(f"s = 1")
    lines.append(f"X = {{{', '.join(piecewise_cases)}}}")
    lines.append("(X, Y)")
    lines.append("Y ~ m*X + b")

    # Write output to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Generated Desmos list definitions for {len(x_fields)} features in '{output_path}'.")


# Example Configuration for auto.csv:
filename = "auto_mpg"

export_desmos_lists(
    csv_path=f"{filename}.csv",
    y_field="mpg",
    x_fields=[
        "cylinders",
        "displacement",
        "horsepower",
        "weight",
        "acceleration",
        "model year"
    ],
    output_path=f"desmos/{filename}.txt"
)