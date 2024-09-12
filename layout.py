import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import pandas as pd
from scipy import stats
import numpy as np
from collections import Counter
import re
import dash
from scipy.stats import chi2_contingency, shapiro, norm
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
from ast import literal_eval

#chatgpt:
# Um  eigene CSV-Datei einzufügen, ersetzen Sie 'your_file.csv' durch den Pfad zu Ihrer CSV-Datei.
# Stellen Sie sicher, dass Ihre CSV-Datei im selben Verzeichnis wie dieses Skript liegt oder geben Sie den vollständigen Pfad an.
# df_bsp = pd.read_csv('your_file.csv')
# df_bsp.head({Anzahl der Zeilen, die angezeigt werden sollen})


colors_blind_friendly = ['#D55E00', '#0072B2', '#F0E442', '#009E73', '#E69F00', '#56B4E9', '#CC79A7', '#8E44AD',
                         '#F39C12', '#1ABC9C', '#2C3E50', '#C0392B', '#2980B9', '#27AE60']

# DATEN AUS CSV
# test
import pandas as pd
import plotly.express as px
from scipy import stats

# Assuming you have loaded the dataframes df_universities, df_fachhochschulen and merged them as df_combined
import pandas as pd

# Load all datasets
df_german_uni = pd.read_csv('Data/Frage_7/German_Uni.csv')
df_german_fh = pd.read_csv('Data/Frage_7/German_FH.csv')
df_germany = pd.read_csv('Data/Frage_7/Germany.csv')
df_eu = pd.read_csv('Data/Frage_7/EU.csv')
df_asia = pd.read_csv('Data/Frage_7/Asia.csv')
df_world = pd.read_csv('Data/Frage_7/World.csv')
# Adding 'type' column to differentiate the sources of data
df_german_uni['type'] = 'Universität DE'
df_german_fh['type'] = 'Fachhochschule DE'
df_germany['type'] = 'Germany'
df_eu['type'] = 'EU'
df_asia['type'] = 'Asien'
df_world['type'] = 'World'

# Combine datasets (two-way combinations)

# 1. Combine German University and Fachhochschule
df_combined_Uni_FH = pd.concat([df_german_uni, df_german_fh])

# 2. Combine German University and Germany
df_combined_Uni_Germany = pd.concat([df_german_uni, df_germany])

# 3. Combine German University and EU
df_combined_Uni_EU = pd.concat([df_german_uni, df_eu])

# 4. Combine German University and Asia
df_combined_Uni_Asia = pd.concat([df_german_uni, df_asia])

# 5. Combine German University and World
df_combined_Uni_World = pd.concat([df_german_uni, df_world])

# 6. Combine Fachhochschule and Germany
df_combined_FH_Germany = pd.concat([df_german_fh, df_germany])

# 7. Combine Fachhochschule and EU
df_combined_FH_EU = pd.concat([df_german_fh, df_eu])

# 8. Combine Fachhochschule and Asia
df_combined_FH_Asia = pd.concat([df_german_fh, df_asia])

# 9. Combine Fachhochschule and World
df_combined_FH_World = pd.concat([df_german_fh, df_world])

# 10. Combine Germany and EU
df_combined_Germany_EU = pd.concat([df_germany, df_eu])

# 11. Combine Germany and Asia
df_combined_Germany_Asia = pd.concat([df_germany, df_asia])

# 12. Combine Germany and World
df_combined_Germany_World = pd.concat([df_germany, df_world])

# 13. Combine EU and Asia
df_combined_EU_Asia = pd.concat([df_eu, df_asia])
# 14. Combine EU and World
df_combined_EU_World = pd.concat([df_eu, df_world])

# 15. Combine Asia and World
df_combined_Asia_World = pd.concat([df_asia, df_world])

datasets = {
    'German University': df_german_uni,
    'Fachhochschule': df_german_fh,
    'Germany': df_germany,
    'EU': df_eu,
    'Asia': df_asia,
    'World': df_world
}
# Now you have all two-way combinations of datasets in the following variables:
# - df_combined_Uni_FH
# - df_combined_Uni_Germany
# - df_combined_Uni_EU
# - df_combined_Uni_Asia
# - df_combined_Uni_World
# - df_combined_FH_Germany
# - df_combined_FH_EU
# - df_combined_FH_Asia
# - df_combined_FH_World
# - df_combined_Germany_EU
# - df_combined_Germany_Asia
# - df_combined_Germany_World
# - df_combined_EU_Asia
# - df_combined_EU_World
# - df_combined_Asia_World

df_universities = pd.read_csv('Data/Frage_7/German_Uni.csv')
df_fachhochschulen = pd.read_csv('Data/Frage_7/German_FH.csv')
df_universities['type'] = 'Universität'
df_fachhochschulen['type'] = 'Fachhochschule'

#df_eu['type'] = 'EU'
#df_asia['type'] = 'Asien'


def prepare_data(df, date_cutoff=2023):
    # Konvertiere 'flag' Spalte in ein besser lesbares Format
    df['flag'] = df['flag'].apply(lambda x: 'Flagged' if x == 'Yes' else 'Not Flagged')

    # Füge eine Spalte für 'DateCategory' hinzu (vor und nach einem bestimmten Datum)
    df['DateCategory'] = df['PubDate'].apply(
        lambda x: f'Before {date_cutoff}' if x < date_cutoff else f'After {date_cutoff}')

    return df


# Schritt 2: Gruppierte Datenberechnung (Flagged Papiere und Gesamtanzahl)
def compute_grouped_data(df):
    # Gruppiere nach Typ (z.B. Universität vs Fachhochschule oder EU vs Asien) und Flag-Status
    df_grouped = df.groupby(['type', 'flag']).size().reset_index(name='count')
    df_total = df.groupby('type').size().reset_index(name='total_count')

    # Prozentsätze berechnen
    df_grouped = pd.merge(df_grouped, df_total, on='type')
    df_grouped['percentage'] = (df_grouped['count'] / df_grouped['total_count']) * 100

    return df_grouped


# Schritt 3: Jährliche Trends (Flagged Papiere über bestimmte Jahre hinweg)
def compute_yearly_trend(df, years_range):
    # Filter the data for the specified years and remove rows where PubDate is invalid (PubDate == 0)
    df_filtered_years = df[(df['PubDate'].isin(years_range)) & (df['PubDate'] != 0)]

    # Group by year and type for flagged papers
    df_year_grouped = df_filtered_years[df_filtered_years['flag'] == 'Flagged'].groupby(
        ['type', 'PubDate']).size().reset_index(name='count')
    df_total_years = df_filtered_years.groupby(['type', 'PubDate']).size().reset_index(name='total_count')

    # Merge the two dataframes
    df_year_grouped = pd.merge(df_year_grouped, df_total_years, on=['type', 'PubDate'])

    # Calculate percentages
    df_year_grouped['percentage'] = (df_year_grouped['count'] / df_year_grouped['total_count']) * 100

    # Check if there's enough data to perform regression
    if df_year_grouped.shape[0] < 2:
        return df_year_grouped, None  # Not enough data for regression

    # Perform linear regression
    years = df_year_grouped['PubDate'].values
    percentages = df_year_grouped['percentage'].values

    if len(years) == 0 or len(percentages) == 0:
        return df_year_grouped, None  # Avoid running regression on empty arrays

    slope, intercept, r_value, p_value, std_err = stats.linregress(years, percentages)

    # Add trend line
    df_year_grouped['trend'] = intercept + slope * df_year_grouped['PubDate']

    return df_year_grouped, p_value



