import base64
import io

import matplotlib.pyplot as plt

AIR_COLUMN = "Kraków - ul. Złoty Róg (pył zawieszony PM10 [jednostka ug/m3])"

STREET_NAMES = [
    "Armii Krajowej",
    "Bora-Komorowskiego",
    "Bulwary",
    "Dworzec Główny",
    "Grzegórzecka",
    "Kamieńskiego",
    "Klimeckiego",
    "Kopernika",
    "Kotlarska",
    "Mogilska",
    "Monte Cassino",
    "Niepołomska",
    "Nowohucka",
    "Smoleńsk",
    "Tyniecka",
    "Wadowicka",
    "Wielicka",
]

MONTH_TO_SEASON = {
    "December": "Winter",
    "January": "Winter",
    "February": "Winter",
    "March": "Spring",
    "April": "Spring",
    "May": "Spring",
    "June": "Summer",
    "July": "Summer",
    "August": "Summer",
    "September": "Autumn",
    "October": "Autumn",
    "November": "Autumn",
}


def save_plot_as_base64() -> str:
    """
    Convert current matplotlib plot to base64 encoded string.

    Saves the current plot as PNG image in memory and converts it to
    base64 format for embedding in HTML or web applications.

    :return: Base64 encoded string of the plot image
    """
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png", transparent=True)
    buffer.seek(0)
    plot_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()
    return plot_base64
