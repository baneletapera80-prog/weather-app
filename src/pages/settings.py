import flet as ft
from state import state


def settings_view(page: ft.Page) -> ft.View:
    async def go_home(e):
        await page.push_route("/")

    def toggle(e):
        state["units"] = "imperial" if e.control.value else "metric"

    return ft.View(
        route="/settings",
        appbar=ft.AppBar(
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=go_home),
            title=ft.Text("Settings"),
            center_title=True,
        ),
        controls=[
            ft.Switch(
                label="Use Fahrenheit and mph",
                value=state["units"] == "imperial",
                on_change=toggle,
            )
        ],
    )