# Schritt 4: Visualisierungen
def visualize_task(df_grouped, df_year_grouped, p_value, task_title):
    # Bar-Diagramm für markierte Papiere
    fig_bar = px.bar(df_grouped[df_grouped['flag'] == 'Flagged'], x='type', y='percentage', color='type',
                     title=f"Percentage of Flagged Papers ({task_title})",
                     labels={'type': 'Institution Type', 'percentage': 'Percentage of Papers'})

    # Liniendiagramm für markierte Papiere über die Jahre mit Trendlinie
    if p_value is not None:
        title_with_p_value = f"Percentage of Flagged Papers ({task_title}) from {df_year_grouped['PubDate'].min()} to {df_year_grouped['PubDate'].max()} (Trend Line, p-value: {p_value:.4f})"
    else:
        title_with_p_value = f"Percentage of Flagged Papers ({task_title}) from {df_year_grouped['PubDate'].min()} to {df_year_grouped['PubDate'].max()} (No valid p-value)"

    fig_line = px.line(df_year_grouped, x='PubDate', y='percentage', color='type',
                       title=title_with_p_value,
                       labels={'PubDate': 'Publication Year', 'percentage': 'Percentage of Papers',
                               'type': 'Institution Type'})

    # Trendlinie hinzufügen
    fig_line.add_scatter(x=df_year_grouped['PubDate'], y=df_year_grouped['trend'], mode='lines', name='Trend Line')

    return fig_bar, fig_line



# Schritt 5: Universeller Workflow für jede Aufgabe (z.B. 7.1, 7.2)
def task_workflow(df, years_range, task_title):
    df = prepare_data(df)
    df_grouped = compute_grouped_data(df)
    df_year_grouped, p_value = compute_yearly_trend(df, years_range)
    fig_bar, fig_line = visualize_task(df_grouped, df_year_grouped, p_value, task_title)

    return fig_bar, fig_line


# Assuming df_combined is the merged dataframe of universities and Fachhochschulen
#fig_bar_7_1, fig_line_7_1 = task_workflow(df_combined_Uni_FH, [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
#                                          "Universities vs Fachhochschulen")
#fig_bar_7_2, fig_line_7_2 = task_workflow(df_combined_Asia_World, [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
#                                          "EU vs Asia")

# Frage 5
df_kiel_uni_5 = pd.read_csv('Data/Kiel_Uni_arxiv_flag_updated.csv')
df_merged_germany_5 = pd.read_csv('Data/Frage_7/Germany.csv')
# Add 'type' column to differentiate CAU and other universities
df_kiel_uni_5['type'] = 'CAU'
df_merged_germany_5['type'] = 'Other Universities'

# Combine the two datasets
df_combined_5 = pd.concat([df_kiel_uni_5, df_merged_germany_5])

# Flag column handling
df_combined_5['flag'] = df_combined_5['flag'].apply(lambda x: 'Flagged' if x == 'Yes' else 'Not Flagged')

# Create date category for before and after 1.1.2023
df_combined_5['DateCategory'] = df_combined_5['PubDate'].apply(
    lambda x: 'Before 1.1.2023' if x < 2023 else 'After 1.1.2023')

# 1. Bar chart for flagged papers percentage
df_grouped_5 = df_combined_5.groupby(['type', 'flag']).size().reset_index(name='count')
df_total_5 = df_combined_5.groupby('type').size().reset_index(name='total_count')
df_grouped_5 = pd.merge(df_grouped_5, df_total_5, on='type')
df_grouped_5['percentage'] = (df_grouped_5['count'] / df_grouped_5['total_count']) * 100

# 2. Bar chart for comparison before and after 1.1.2023
df_date_grouped_5 = df_combined_5[df_combined_5['flag'] == 'Flagged'].groupby(
    ['type', 'DateCategory']).size().reset_index(name='count')
df_total_date_5 = df_combined_5.groupby(['type', 'DateCategory']).size().reset_index(name='total_count')
df_date_grouped_5 = pd.merge(df_date_grouped_5, df_total_date_5, on=['type', 'DateCategory'])
df_date_grouped_5['percentage'] = (df_date_grouped_5['count'] / df_date_grouped_5['total_count']) * 100

# 3. Line chart for flagged papers for 2020-2024
df_filtered_years_5 = df_combined_5[df_combined_5['PubDate'].isin([2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])]
df_year_grouped_5 = df_filtered_years_5[df_filtered_years_5['flag'] == 'Flagged'].groupby(
    ['type', 'PubDate']).size().reset_index(name='count')
df_total_years_5 = df_filtered_years_5.groupby(['type', 'PubDate']).size().reset_index(name='total_count')
df_year_grouped_5 = pd.merge(df_year_grouped_5, df_total_years_5, on=['type', 'PubDate'])
df_year_grouped_5['percentage'] = (df_year_grouped_5['count'] / df_year_grouped_5['total_count']) * 100
years = df_year_grouped_5['PubDate'].values
percentages = df_year_grouped_5['percentage'].values
slope, intercept, r_value, p_value, std_err = stats.linregress(years, percentages)
df_year_grouped_5['trend'] = intercept + slope * df_year_grouped_5['PubDate']
title_with_p_value = f"Percentage of Flagged Papers for 2017-2024 (CAU vs Other Universities)\nTrend Line (p-value: {p_value:.4f})"

# Research question 4
df_RQ4_comparison = pd.read_csv('Data/RQ4_comparison.csv')
RQ_4_df = pd.read_csv('Data/RQ4_PDF_Abstract.csv')

##### RQ6 Import
RQ_6_df = pd.read_csv('Data/RQ6_faculty_keyword.csv')

# Example CSV data
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

# List of color codes for color-blind friendly palette
colors_blind_friendly_extended = ['#D55E00', '#0072B2', '#F0E442', '#009E73', '#E69F00', '#56B4E9', '#CC79A7',
                                  '#8E44AD', '#F39C12', '#1ABC9C', '#2C3E50', '#C0392B', '#2980B9', '#27AE60']

# Use the blue and orange tones specifically for the visualizations
color_blue = colors_blind_friendly_extended[1]  # '#0072B2' (Blue)
color_orange = colors_blind_friendly_extended[0]  # '#D55E00' (Orange)


######## Code for Research Question 1#####################################################

# Relative Frequency Calculation for multiple regions
# Function to extract words and their frequencies from the "found_words" column
def extract_words(text):
    pattern = r'(\w+)\s*\((\d+)\)'
    found = re.findall(pattern, text)
    return Counter({word: int(count) for word, count in found})

# Function to calculate relative word frequencies
def calculate_relative_frequencies(df_pre, df_post):
    pre_chatgpt_words = Counter()
    post_chatgpt_words = Counter()

    # Count words for both periods
    for words in df_pre['found_words'].dropna():
        pre_chatgpt_words.update(extract_words(words))

    for words in df_post['found_words'].dropna():
        post_chatgpt_words.update(extract_words(words))

    # Calculate the total number of words for each period
    total_pre_chatgpt_words = sum(pre_chatgpt_words.values())
    total_post_chatgpt_words = sum(post_chatgpt_words.values())

    # Calculate relative frequencies for each word
    pre_chatgpt_relative = {word: count / total_pre_chatgpt_words for word, count in pre_chatgpt_words.items()}
    post_chatgpt_relative = {word: count / total_post_chatgpt_words for word, count in post_chatgpt_words.items()}

    # Ensure both lists have the same words
    all_words = set(pre_chatgpt_relative.keys()).union(set(post_chatgpt_relative.keys()))
    pre_chatgpt_relative = {word: pre_chatgpt_relative.get(word, 0) for word in all_words}
    post_chatgpt_relative = {word: post_chatgpt_relative.get(word, 0) for word in all_words}

    return pre_chatgpt_relative, post_chatgpt_relative, all_words


# Calculate for all regions
df_eu_pre = df_eu[df_eu['PubDate'] <= 2022]
df_eu_post = df_eu[df_eu['PubDate'] >= 2023]
pre_chatgpt_relative_eu, post_chatgpt_relative_eu, all_words_eu = calculate_relative_frequencies(df_eu_pre, df_eu_post)

df_asia_pre = df_asia[df_asia['PubDate'] <= 2022]
df_asia_post = df_asia[df_asia['PubDate'] >= 2023]
pre_chatgpt_relative_asia, post_chatgpt_relative_asia, all_words_asia = calculate_relative_frequencies(df_asia_pre,
                                                                                                       df_asia_post)

