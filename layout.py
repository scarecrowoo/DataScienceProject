import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Beispiel-Daten
df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Values': [10, 15, 7, 20]
})

# Homepage Layout
homepage = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Willkommen zu unserem Forschungsprojekt", style={"color": "#9b0a7d"})),
        dbc.Col(html.P("Diese Website präsentiert interaktive Visualisierungen und Einblicke in unsere Forschungsfragen zum Einfluss von ChatGPT auf wissenschaftliche Arbeiten.")),
    ], className="mt-4"),
    dbc.Row([
        dbc.Col(html.P("Navigiere durch die verschiedenen Forschungsfragen, um mehr zu erfahren!"))
    ])
])

# Layout für Forschungsfrage 1: Veränderung der Wortverwendung
page1_layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("Frage 1: Veränderung der Wortverwendung", style={"color": "#9b0a7d"}))),
    dbc.Row(dbc.Col(html.P("Wie hat sich die Verwendung bestimmter Wörter in wissenschaftlichen Arbeiten seit der Einführung von ChatGPT verändert?"))),
    dbc.Row([
        dbc.Col(dcc.Graph(
            id="rq1-graph",
            figure=px.bar(df, x="Category", y="Values", title="Kategoriehäufigkeiten")
        )),
    ]),
    dbc.Row(dbc.Col(html.P("Diese Grafik zeigt die Häufigkeiten bestimmter Wörter im Zeitverlauf."))),
])

# Layout für Forschungsfrage 2: Veränderung der Fragewörter
page2_layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("Frage 2: Veränderung der Fragewörter", style={"color": "#9b0a7d"}))),
    dbc.Row(dbc.Col(html.P("Welche Veränderungen gibt es in der Nutzung von Fragewörtern in wissenschaftlichen Arbeiten seit der Einführung von ChatGPT?"))),
    dbc.Row([
        dbc.Col(dcc.Graph(
            id="rq2-graph",
            figure=px.pie(df, names="Category", values="Values", title="Verteilung von Fragewörtern")
        )),
    ]),
    dbc.Row(dbc.Col(html.P("Diese Visualisierung zeigt die Verteilung von Fragewörtern in wissenschaftlichen Arbeiten."))),
])

# Layout für Forschungsfrage 3: Satzlängen in wissenschaftlichen Arbeiten
page3_layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("Frage 3: Satzlängen in wissenschaftlichen Arbeiten", style={"color": "#9b0a7d"}))),
    dbc.Row(dbc.Col(html.P("Wie haben sich die Satzlängen in wissenschaftlichen Arbeiten seit der Einführung von ChatGPT verändert?"))),
    dbc.Row([
        dbc.Col(dcc.Graph(
            id="rq3-graph",
            figure=px.line(df, x="Category", y="Values", title="Satzlängen im Zeitverlauf")
        )),
    ]),
    dbc.Row(dbc.Col(html.P("Diese Grafik zeigt die Veränderung der Satzlängen über die Zeit."))),
])

# Bereits bestehende Layouts (Homepage, Frage 1-3)

# Layout für Forschungsfrage 4: Unterschiede zwischen Abstracts und vollständigen Texten
page4_layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("Frage 4: Unterschiede zwischen Abstracts und vollständigen Texten", style={"color": "#9b0a7d"}))),
    dbc.Row(dbc.Col(html.P("Untersuchung, ob es Unterschiede in der sprachlichen Gestaltung zwischen Abstracts und den vollständigen Texten wissenschaftlicher Arbeiten gibt."))),
    # Hier könnten interaktive Visualisierungen oder Analysen eingefügt werden
])

# Layout für Forschungsfrage 5: Vergleich CAU vs. andere Universitäten
page5_layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("Frage 5: Vergleich zwischen CAU und anderen deutschen Universitäten", style={"color": "#9b0a7d"}))),
    dbc.Row(dbc.Col(html.P("Vergleich der vermeintlichen Beeinflussung durch ChatGPT zwischen der Christian-Albrechts-Universität zu Kiel (CAU) und anderen deutschen Universitäten."))),
    # Weitere Analysen oder Visualisierungen können hier eingefügt werden
])

# Layout für Forschungsfrage 6: Vergleich zwischen Fakultäten der CAU
page6_layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("Frage 6: Vergleich der Wortwahl zwischen Fakultäten der CAU", style={"color": "#9b0a7d"}))),
    dbc.Row(dbc.Col(html.P("Untersuchung der Veränderungen in der Wortwahl zwischen verschiedenen Fakultäten der CAU seit der Einführung von ChatGPT."))),
    # Hier könnten Visualisierungen zum Vergleich der Fakultäten ergänzt werden
])

# Layout für Forschungsfrage 7: Vergleich globaler Universitäten
page7_layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("Frage 7: Unterschiede zwischen Universitäten weltweit", style={"color": "#9b0a7d"}))),
    dbc.Row(dbc.Col(html.P("Unterschiede zwischen verschiedenen Universitäten weltweit hinsichtlich der vermeintlichen Beeinflussung durch ChatGPT."))),
    # Hier könnten Vergleichsanalysen zwischen globalen Universitäten hinzugefügt werden
])

# Layout für den Imprint-Bereich
imprint_layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("Kontakt", style={"color": "#9b0a7d"}))),
    dbc.Row(dbc.Col(html.P("Autor: [Louis Krückmeyer, Matheus Kolzarek, Tom Skrzynski-Fox]"))),
    dbc.Row(dbc.Col(html.P("Gruppe: [Joule im Pool]"))),
])

# Layout für die restlichen Fragen kannst du analog hinzufügen...
