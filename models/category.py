from enum import Enum


class ValuesMixin:
    @classmethod
    def values(cls):
        return list(map(lambda c: c.value, cls))


class Category(ValuesMixin, Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"

    @property
    def subcategories(self):
        return SUBCATEGORIES[self]


class Subcategory(ValuesMixin, Enum):
    SQL = "sql"
    ASP = "asp.net"
    NODE_JS = "nodejs"
    RASPBERRY_PI = "raspberry-pi"
    HTML = "html"
    CSS = "css"
    JAVASCRIPT = "javascript"
    REACT = "reactjs"

    @property
    def link(self):
        return LINKS[self]


SUBCATEGORIES = {
    Category.BACKEND: [
        Subcategory.SQL,
        Subcategory.ASP,
        Subcategory.NODE_JS,
        Subcategory.RASPBERRY_PI,
    ],
    Category.FRONTEND: [
        Subcategory.HTML,
        Subcategory.CSS,
        Subcategory.JAVASCRIPT,
        Subcategory.REACT,
    ],
}

LINKS = {
    Subcategory.SQL: "https://www.w3schools.com/sql/default.asp",
    Subcategory.ASP: "https://www.w3schools.com/asp/default.asp",
    Subcategory.NODE_JS: "https://www.w3schools.com/nodejs/default.asp",
    Subcategory.RASPBERRY_PI: "https://www.w3schools.com/nodejs/nodejs_raspberrypi.asp",
    Subcategory.HTML: "https://www.w3schools.com/html/default.asp",
    Subcategory.CSS: "https://www.w3schools.com/css/default.asp",
    Subcategory.JAVASCRIPT: "https://www.w3schools.com/js/default.asp",
    Subcategory.REACT: "https://www.w3schools.com/react/default.asp",
}