df_universities_pre = df_universities[df_universities['PubDate'] <= 2022]
df_universities_post = df_universities[df_universities['PubDate'] >= 2023]
pre_chatgpt_relative_universities, post_chatgpt_relative_universities, all_words_universities = calculate_relative_frequencies(
    df_universities_pre, df_universities_post)

df_fachhochschulen_pre = df_fachhochschulen[df_fachhochschulen['PubDate'] <= 2022]
df_fachhochschulen_post = df_fachhochschulen[df_fachhochschulen['PubDate'] >= 2023]
pre_chatgpt_relative_fachhochschulen, post_chatgpt_relative_fachhochschulen, all_words_fachhochschulen = calculate_relative_frequencies(
    df_fachhochschulen_pre, df_fachhochschulen_post)


# Function to generate bar chart for relative word usage
def generate_relative_frequency_bar(pre_chatgpt_relative, post_chatgpt_relative, region_name):
    # Convert the relative frequency data into a DataFrame
    df = pd.DataFrame({
        'Word': list(pre_chatgpt_relative.keys()),
        'Pre_ChatGPT': list(pre_chatgpt_relative.values()),
        'Post_ChatGPT': list(post_chatgpt_relative.values())
    })

    # Create bar chart using Plotly Express
    fig = px.bar(
        df,
        x='Word',
        y=['Pre_ChatGPT', 'Post_ChatGPT'],
        title=f'Relative Word Usage Before and After ChatGPT ({region_name})',
        barmode='group'
    )

    # Return the figure for use in Dash layout
    return fig

# Generate relative frequency bar charts for all regions

# For EU region
fig_bar_eu = generate_relative_frequency_bar(pre_chatgpt_relative_eu, post_chatgpt_relative_eu, "EU")

# For Asia region
fig_bar_asia = generate_relative_frequency_bar(pre_chatgpt_relative_asia, post_chatgpt_relative_asia, "Asia")

# For Universities
fig_bar_universities = generate_relative_frequency_bar(pre_chatgpt_relative_universities,
                                                       post_chatgpt_relative_universities, "Universities")

# For Fachhochschulen
fig_bar_fachhochschulen = generate_relative_frequency_bar(pre_chatgpt_relative_fachhochschulen,
                                                          post_chatgpt_relative_fachhochschulen, "Fachhochschulen")


# Chi-Square Test function
def perform_chi_square_test(pre_chatgpt_relative, post_chatgpt_relative, all_words):
    # Create a contingency table
    contingency_table = pd.DataFrame({
        'Pre_ChatGPT': [pre_chatgpt_relative[word] for word in all_words],
        'Post_ChatGPT': [post_chatgpt_relative[word] for word in all_words]
    })

    # Add a small value to avoid zero frequencies
    contingency_table += 1e-10

    # Perform the Chi-Square test (returning chi2 and p only)
    chi2, p, dof, _ = chi2_contingency(contingency_table)

    return chi2, p, dof
# Perform the Chi-Square test for EU
chi2_eu, p_eu, dof_eu = perform_chi_square_test(pre_chatgpt_relative_eu, post_chatgpt_relative_eu, all_words_eu)

# Perform the Chi-Square test for Asia
chi2_asia, p_asia, dof_asia = perform_chi_square_test(pre_chatgpt_relative_asia, post_chatgpt_relative_asia,
                                                      all_words_asia)

# Perform the Chi-Square test for Universities
chi2_universities, p_universities, dof_universities = perform_chi_square_test(pre_chatgpt_relative_universities,
                                                                              post_chatgpt_relative_universities,
                                                                              all_words_universities)

# Perform the Chi-Square test for Fachhochschulen
chi2_fachhochschulen, p_fachhochschulen, dof_fachhochschulen = perform_chi_square_test(
    pre_chatgpt_relative_fachhochschulen, post_chatgpt_relative_fachhochschulen, all_words_fachhochschulen)


