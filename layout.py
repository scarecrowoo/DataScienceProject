import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import pandas as pd
import re
from collections import Counter
from scipy.stats import mannwhitneyu

# --- Example CSV data for other sections (you can replace this with your actual data) ---
df_word_usage = pd.DataFrame({
    'Year': ['2020', '2021', '2022'],
    'Word_Count': [100, 150, 200],
    'Word_Type': ['Technical', 'Non-Technical', 'Mixed']
})

df_sentence_length = pd.DataFrame({
    'Year': ['2020', '2021', '2022'],
    'Avg_Sentence_Length': [12.5, 13.0, 14.0]
})

df_asia_data = pd.DataFrame({
    'Year': ['2020', '2021', '2022'],
    'Keyword_Count': [1200, 1300, 1500]
})

# --- Research Question 2 Data and Analysis ---
# Load your data here by replacing 'your_data.csv' with the actual file path
df = pd.read_csv('your_data.csv')  # <-- INSERT YOUR FILE PATH HERE

# Process the data
df = df.dropna(subset=['Abstract', 'Publication_year'])
df['Publication_year'] = df['Publication_year'].astype(int)

# Define question words
question_words = ['what', 'why', 'how', 'where', 'when', 'which', 'who', 'whom', 'whose']

# Function to count question words
def count_question_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    count = sum(1 for word in words if word in question_words)
    return count

df['Question_Word_Count'] = df['Abstract'].apply(count_question_words)
df['Question_Mark_Count'] = df['Abstract'].apply(lambda x: x.count('?'))

# Split data into periods
df_before_2023 = df[df['Publication_year'] < 2023]
df_after_2023 = df[df['Publication_year'] >= 2023]

# Mann-Whitney U test for question words
stat, p_value = mannwhitneyu(df_before_2023['Question_Word_Count'], df_after_2023['Question_Word_Count'])

# Mann-Whitney U test for question marks
stat_qm, p_value_qm = mannwhitneyu(df_before_2023['Question_Mark_Count'], df_after_2023['Question_Mark_Count'])

# Prepare data for plot
data_for_plot = pd.concat([
    df_before_2023.assign(Period='Before 2023'),
    df_after_2023.assign(Period='2023 and After')
])

# Create visualizations for Research Question 2
fig_question_words = px.box(
    data_for_plot,
    x='Period',
    y='Question_Word_Count',
    title='Verteilung der Fragewörter vor und nach 2023',
    labels={'Question_Word_Count': 'Anzahl der Fragewörter'}
)

fig_question_marks = px.box(
    data_for_plot,
    x='Period',
    y='Question_Mark_Count',
    title='Verteilung der Fragezeichen vor und nach 2023',
    labels={'Question_Mark_Count': 'Anzahl der Fragezeichen'}
)

# --- Home Section (Intro and overview) ---
homepage = html.Div(id="start", children=[
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to our Data Science Project!", style={"color": "#9b0a7d"}), className="mt-5"),
        ]),
        dbc.Row([
            dbc.Col(html.P(
                "Below, you'll find a series of research questions exploring the impact of ChatGPT on scientific papers."
            )),
        ]),
    ], className="py-5")
])

