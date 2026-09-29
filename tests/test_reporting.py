import pandas as pd

from order_report.reporting import write_reports


def test_files_are_saved_and_folder_is_created(tmp_path):
    reports = {"a": pd.DataFrame({"x": [1, 2]}), "b": pd.DataFrame({"y": [3]})}
    output_dir = tmp_path / "ny_mapp" / "under"

    saved = write_reports(reports, output_dir)

    assert [path.name for path in saved] == ["a.csv", "b.csv"]
    assert pd.read_csv(output_dir / "a.csv")["x"].tolist() == [1, 2]