# Function to generate the Chi-Square pie chart, always showing a visual regardless of p-value
def generate_chi_square_pie(p_value, region_name):
    # If p-value is 1.0, it means "No significant difference"
    if p_value >= 0.05:
        significant_label = "No significant difference"
        significant_value = 1
    else:
        significant_label = "Significant difference"
        significant_value = 1

    # Create pie chart
    fig = go.Figure()

    # Add pie chart trace
    fig.add_trace(go.Pie(
        labels=[significant_label,
                "Significant difference" if significant_label == "No significant difference" else "No significant difference"],
        values=[significant_value, 0],  # Adjust the second value to ensure the visualization is balanced
        hole=0.4  # Donut chart
    ))

    # Update layout for the chart
    fig.update_layout(
        title_text=f"Chi-Square Test Result for {region_name} (p-value: {p_value:.6f})",
        annotations=[dict(text=significant_label, x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    return fig


# Shapiro-Wilk Test for multiple regions

# Function to perform the Shapiro-Wilk test for normality
def perform_shapiro_test(pre_chatgpt_relative, post_chatgpt_relative):
    pre_chatgpt_values = list(pre_chatgpt_relative.values())
    post_chatgpt_values = list(post_chatgpt_relative.values())

    shapiro_pre_result = None
    shapiro_post_result = None

    # Perform the Shapiro-Wilk test for Pre-ChatGPT data
    if len(pre_chatgpt_values) >= 3:  # Shapiro-Wilk test requires at least 3 values
        stat_pre, p_pre = shapiro(pre_chatgpt_values)
        shapiro_pre_result = (stat_pre, p_pre)

    # Perform the Shapiro-Wilk test for Post-ChatGPT data
    if len(post_chatgpt_values) >= 3:
        stat_post, p_post = shapiro(post_chatgpt_values)
        shapiro_post_result = (stat_post, p_post)

    return shapiro_pre_result, shapiro_post_result


# Perform the Shapiro-Wilk test for all regions
shapiro_pre_eu, shapiro_post_eu = perform_shapiro_test(pre_chatgpt_relative_eu, post_chatgpt_relative_eu)
shapiro_pre_asia, shapiro_post_asia = perform_shapiro_test(pre_chatgpt_relative_asia, post_chatgpt_relative_asia)
shapiro_pre_universities, shapiro_post_universities = perform_shapiro_test(pre_chatgpt_relative_universities,
                                                                           post_chatgpt_relative_universities)
shapiro_pre_fachhochschulen, shapiro_post_fachhochschulen = perform_shapiro_test(pre_chatgpt_relative_fachhochschulen,
                                                                                 post_chatgpt_relative_fachhochschulen)


# Function to plot Shapiro-Wilk Test histograms for normality visualization
# Function to generate Plotly histogram for Shapiro-Wilk test
# Function to generate a Shapiro-Wilk Test histogram with the specified colors
def generate_shapiro_histogram_figure(pre_values, post_values, region_name):
    # Create a figure for Plotly histogram
    fig = go.Figure()

    # Pre-ChatGPT histogram
    fig.add_trace(go.Histogram(x=pre_values, name="Pre-ChatGPT", marker_color=color_blue, opacity=0.75))

    # Post-ChatGPT histogram
    fig.add_trace(go.Histogram(x=post_values, name="Post-ChatGPT", marker_color=color_orange, opacity=0.75))

    # Update layout
    fig.update_layout(
        title=f'Shapiro-Wilk Test Histogram for {region_name}',
        barmode='overlay',
        xaxis_title='Relative Frequency',
        yaxis_title='Density',
        legend_title="Time Period",
        bargap=0.1,
        bargroupgap=0.2
    )

    # Return the figure
    return fig


# Generate Chi-Square pie charts for all regions
fig_pie_eu = generate_chi_square_pie(p_eu, "EU")
fig_pie_asia = generate_chi_square_pie(p_asia, "Asia")
fig_pie_universities = generate_chi_square_pie(p_universities, "Universities")
fig_pie_fachhochschulen = generate_chi_square_pie(p_fachhochschulen, "Fachhochschulen")

# Generate the Shapiro-Wilk histogram figures for all regions

# EU region
fig_shapiro_eu = generate_shapiro_histogram_figure(
    list(pre_chatgpt_relative_eu.values()),
    list(post_chatgpt_relative_eu.values()),
    "EU"
)

# Asia region
fig_shapiro_asia = generate_shapiro_histogram_figure(
    list(pre_chatgpt_relative_asia.values()),
    list(post_chatgpt_relative_asia.values()),
    "Asia"
)

# Universities region
fig_shapiro_universities = generate_shapiro_histogram_figure(
    list(pre_chatgpt_relative_universities.values()),
    list(post_chatgpt_relative_universities.values()),
    "Universities"
)

# Fachhochschulen region
fig_shapiro_fachhochschulen = generate_shapiro_histogram_figure(
    list(pre_chatgpt_relative_fachhochschulen.values()),
    list(post_chatgpt_relative_fachhochschulen.values()),
    "Fachhochschulen"
)


def clean_numeric_values(values):
    # Filter out any non-numeric values or NaNs
    return [v for v in values if isinstance(v, (int, float)) and not np.isnan(v)]


# Mann-Whitney U-Test function
def perform_mann_whitney_test(pre_values, post_values):
    # Clean the data to ensure only numeric values are passed to the test
    pre_values_clean = clean_numeric_values(pre_values)
    post_values_clean = clean_numeric_values(post_values)

    # Perform the Mann-Whitney U test
    u_stat, p_value = mannwhitneyu(pre_values_clean, post_values_clean)
    return u_stat, p_value


# Violin plot for visualizing distributions
def generate_violin_plot(pre_values, post_values, region_name):
    # Create a DataFrame for Plotly
    data = pd.DataFrame({
        'Values': pre_values + post_values,
        'Group': ['Pre-ChatGPT'] * len(pre_values) + ['Post-ChatGPT'] * len(post_values)
    })

    # Create the violin plot
    fig = px.violin(data, x='Group', y='Values', box=True, points='all', title=f"Mann-Whitney U Test for {region_name}")

    return fig


# Perform the Mann-Whitney U test for all regions

# For EU
u_stat_eu, p_value_eu = perform_mann_whitney_test(list(pre_chatgpt_relative_eu.values()),
                                                  list(post_chatgpt_relative_eu.values()))
fig_violin_eu = generate_violin_plot(list(pre_chatgpt_relative_eu.values()), list(post_chatgpt_relative_eu.values()),
                                     "EU")

# For Asia
u_stat_asia, p_value_asia = perform_mann_whitney_test(list(pre_chatgpt_relative_asia.values()),
                                                      list(post_chatgpt_relative_asia.values()))
fig_violin_asia = generate_violin_plot(list(pre_chatgpt_relative_asia.values()),
                                       list(post_chatgpt_relative_asia.values()), "Asia")

# For Universities
u_stat_universities, p_value_universities = perform_mann_whitney_test(list(pre_chatgpt_relative_universities.values()),
                                                                      list(post_chatgpt_relative_universities.values()))
fig_violin_universities = generate_violin_plot(list(pre_chatgpt_relative_universities.values()),
                                               list(post_chatgpt_relative_universities.values()), "Universities")

# For Fachhochschulen
u_stat_fachhochschulen, p_value_fachhochschulen = perform_mann_whitney_test(
    list(pre_chatgpt_relative_fachhochschulen.values()), list(post_chatgpt_relative_fachhochschulen.values()))
fig_violin_fachhochschulen = generate_violin_plot(list(pre_chatgpt_relative_fachhochschulen.values()),
                                                  list(post_chatgpt_relative_fachhochschulen.values()),
                                                  "Fachhochschulen")

############################################ End research question 1 ##################################################


######## Code for Research Question 2 ###########################################################################

# Load the CSV files for each region
df_eu_question = pd.read_csv('Data/Merged_EU_datasets_questionwords.csv')
df_asia_question = pd.read_csv('Data/Merged_Asia_datasets_questionwords.csv')
df_fachhochschule_question = pd.read_csv('Data/Merged_FH_datasets_questionwords.csv')
df_world_question = pd.read_csv('Data/Merged_World_datasets_questionwords.csv')


# Function to extract question words and their counts from the 'Question_Words' column
def extract_question_words(question_words_column):
    question_words_count = []
    for entry in question_words_column:
        if isinstance(entry, str):  # Check if the entry is a valid string
            words = re.findall(r'(\w+)\s\((\d+)\)', entry)
            word_count = {word: int(count) for word, count in words}
            question_words_count.append(word_count)
        else:
            question_words_count.append({})
    return question_words_count


# Function to aggregate question words across the dataframe
def aggregate_question_words(df):
    total_words = Counter()
    for index, row in df.iterrows():
        total_words.update(row['Question_Words_Count'])
    return total_words


# Function to calculate relative frequencies of question words
def calculate_relative_frequencies(word_counts, num_abstracts):
    return {word: count / num_abstracts for word, count in word_counts.items()}


# Function to calculate relative frequencies of question marks
def calculate_relative_marks(df, num_abstracts):
    return df['Question_Mark_Count'].sum() / num_abstracts


# Process each region separately

# Function to generate bar chart for question words with the specified colors
def generate_question_word_bar_chart(before_values, after_values, words):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=words, y=before_values, name='Pre-ChatGPT', marker_color=color_blue))
    fig.add_trace(go.Bar(x=words, y=after_values, name='Post-ChatGPT', marker_color=color_orange))

    # Update layout
    fig.update_layout(
        title="Comparison of Relative Frequencies of Question Words (Pre-ChatGPT vs Post-ChatGPT)",
        xaxis_title="Question Words",
        yaxis_title="Relative Frequency",
        barmode='group',
        xaxis_tickangle=-45
    )

    return fig


# Bar chart for question marks with Pre-ChatGPT and Post-ChatGPT labels, using specified colors
def generate_question_mark_chart(relative_marks_before, relative_marks_after):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=['Pre-ChatGPT', 'Post-ChatGPT'], y=[relative_marks_before, relative_marks_after],
                         marker_color=[color_blue, color_orange]))

    # Update layout
    fig.update_layout(
        title="Comparison of Relative Frequencies of Question Marks (Pre-ChatGPT vs Post-ChatGPT)",
        xaxis_title="Time Period",
        yaxis_title="Relative Frequency"
    )

    return fig


# Process each region separately using the correct DataFrame
def process_region_data(df, region_name):
    # Check if 'Question_Words' column exists
    if 'Question_Words' not in df.columns:
        raise KeyError(f"Column 'Question_Words' not found in {region_name} data")

    # Extract question words
    df['Question_Words_Count'] = extract_question_words(df['Question_Words'])

    # Split data into before and after 2023
    df_before_2023 = df[df['PubDate'] <= 2022]
    df_after_2023 = df[df['PubDate'] >= 2023]

    # Number of abstracts
    n_abstracts_before_2023 = len(df_before_2023)
    n_abstracts_after_2023 = len(df_after_2023)

    # Aggregate question words
    words_before_2023 = aggregate_question_words(df_before_2023)
    words_after_2023 = aggregate_question_words(df_after_2023)

    # Filter out excluded words
    excluded_words = {'much', 'many', 'far', 'long'}
    words_before_2023_filtered = {k: v for k, v in words_before_2023.items() if k not in excluded_words}
    words_after_2023_filtered = {k: v for k, v in words_after_2023.items() if k not in excluded_words}

    # Calculate relative frequencies
    relative_words_before_2023 = calculate_relative_frequencies(words_before_2023_filtered, n_abstracts_before_2023)
    relative_words_after_2023 = calculate_relative_frequencies(words_after_2023_filtered, n_abstracts_after_2023)

    # Calculate question mark frequencies
    relative_marks_before_2023 = calculate_relative_marks(df_before_2023, n_abstracts_before_2023)
    relative_marks_after_2023 = calculate_relative_marks(df_after_2023, n_abstracts_after_2023)

    # Prepare data for visualization
    all_words = sorted(set(relative_words_before_2023.keys()).union(set(relative_words_after_2023.keys())))
    before_values = [relative_words_before_2023.get(word, 0) for word in all_words]
    after_values = [relative_words_after_2023.get(word, 0) for word in all_words]

    # Generate figures
    fig_question_words = generate_question_word_bar_chart(before_values, after_values, all_words)
    fig_question_marks = generate_question_mark_chart(relative_marks_before_2023, relative_marks_after_2023)

    return fig_question_words, fig_question_marks


