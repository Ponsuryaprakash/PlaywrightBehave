import json
import os


def generate_html_report(json_path, output_path, template_path):
    with open(json_path, "r", encoding="utf-8") as f:
        report_data = json.load(f)

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    final_html = template.replace("{{DATA}}", json.dumps(report_data))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"\nHTML Report generated at: {os.path.abspath(output_path)}")