import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.krakowbike.utils import AIR_COLUMN, MONTH_TO_SEASON, STREET_NAMES, save_plot_as_base64


def plot_total_daily_traffic(df: pd.DataFrame, save_plot: bool = False) -> str:
    """

    :param df:
    :param save_plot:
    :return:
    """
    plt.figure(figsize=(15, 10))
    sns.lineplot(x=df.index, y=df["total_daily_traffic"])
    plt.title("Total daily traffic")
    plt.grid()
    plt.ylim(0, None)
    if save_plot:
        return save_plot_as_base64()
    plt.show()
    return ""


def plot_correlation_matrix(df: pd.DataFrame, save_plot: bool = False) -> str:
    """

    :param df:
    :param save_plot:
    :return:
    """
    plt.figure(figsize=(15, 15))
    cols = [col for col in df.columns if not col in STREET_NAMES]
    sns.heatmap(df[cols].corr(), annot=True, cmap='Blues', vmin=-1, vmax=1, )
    plt.title("Correlation matrix")
    if save_plot:
        return save_plot_as_base64()
    plt.show()
    return ""


def visualize_seasonal_traffic(df: pd.DataFrame, save_plot: bool = False) -> str:
    """

    :param df:
    :param save_plot:
    :return:
    """
    df["month"] = df.index.month_name()
    df["day_of_week"] = df.index.day_name()
    df["season"] = df["month"].map(MONTH_TO_SEASON)

    fig, axes = plt.subplots(3, 1, figsize=(15, 15))
    plt.suptitle("Violin plots of seasonal traffic")
    periods = ["month", "day_of_week", "season"]
    for i, period in enumerate(periods):
        ax = axes[i % 3]
        sns.violinplot(data=df, x=period, y="total_daily_traffic", ax=ax, legend=False)
        ax.set_title(period)
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.grid()
    if save_plot:
        return save_plot_as_base64()
    plt.show()
    return ""


def visualize_weather_impact(df: pd.DataFrame, save_plot: bool = False) -> list[str]:
    """

    :param df:
    :param save_plot:
    :return:
    """
    plots = []
    factors = [
        "Średnia temperatura dobowa [°C]",
        "Suma dobowa opadów [mm]",
        AIR_COLUMN,
    ]
    for i, factor in enumerate(factors):
        sns.jointplot(data=df, x="total_daily_traffic", y=factor)
        plt.grid()
        if save_plot:
            plots.append(save_plot_as_base64())
        else:
            plt.show()

    return plots