# Process the regions using the specific variables for each
fig_words_eu, fig_marks_eu = process_region_data(df_eu_question, "EU")
fig_words_asia, fig_marks_asia = process_region_data(df_asia_question, "Asia")
fig_words_fachhochschule, fig_marks_fachhochschule = process_region_data(df_fachhochschule_question, "Fachhochschule")
fig_words_world, fig_marks_world = process_region_data(df_world_question, "World")

############################################ End research question 2 ##################################################

######## Code for Research Question 3 ###########################################################################

# Load the regional CSV files
df_eu_sentence = pd.read_csv('Data/Merged_EU_datasets_sentence.csv')
df_asia_sentence = pd.read_csv('Data/Merged_Asia_datasets_sentence.csv')
df_fachhochschule_sentence = pd.read_csv('Data/Merged_FH_datasets_sentence.csv')
df_world_sentence = pd.read_csv('Data/Merged_World_datasets_sentence.csv')


# Function to split the data into pre- and post-ChatGPT (2022 and earlier vs. 2023 and later)
def split_data(df):
    df['Year'] = pd.to_numeric(df['PubDate'], errors='coerce').fillna(0).astype(int)
    pre_chatgpt = df[df['Year'] <= 2022]
    post_chatgpt = df[df['Year'] >= 2023]
    return pre_chatgpt, post_chatgpt


# Function to calculate average values
def calculate_averages(df):
    avg_sentence_count = df['Sentence_Count'].mean()

    def safe_mean(x):
        try:
            lengths = literal_eval(x)
            if isinstance(lengths, list) and len(lengths) > 0:
                return np.mean(lengths)
            return np.nan
        except (ValueError, SyntaxError):
            return np.nan

    def safe_sum(x):
        try:
            lengths = literal_eval(x)
            if isinstance(lengths, list) and len(lengths) > 0:
                return np.sum(lengths)
            return np.nan
        except (ValueError, SyntaxError):
            return np.nan

    # Calculate average number of words per sentence
    avg_words_per_sentence = df['Sentence_Lengths'].apply(safe_mean).mean()

    # Calculate average number of words per abstract
    avg_words_per_abstract = df['Sentence_Lengths'].apply(safe_sum).mean()

    return avg_sentence_count, avg_words_per_sentence, avg_words_per_abstract


# Visualization using Plotly
def visualize_averages(pre_averages, post_averages):
    labels = ['Sentence Count', 'Words per Sentence', 'Words per Abstract']

    pre_values = list(pre_averages)
    post_values = list(post_averages)

    x = np.arange(len(labels))
    width = 0.35

    fig = go.Figure()

    # Add bars for Pre-ChatGPT
    fig.add_trace(go.Bar(x=labels, y=pre_values, name='Pre-ChatGPT', marker_color=color_blue))

    # Add bars for Post-ChatGPT
    fig.add_trace(go.Bar(x=labels, y=post_values, name='Post-ChatGPT', marker_color=color_orange))

    # Customize layout
    fig.update_layout(
        title="Average Values Comparison (Pre-ChatGPT vs Post-ChatGPT)",
        xaxis_title="Metrics",
        yaxis_title="Average Value",
        barmode='group'
    )

    return fig


# Process and visualize averages for each region
def process_and_visualize_region(df, region_name):
    pre_chatgpt, post_chatgpt = split_data(df)

    # Calculate averages
    pre_averages = calculate_averages(pre_chatgpt)
    post_averages = calculate_averages(post_chatgpt)

    # Generate visualization
    fig = visualize_averages(pre_averages, post_averages)

    return fig


# Generate figures for each region
fig_eu = process_and_visualize_region(df_eu_sentence, "EU")
fig_asia = process_and_visualize_region(df_asia_sentence, "Asia")
fig_fachhochschule = process_and_visualize_region(df_fachhochschule_sentence, "Fachhochschule")
fig_world = process_and_visualize_region(df_world_sentence, "World")


############

def safe_mean(x):
    try:
        lengths = literal_eval(x)
        if isinstance(lengths, list) and len(lengths) > 0:
            valid_lengths = [l for l in lengths if not np.isnan(l)]  # Filter out NaN values
            if len(valid_lengths) > 0:
                return np.mean(valid_lengths)
        return np.nan
    except (ValueError, SyntaxError):
        return np.nan


def safe_sum(x):
    try:
        lengths = literal_eval(x)
        if isinstance(lengths, list) and len(lengths) > 0:
            valid_lengths = [l for l in lengths if not np.isnan(l)]  # Filter out NaN values
            if len(valid_lengths) > 0:
                return np.sum(valid_lengths)
        return np.nan
    except (ValueError, SyntaxError):
        return np.nan


# Filter NaN values before performing Chi-Square tests or any other operations
def filter_valid_data(data):
    return data.dropna()  # Remove NaN values


# performing Chi-Square tests
def perform_chi_square_test(pre_data, post_data, label):
    # Drop NaN values
    pre_data = pre_data.dropna()
    post_data = post_data.dropna()

    # Ensure that both datasets are non-empty
    if pre_data.empty or post_data.empty:
        print(f"Insufficient data for {label}. Skipping Chi-Square test.")
        return None, None, None

    # Proceed with Chi-Square test
    pre_categories, pre_counts = np.unique(pre_data, return_counts=True)
    post_categories, post_counts = np.unique(post_data, return_counts=True)

    # Ensure matching categories in both groups
    categories = sorted(set(pre_categories).union(set(post_categories)))

    # Align counts for each category
    pre_counts_aligned = np.array(
        [pre_counts[np.where(pre_categories == cat)[0][0]] if cat in pre_categories else 0 for cat in categories])
    post_counts_aligned = np.array(
        [post_counts[np.where(post_categories == cat)[0][0]] if cat in post_categories else 0 for cat in categories])

    # Create a contingency table
    contingency_table = np.array([pre_counts_aligned, post_counts_aligned])

    # Perform the Chi-Square test
    chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)

    return chi2_stat, p_value, dof


