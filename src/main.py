import flet as ft
from pages.home import home_view
from pages.settings import settings_view

ROUTES = {
    "/": home_view,
    "/settings": settings_view,
}


def main(page: ft.Page):
    page.title = "Weather App"
    page.window.width = 420
    page.window.height = 700

    def route_change():
        page.views.clear()
        page.views.append(home_view(page))

        if page.route != "/" and page.route in ROUTES:
            page.views.append(ROUTES[page.route](page))

        page.update()

    async def view_pop(e):
        page.views.pop()
        await page.push_route(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change()


ft.run(main)