# --- Projects Section now contains research questions and actual data visualizations ---
projects_section = html.Div(id="projects", children=[
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Research Questions", style={"color": "#9b0a7d"}), className="mt-5 mb-4 text-center"),
        ]),

        # Research Question 1: Changes in Word Usage
        dbc.Row([
            dbc.Col(html.H4("Research Question 1: Changes in Word Usage in Scientific Papers"), width=6),
            dbc.Col(html.P(
                "How has the usage of specific words in scientific papers changed since the introduction of ChatGPT? "
                "This analysis aims to identify whether certain terms have become more or less frequent."
            )),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(
                id="word-usage-graph",
                figure=px.bar(df_word_usage, x="Year", y="Word_Count", color="Word_Type",
                              title="Word Usage Over Time by Type")
            )),
        ], className="mb-5"),

        # Research Question 2: Changes in the Use of Question Words
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H2("Research Question 2: Changes in the Use of Question Words", style={"color": "#9b0a7d"}), width=12),
            ], className="mt-5 mb-4 text-center"),
            dbc.Row([
                dbc.Col(html.P(
                    "Welche Veränderungen gibt es in der Verwendung von Fragewörtern (z.B. was, warum) in wissenschaftlichen Arbeiten seit der Einführung von ChatGPT? "
                    "Dieser Abschnitt untersucht die Häufigkeit von Fragewörtern vor und nach 2023."
                ), width=12),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(
                    id="question-words-graph",
                    figure=fig_question_words
                ), width=6),
                dbc.Col(dcc.Graph(
                    id="question-marks-graph",
                    figure=fig_question_marks
                ), width=6),
            ]),
            dbc.Row([
                dbc.Col(html.P(f"Mann-Whitney U Test p-Wert für Fragewörter: {p_value:.4f}"), width=6),
                dbc.Col(html.P(f"Mann-Whitney U Test p-Wert für Fragezeichen: {p_value_qm:.4f}"), width=6),
            ], className="mt-3"),
        ], className="mb-5"),

        # Research Question 3: Sentence Length in Scientific Papers
        dbc.Row([
            dbc.Col(html.H4("Research Question 3: Sentence Length in Scientific Papers"), width=6),
            dbc.Col(html.P(
                "How has the length of sentences in scientific papers changed since the introduction of ChatGPT? "
                "We aim to investigate whether sentences have become longer or shorter post-ChatGPT."
            )),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(
                id="sentence-length-graph",
                figure=px.line(df_sentence_length, x="Year", y="Avg_Sentence_Length",
                               title="Average Sentence Length Over Time")
            )),
        ], className="mb-5"),

        # Research Question 4: Asia University Keyword Analysis
        dbc.Row([
            dbc.Col(html.H4("Research Question 4: Keyword Frequency in Asia Universities"), width=6),
            dbc.Col(html.P(
                "This analysis explores how keyword usage has changed in Asian universities since the introduction of ChatGPT."
            )),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(
                id="asia-keyword-graph",
                figure=px.line(df_asia_data, x="Year", y="Keyword_Count",
                               title="Keyword Count in Asian Universities Over Time")
            )),
        ], className="mb-5"),

        # Research Question 5: Comparison Between CAU and Other Universities
        dbc.Row([
            dbc.Col(html.H4("Research Question 5: Comparison Between CAU and Other Universities"), width=6),
            dbc.Col(html.P(
                "What are the differences between Christian-Albrechts-Universität zu Kiel (CAU) and other German universities regarding the perceived influence of ChatGPT? "
                "This project compares the language changes at CAU with other institutions."
            )),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(
                id="comparison-universities-graph",
                figure=px.bar(df_word_usage, x="Year", y="Word_Count", color="Word_Type",
                              title="Comparison of Word Usage Across Universities")
            )),
        ], className="mb-5"),

        # Research Question 6: Faculty Differences at CAU
        dbc.Row([
            dbc.Col(html.H4("Research Question 6: Faculty Differences at CAU"), width=6),
            dbc.Col(html.P(
                "How has word usage changed across different faculties at CAU since the introduction of ChatGPT? "
                "This project analyzes differences between disciplines, such as natural sciences and humanities."
            )),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(
                id="faculty-differences-graph",
                figure=px.bar(df_word_usage, x="Year", y="Word_Count", color="Word_Type",
                              title="Comparison of Word Usage by Faculty")
            )),
        ], className="mb-5"),

        # Research Question 7: Global Comparison Between Universities
        dbc.Row([
            dbc.Col(html.H4("Research Question 7: Global Comparison Between Universities"), width=6),
            dbc.Col(html.P(
                "How do the effects of ChatGPT on scientific papers differ between various universities worldwide? "
                "This includes comparisons between top German universities, European, and Asian institutions."
            )),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(
                id="global-comparison-graph",
                figure=px.line(df_asia_data, x="Year", y="Keyword_Count", title="Global Comparison of Keyword Trends")
            )),
        ], className="mb-5"),

    ], className="py-5")
])

# --- About Section ---
about_section = html.Div(id="about", children=[
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("About Me", style={"color": "#9b0a7d"}), className="mt-5 mb-4 text-center"),
        ]),
        dbc.Row([
            dbc.Col(html.P(
                "Thank you for exploring our page. This project was created by Louis Krückmeyer, Matheus Kolzarek, and Tom Skrzynski-Fox "
                "to explore the impact of ChatGPT on scientific papers. We hope you enjoyed the analysis and visualizations."
            )),
        ], className="text-center"),
    ], className="py-5")
])