# Generate pie chart for Chi-Square results
def generate_chi_square_pie(p_value, label):
    if p_value is None:
        fig = go.Figure()
        fig.add_trace(go.Pie(labels=["Insufficient Data"], values=[1], hole=0.4,
                             marker=dict(colors=[color_blue, '#EAECEE'])))  # Light grey for 'No Data'
        fig.update_layout(
            title_text=f"Chi-Square Test for {label} - Insufficient Data",
            annotations=[dict(text="No Data", x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        return fig

    significant_label = "No significant difference" if p_value >= 0.05 else "Significant difference"
    significant_value = 1

    # Create pie chart with blue and orange tones
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=[significant_label, "Other"],
        values=[significant_value, 0],
        hole=0.4,
        marker=dict(colors=[color_blue, color_orange])
    ))

    fig.update_layout(
        title_text=f"Chi-Square Test Result for {label} (p-value: {p_value:.6f})",
        annotations=[dict(text=significant_label, x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    return fig


# Main function to analyze and perform Chi-Square test
def analyze_with_chi_square(df):
    # Split data into pre- and post-ChatGPT
    pre_chatgpt, post_chatgpt = split_data(df)

    # Prepare data for the test
    pre_sentence_count = filter_valid_data(pre_chatgpt['Sentence_Count'])
    post_sentence_count = filter_valid_data(post_chatgpt['Sentence_Count'])

    pre_word_lengths = pre_chatgpt['Sentence_Lengths'].apply(lambda x: safe_mean(x) if pd.notnull(x) else np.nan)
    post_word_lengths = post_chatgpt['Sentence_Lengths'].apply(lambda x: safe_mean(x) if pd.notnull(x) else np.nan)

    pre_word_counts = pre_chatgpt['Sentence_Lengths'].apply(lambda x: safe_sum(x) if pd.notnull(x) else np.nan)
    post_word_counts = post_chatgpt['Sentence_Lengths'].apply(lambda x: safe_sum(x) if pd.notnull(x) else np.nan)

    # Perform the Chi-Square tests
    chi2_sentence_count, p_sentence_count, _ = perform_chi_square_test(pre_sentence_count, post_sentence_count,
                                                                       "Sentence Count")
    chi2_word_lengths, p_word_lengths, _ = perform_chi_square_test(pre_word_lengths, post_word_lengths,
                                                                   "Words per Sentence")
    chi2_word_counts, p_word_counts, _ = perform_chi_square_test(pre_word_counts, post_word_counts,
                                                                 "Words per Abstract")

    # Generate pie charts
    fig_sentence_count = generate_chi_square_pie(p_sentence_count, "Sentence Count")
    fig_word_lengths = generate_chi_square_pie(p_word_lengths, "Words per Sentence")
    fig_word_counts = generate_chi_square_pie(p_word_counts, "Words per Abstract")

    return fig_sentence_count, fig_word_lengths, fig_word_counts


# Perform Chi-Square analysis for each region
fig_eu_sentence_count, fig_eu_word_lengths, fig_eu_word_counts = analyze_with_chi_square(df_eu_sentence)
fig_asia_sentence_count, fig_asia_word_lengths, fig_asia_word_counts = analyze_with_chi_square(df_asia_sentence)
fig_fachhochschule_sentence_count, fig_fachhochschule_word_lengths, fig_fachhochschule_word_counts = analyze_with_chi_square(
    df_fachhochschule_sentence)
fig_world_sentence_count, fig_world_word_lengths, fig_world_word_counts = analyze_with_chi_square(df_world_sentence)
############################################ End research question 3 ##################################################


# Home Section (Intro and overview)
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
        # Removed the row containing the "Explore Research" button
    ], className="py-5")
])

