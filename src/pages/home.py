from datetime import datetime
import flet as ft
from api import get_weather, get_forecast, ICON_URL
from state import state


def home_view(page: ft.Page) -> ft.View:
    result = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    city_field = ft.TextField(label="Enter city name", value=state["city"], expand=True)

    def render():
        result.controls.clear()
        if not state["city"]:
            return

        units = state["units"]
        temp_unit = "°C" if units == "metric" else "°F"
        wind_unit = "m/s" if units == "metric" else "mph"

        weather = get_weather(state["city"], units)
        if not weather["ok"]:
            result.controls.append(
                ft.Text(weather["error"], color=ft.Colors.RED_400, size=18)
            )
            return

        forecast = get_forecast(state["city"], units)
        tiles = []
        if forecast["ok"]:
            for day in forecast["days"]:
                name = datetime.strptime(day["date"], "%Y-%m-%d").strftime("%a")
                tiles.append(
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                        controls=[
                            ft.Text(name, weight=ft.FontWeight.BOLD),
                            ft.Image(src=ICON_URL.format(day["icon"]), width=50, height=50),
                            ft.Text(f"{day['temp']}{temp_unit}"),
                        ],
                    )
                )

        result.controls.extend(
            [
                ft.Text(weather["city"], size=26, weight=ft.FontWeight.W_500),
                ft.Image(src=ICON_URL.format(weather["icon"]), width=110, height=110),
                ft.Text(f"{weather['temp']}{temp_unit}", size=56, weight=ft.FontWeight.BOLD),
                ft.Text(weather["description"], size=18),
                ft.Container(height=10),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        ft.Text(f"Humidity: {weather['humidity']}%"),
                        ft.Text(f"Wind: {weather['wind']} {wind_unit}"),
                    ],
                ),
                ft.Container(height=20),
                ft.Text("5-Day Forecast", size=18, weight=ft.FontWeight.BOLD),
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=tiles),
            ]
        )

    def search(e):
        state["city"] = city_field.value.strip()
        render()
        page.update()

    async def go_settings(e):
        await page.push_route("/settings")

    city_field.on_submit = search
    render()

    return ft.View(
        route="/",
        scroll=ft.ScrollMode.AUTO,
        appbar=ft.AppBar(
            title=ft.Text("Weather App"),
            center_title=True,
            actions=[ft.IconButton(icon=ft.Icons.SETTINGS, on_click=go_settings)],
        ),
        controls=[
            ft.Row([city_field, ft.IconButton(icon=ft.Icons.SEARCH, on_click=search)]),
            result,
        ],
    )