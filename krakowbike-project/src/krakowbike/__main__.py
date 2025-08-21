import argparse

from jinja2 import Environment, FileSystemLoader

from src.krakowbike.analyze_data import (
    calculate_basic_statistics,
    calculate_seasonal_trends,
    calculate_weather_correlations,
    weather_summary,
)
from src.krakowbike.load_data import load_air_data, load_bike_data, \
    load_weather_data
from src.krakowbike.preprocess_data import preprocess_dataset
from src.krakowbike.visualize_data import (
    plot_correlation_matrix,
    plot_total_daily_traffic,
    visualize_seasonal_traffic,
    visualize_weather_impact,
)


def generate_data_for_html_report(
        project_path: str, start_date: str = "2017-01-01",
        end_date: str = "2021-12-31"
) -> dict:
    path_to_data = f"{project_path}/krakow_data"
    df = preprocess_dataset(
        load_air_data(path_to_data),
        load_bike_data(path_to_data),
        load_weather_data(path_to_data),
        start_date=start_date,
        end_date=end_date,
    )
    basic_statistics = calculate_basic_statistics(df, for_html=True)
    weather_dict = weather_summary(df, for_html=True)
    seasonal_dict = calculate_seasonal_trends(df, for_html=True)
    weather_corrs = calculate_weather_correlations(df)
    daily_traffic_plot = plot_total_daily_traffic(df, save_plot=True)
    correlations_matrix = plot_correlation_matrix(df, save_plot=True)
    seasonal_traffic_plot = visualize_seasonal_traffic(df, save_plot=True)
    weather_plot = visualize_weather_impact(df, save_plot=True)
    data = {
        "basic_statistics": basic_statistics,
        "weather_dict": weather_dict,
        "seasonal_dict": seasonal_dict,
        "weather_corrs": weather_corrs,
        "daily_traffic_plot": daily_traffic_plot,
        "correlations_matrix": correlations_matrix,
        "seasonal_traffic_plot": seasonal_traffic_plot,
        "weather_plot": weather_plot,
    }
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--project_path",
        help="Path to the `krakowbike` project directory.",
        default="./krakowbike-project",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        help="Path to the directory in which report should be created.",
    )
    parser.add_argument(
        "-r",
        "--report_name",
        help="Name of the report file.",
        default="krakow_bike_report",
    )
    parser.add_argument(
        "-s",
        "--start_date",
        help="Start date of analyzed period.",
        default="2017-01-01",
    )
    parser.add_argument(
        "-e",
        "--end_date",
        help="",
        default="2021-12-31",
    )
    args = parser.parse_args()

    environment = Environment(
        loader=FileSystemLoader(f"{args.project_path}/templates"))
    template = environment.get_template("report.html")
    krakow_data = generate_data_for_html_report(
        args.project_path, args.start_date, args.end_date
    )

    content = template.render(krakow_data)
    report_path = f"{args.output_dir}/{args.file_name}.html"
    with open(report_path, mode="w", encoding="utf-8") as report:
        report.write(content)
        print(
            f"Created {args.file_name}.html report in {args.output_dir} directory.")


if __name__ == "__main__":
    main()