# Projects Section now contains research questions and actual data visualizations
projects_section = html.Div(id="projects", children=[
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Research Questions", style={"color": "#9b0a7d"}), className="mt-5 mb-4 text-center"),
        ]),
        # Research Question 1: Changes in Word Usage (using real data)

        # Universities Section
        dbc.Row([dbc.Col(html.H2("Universities Section"), className="mb-4 text-center")]),
        # Bar Chart for Universities
        dbc.Row([dbc.Col(dcc.Graph(id="word-usage-bar-universities", figure=fig_bar_universities))], className="mb-5"),
        # Chi-Square Test for Universities
        dbc.Row([dbc.Col(dcc.Graph(id="chi-square-pie-universities", figure=fig_pie_universities))], className="mb-5"),
        dbc.Row([dbc.Col(html.P(
            f"Chi-Square Test for Universities: chi2 = {chi2_universities:.6f}, p-value = {p_universities:.6f}. "
            f"{'Significant difference' if p_universities < 0.05 else 'No significant difference'}."
        ))], className="mb-5"),
        # Shapiro-Wilk Test for Universities
        dbc.Row([dbc.Col(dcc.Graph(id="shapiro-histogram-universities", figure=fig_shapiro_universities))],
                className="mb-5"),
        dbc.Row([
            dbc.Col(html.P(
                f"Shapiro-Wilk Test for Pre-ChatGPT Universities: p-value = {shapiro_pre_universities[1]:.6f}, stat = {shapiro_pre_universities[0]:.6f}. "
                f"{'Not normally distributed' if shapiro_pre_universities[1] < 0.05 else 'Normally distributed'}."
            )),
            dbc.Col(html.P(
                f"Shapiro-Wilk Test for Post-ChatGPT Universities: p-value = {shapiro_post_universities[1]:.6f}, stat = {shapiro_post_universities[0]:.6f}. "
                f"{'Not normally distributed' if shapiro_post_universities[1] < 0.05 else 'Normally distributed'}."
            )),
        ], className="mb-5"),
        # Mann-Whitney U Test for Universities
        dbc.Row([dbc.Col(dcc.Graph(id="mann-whitney-violin-universities", figure=fig_violin_universities))],
                className="mb-5"),
        dbc.Row([dbc.Col(html.P(
            f"Mann-Whitney U Test for Universities: U-statistic = {u_stat_universities:.6f}, p-value = {p_value_universities:.6f}. "
            f"{'Significant difference' if p_value_universities < 0.05 else 'No significant difference'}."
        ))], className="mb-5"),

        # EU Section
        dbc.Row([dbc.Col(html.H2("EU Section"), className="mb-4 text-center")]),
        # Bar Chart for EU
        dbc.Row([dbc.Col(dcc.Graph(id="word-usage-bar-eu", figure=fig_bar_eu))], className="mb-5"),
        # Chi-Square Test for EU
        dbc.Row([dbc.Col(dcc.Graph(id="chi-square-pie-eu", figure=fig_pie_eu))], className="mb-5"),
        dbc.Row([dbc.Col(html.P(
            f"Chi-Square Test for EU: chi2 = {chi2_eu:.6f}, p-value = {p_eu:.6f}. "
            f"{'Significant difference' if p_eu < 0.05 else 'No significant difference'}."
        ))], className="mb-5"),
        # Shapiro-Wilk Test for EU
        dbc.Row([dbc.Col(dcc.Graph(id="shapiro-histogram-eu", figure=fig_shapiro_eu))], className="mb-5"),
        dbc.Row([
            dbc.Col(html.P(
                f"Shapiro-Wilk Test for Pre-ChatGPT EU: p-value = {shapiro_pre_eu[1]:.6f}, stat = {shapiro_pre_eu[0]:.6f}. "
                f"{'Not normally distributed' if shapiro_pre_eu[1] < 0.05 else 'Normally distributed'}."
            )),
            dbc.Col(html.P(
                f"Shapiro-Wilk Test for Post-ChatGPT EU: p-value = {shapiro_post_eu[1]:.6f}, stat = {shapiro_post_eu[0]:.6f}. "
                f"{'Not normally distributed' if shapiro_post_eu[1] < 0.05 else 'Normally distributed'}."
            )),
        ], className="mb-5"),
        # Mann-Whitney U Test for EU
        dbc.Row([dbc.Col(dcc.Graph(id="mann-whitney-violin-eu", figure=fig_violin_eu))], className="mb-5"),
        dbc.Row([dbc.Col(html.P(
            f"Mann-Whitney U Test for EU: U-statistic = {u_stat_eu:.6f}, p-value = {p_value_eu:.6f}. "
            f"{'Significant difference' if p_value_eu < 0.05 else 'No significant difference'}."
        ))], className="mb-5"),

        # Asia Section
        dbc.Row([dbc.Col(html.H2("Asia Section"), className="mb-4 text-center")]),
        # Bar Chart for Asia
        dbc.Row([dbc.Col(dcc.Graph(id="word-usage-bar-asia", figure=fig_bar_asia))], className="mb-5"),
        # Chi-Square Test for Asia
        dbc.Row([dbc.Col(dcc.Graph(id="chi-square-pie-asia", figure=fig_pie_asia))], className="mb-5"),
        dbc.Row([dbc.Col(html.P(
            f"Chi-Square Test for Asia: chi2 = {chi2_asia:.6f}, p-value = {p_asia:.6f}. "
            f"{'Significant difference' if p_asia < 0.05 else 'No significant difference'}."
        ))], className="mb-5"),
        # Shapiro-Wilk Test for Asia
        dbc.Row([dbc.Col(dcc.Graph(id="shapiro-histogram-asia", figure=fig_shapiro_asia))], className="mb-5"),
        dbc.Row([
            dbc.Col(html.P(
                f"Shapiro-Wilk Test for Pre-ChatGPT Asia: p-value = {shapiro_pre_asia[1]:.6f}, stat = {shapiro_pre_asia[0]:.6f}. "
                f"{'Not normally distributed' if shapiro_pre_asia[1] < 0.05 else 'Normally distributed'}."
            )),
            dbc.Col(html.P(
                f"Shapiro-Wilk Test for Post-ChatGPT Asia: p-value = {shapiro_post_asia[1]:.6f}, stat = {shapiro_post_asia[0]:.6f}. "
                f"{'Not normally distributed' if shapiro_post_asia[1] < 0.05 else 'Normally distributed'}."
            )),
        ], className="mb-5"),
        # Mann-Whitney U Test for Asia
        dbc.Row([dbc.Col(dcc.Graph(id="mann-whitney-violin-asia", figure=fig_violin_asia))], className="mb-5"),
        dbc.Row([dbc.Col(html.P(
            f"Mann-Whitney U Test for Asia: U-statistic = {u_stat_asia:.6f}, p-value = {p_value_asia:.6f}. "
            f"{'Significant difference' if p_value_asia < 0.05 else 'No significant difference'}."
        ))], className="mb-5"),

        # Fachhochschulen Section
        dbc.Row([dbc.Col(html.H2("Fachhochschulen Section"), className="mb-4 text-center")]),
        # Bar Chart for Fachhochschulen
        dbc.Row([dbc.Col(dcc.Graph(id="word-usage-bar-fachhochschulen", figure=fig_bar_fachhochschulen))],
                className="mb-5"),
        # Chi-Square Test for Fachhochschulen
        dbc.Row([dbc.Col(dcc.Graph(id="chi-square-pie-fachhochschulen", figure=fig_pie_fachhochschulen))],
                className="mb-5"),
        dbc.Row([dbc.Col(html.P(
            f"Chi-Square Test for Fachhochschulen: chi2 = {chi2_fachhochschulen:.6f}, p-value = {p_fachhochschulen:.6f}. "
            f"{'Significant difference' if p_fachhochschulen < 0.05 else 'No significant difference'}."
        ))], className="mb-5"),
        # Shapiro-Wilk Test for Fachhochschulen
        dbc.Row([dbc.Col(dcc.Graph(id="shapiro-histogram-fachhochschulen", figure=fig_shapiro_fachhochschulen))],
                className="mb-5"),
        dbc.Row([
            dbc.Col(html.P(
                f"Shapiro-Wilk Test for Pre-ChatGPT Fachhochschulen: p-value = {shapiro_pre_fachhochschulen[1]:.6f}, stat = {shapiro_pre_fachhochschulen[0]:.6f}. "
                f"{'Not normally distributed' if shapiro_pre_fachhochschulen[1] < 0.05 else 'Normally distributed'}."
            )),
            dbc.Col(html.P(
                f"Shapiro-Wilk Test for Post-ChatGPT Fachhochschulen: p-value = {shapiro_post_fachhochschulen[1]:.6f}, stat = {shapiro_post_fachhochschulen[0]:.6f}. "
                f"{'Not normally distributed' if shapiro_post_fachhochschulen[1] < 0.05 else 'Normally distributed'}."
            )),
        ], className="mb-5"),
        # Mann-Whitney U Test for Fachhochschulen
        dbc.Row([dbc.Col(dcc.Graph(id="mann-whitney-violin-fachhochschulen", figure=fig_violin_fachhochschulen))],
                className="mb-5"),
        dbc.Row([dbc.Col(html.P(
            f"Mann-Whitney U Test for Fachhochschulen: U-statistic = {u_stat_fachhochschulen:.6f}, p-value = {p_value_fachhochschulen:.6f}. "
            f"{'Significant difference' if p_value_fachhochschulen < 0.05 else 'No significant difference'}."
        ))], className="mb-5"),

        # Research Question 2: Changes in the Use of Question Words
        dbc.Row([
            dbc.Col(html.H4("Research Question 2: Changes in the Use of Question Words"), width=6),
            dbc.Col(html.P(
                "What changes are there in the use of question words (e.g., what, why) in scientific papers since the introduction of ChatGPT? "
                "This section explores the frequency of question words before and after 2022.")),
        ]),

        # EU Section
        dbc.Row([dbc.Col(html.H3("EU Section"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_words_eu))], className="mb-5"),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_marks_eu))], className="mb-5"),

        # Asia Section
        dbc.Row([dbc.Col(html.H3("Asia Section"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_words_asia))], className="mb-5"),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_marks_asia))], className="mb-5"),

        # Fachhochschule Section
        dbc.Row([dbc.Col(html.H3("Fachhochschule Section"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_words_fachhochschule))], className="mb-5"),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_marks_fachhochschule))], className="mb-5"),

        # World Section
        dbc.Row([dbc.Col(html.H3("World Section"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_words_world))], className="mb-5"),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_marks_world))], className="mb-5"),

        # Research Question 3: Sentence Length in Scientific Papers
        dbc.Row([
            dbc.Col(html.H4("Research Question 3: Sentence Length in Scientific Papers"), width=6),
            dbc.Col(html.P(
                "How has the length of sentences in scientific papers changed since the introduction of ChatGPT? "
                "We aim to investigate whether sentences have become longer or shorter post-ChatGPT.")),
        ]),

        # EU Section
        dbc.Row([dbc.Col(html.H3("EU - Sentence Count"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_eu_sentence_count))], className="mb-5"),
        dbc.Row([dbc.Col(html.H3("EU - Words per Sentence"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_eu_word_lengths))], className="mb-5"),
        dbc.Row([dbc.Col(html.H3("EU - Words per Abstract"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_eu_word_counts))], className="mb-5"),

        # Asia Section
        dbc.Row([dbc.Col(html.H3("Asia - Sentence Count"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_asia_sentence_count))], className="mb-5"),
        dbc.Row([dbc.Col(html.H3("Asia - Words per Sentence"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_asia_word_lengths))], className="mb-5"),
        dbc.Row([dbc.Col(html.H3("Asia - Words per Abstract"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_asia_word_counts))], className="mb-5"),

        # World Section
        dbc.Row([dbc.Col(html.H3("World - Sentence Count"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_world_sentence_count))], className="mb-5"),
        dbc.Row([dbc.Col(html.H3("World - Words per Sentence"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_world_word_lengths))], className="mb-5"),
        dbc.Row([dbc.Col(html.H3("World - Words per Abstract"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_world_word_counts))], className="mb-5"),

        # Fachhochschule Section
        dbc.Row([dbc.Col(html.H3("Fachhochschule - Sentence Count"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_fachhochschule_sentence_count))], className="mb-5"),
        dbc.Row([dbc.Col(html.H3("Fachhochschule - Words per Sentence"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_fachhochschule_word_lengths))], className="mb-5"),
        dbc.Row([dbc.Col(html.H3("Fachhochschule - Words per Abstract"))]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_fachhochschule_word_counts))], className="mb-5"),

        # Research Question 4: Comparison of Flagged Keywords in PDFs and Abstracts
        dbc.Row([
            dbc.Col(html.H4("Research Question 4: Comparison of PDF and abstract flagging"), width=6),
            dbc.Col(html.P(
                "How often do certain keywords get flagged in papers?"
                "Is there a correlation between flagged keywords in abstracts and pdf files?")),
        ]),
        dbc.Row([
            html.Div(id='slider-RQ4', children=
            [dcc.Slider(id='RQ4-year-slider',
                        min=RQ_4_df['Year'].min(),
                        max=RQ_4_df['Year'].max(),
                        value=RQ_4_df['Year'].min(),
                        marks={str(year): str(year) for year in RQ_4_df['Year'].unique()},
                        step=None
                        )], style={'width': '50%', 'display': 'inline-block'}),
            # inline-block : to show slider and dropdown in the same line

            html.Div(id='RQ4-radio', children=
            [dcc.RadioItems(id='RQ4-Keyword-radio',
                            options=[
                                {'label': 'PDF', 'value': 'Count_PDF'},
                                {'label': 'Abstract', 'value': 'Count_Abs'}],
                            value='Count_PDF',
                            )], style={'width': '50%', 'display': 'inline-block'}),

            html.Div(id='RQ4-radio-log', children=
            [dcc.RadioItems(id='RQ4-Keyword-radio-log',
                            options=[
                                {'label': 'Log scale', 'value': True},
                                {'label': 'Linear scale', 'value': False}],
                            value=True,
                            )], style={'width': '50%', 'display': 'inline-block'}),

            dcc.Graph(id='RQ4-barchart'),
        ], className="mb-5"),

        # Research Question 5: Comparison Between CAU and Other Universities
        dbc.Row([
            dbc.Col(html.H4("Research Question 5: Comparison Between CAU and Other Universities"), width=6),
            dbc.Col(html.P(
                "How do the effects of ChatGPT on scientific papers differ between CAU and other German universities? "
                "This includes comparisons between Christian-Albrechts-Universität zu Kiel and other institutions.")),
        ]),
        # Bar chart for flagged papers percentage (Research Question 5)
        dbc.Row([
            dbc.Col(dcc.Graph(
                id="comparison-graph-5",
                figure=px.bar(df_grouped_5, x='type', y='percentage', color='flag',
                           title="Flagged vs Non-Flagged Papers (CAU vs Other Universities)",
                           labels={'type': 'Institution Type', 'percentage': 'Percentage of Papers',
                                   'flag': 'Flagged Status'},
                           barmode='stack')

            )),
        ], className="mb-5"),

        # Comparison Before and After 1.1.2023 for Research Question 5
        dbc.Row([
            dbc.Col(html.H4(
                "Research Question 5: Comparison of Papers Before and After 1.1.2023 (CAU vs Other Universities)"),
                    width=6),
            dbc.Col(html.P(
                "How has the percentage of flagged papers changed before and after 1.1.2023 between CAU and other German universities? "
                "This graph shows a comparison of flagged papers before and after the introduction of ChatGPT.")),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(
                id="date-comparison-graph-5",
                figure=px.bar(df_date_grouped_5, x='type', y='percentage', color='DateCategory',
                              color_discrete_sequence=colors_blind_friendly,
                              title="Percentage of Flagged Papers Before and After 1.1.2023 (CAU vs Other Universities)",
                              barmode='group',
                              labels={'type': 'Institution Type', 'percentage': 'Percentage of Papers',
                                      'DateCategory': 'Publication Date Category'})
            )),
        ], className="mb-5"),

        # Line graph for 2020-2024 flagged papers (Research Question 5)
        dbc.Row([
            dbc.Col(html.H4("Research Question 5: Flagged Papers for 2020-2024 (CAU vs Other Universities)"), width=6),
            dbc.Col(html.P(
                "This graph shows the percentage of flagged papers from 2020 to 2024, separated by institution type (CAU and other universities).")),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(
                id="year-comparison-graph-5-with-trend",
                figure=px.line(df_year_grouped_5, x='PubDate', y='percentage', color='type',
                               color_discrete_sequence=colors_blind_friendly,
                               title=title_with_p_value,  # Add p-value to the title
                               labels={'PubDate': 'Publication Year', 'percentage': 'Percentage of Papers',
                                       'type': 'Institution Type'})
                .add_scatter(x=df_year_grouped_5['PubDate'], y=df_year_grouped_5['trend'], mode='lines',
                             name='Trend Line')
                .update_layout(xaxis=dict(tickmode='linear', dtick=1))  # Set to display full years on the x-axis
                # Set to display whole years on the x-axis
            )),
        ], className="mb-5"),
        # Research Question 6: Faculty Differences at CAU
        dbc.Row([
            dbc.Col(html.H4("Research Question 6: Faculty Differences at CAU"), width=6),
            dbc.Col(html.P(
                "How has word usage changed across different faculties at CAU since the introduction of ChatGPT? "
                "This project analyzes differences between disciplines, such as natural sciences and humanities.")),
        ]),
        dbc.Row([

            html.Div(id='slider-RQ6', children=
            [dcc.Slider(id='RQ6-year-slider',
                        min=RQ_6_df['Year'].min(),
                        max=RQ_6_df['Year'].max(),
                        value=RQ_6_df['Year'].min(),
                        marks={str(year): str(year) for year in RQ_6_df['Year'].unique()},
                        step=None
                        )], style={'width': '50%', 'display': 'inline-block'}),
            # inline-block : to show slider and dropdown in the same line

            html.Div(id='dropdown-div', children=
            [dcc.Dropdown(id='RQ6-Keyword-dropdown',
                          options=[{'label': i, 'value': i} for i in np.append(['All'], RQ_6_df['Keyword'].unique())],
                          value='All'
                          )], style={'width': '50%', 'display': 'inline-block'}),

            dcc.Graph(id='RQ6-scatter')
        ]),

        # Interactive description for Research Question 7
        dbc.Row([dbc.Col(html.H4(
            "Research Question 7: How do the influences of ChatGPT on scientific papers differ between universities worldwide?"),
                         width=12)]),
        dbc.Row([dbc.Col(html.P(
            "Now you can explore this question interactively! Using the dropdown menu below, you can select combinations "
            "of different datasets (e.g., German Universities + Fachhochschule, EU + Asia) and compare the flagged papers between "
            "these institutions. Once you select a combination, two graphs will appear: a bar chart and a line chart displaying trends over time. "
            "By selecting different combinations, you can see how the influence of ChatGPT varies across regions and institutions. "
            "Feel free to experiment and discover insights!"
        ), width=12)]),
        dbc.Row([dbc.Col(dcc.Dropdown(
            id='dataset-combination-dropdown',
            options=[
                {'label': 'German University + Fachhochschule', 'value': 'df_combined_Uni_FH'},
                {'label': 'German University + Germany', 'value': 'df_combined_Uni_Germany'},
                {'label': 'German University + EU', 'value': 'df_combined_Uni_EU'},
                {'label': 'German University + Asia', 'value': 'df_combined_Uni_Asia'},
                {'label': 'German University + World', 'value': 'df_combined_Uni_World'},
                {'label': 'Fachhochschule + Germany', 'value': 'df_combined_FH_Germany'},
                {'label': 'Fachhochschule + EU', 'value': 'df_combined_FH_EU'},
                {'label': 'Fachhochschule + Asia', 'value': 'df_combined_FH_Asia'},
                {'label': 'Fachhochschule + World', 'value': 'df_combined_FH_World'},
                {'label': 'Germany + EU', 'value': 'df_combined_Germany_EU'},
                {'label': 'Germany + Asia', 'value': 'df_combined_Germany_Asia'},
                {'label': 'Germany + World', 'value': 'df_combined_Germany_World'},
                {'label': 'EU + Asia', 'value': 'df_combined_EU_Asia'},
                {'label': 'EU + World', 'value': 'df_combined_EU_World'},
                {'label': 'Asia + World', 'value': 'df_combined_Asia_World'}
            ],
            value='df_combined_EU_World',  # Default selection
            clearable=False
        ), width=12)]),

        dbc.Row([dbc.Col(dcc.Graph(id='comparison-bar-chart7'), width=12)]),
        dbc.Row([dbc.Col(dcc.Graph(id='comparison-line-chart7'), width=12)]),
    ], className="py-5")
])

# About Section
about_section = html.Div(id="about", children=[
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("About Me", style={"color": "#9b0a7d"}), className="mt-5 mb-4 text-center"),
        ]),
        dbc.Row([
            dbc.Col(html.P(
                "Thank you for exploring our Page\n"
                "This Date was presented by Louis Krückmeyer, Matheus Kolzarek and Tom Skrzynski-Fox.\n"
                "This project was created to explore the impact of ChatGPT on scientific papers. \n"
                "We hope you enjoyed the analysis and visualizations presented here. \n"
                "Thank you for the great support and feedback Mirjam Bayer"
            )),
        ], className="text-center"),
    ], className="py-5")
])
