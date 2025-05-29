# Qtok/src/qtok/qtoklib/report_generator.py

import os
import base64
from jinja2 import Template
import subprocess

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_html_report(output_folder, labels, stats_table, stats_table_p, unicode_table_p,
                         final_table_lat, final_table_cyr, unseen_tokens_lat, unseen_tokens_cyr):

    # Convert images to base64
    basic_stats_img = image_to_base64(os.path.join(output_folder, "basic_stats.png"))
    unicode_stats_img = image_to_base64(os.path.join(output_folder, "unicode_stats.png"))
    latin_stats_img = image_to_base64(os.path.join(output_folder, "latin_stats.png"))
    cyrillic_stats_img = image_to_base64(os.path.join(output_folder, "cyrillic_stats.png"))

    template = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qtok Analysis Report for {{ label }}</title>
    <style>
        :root {
            --primary-color: #3498db;
            --secondary-color: #2c3e50;
            --bg-color: #ecf0f1;
            --text-color: #333;
            --border-color: #bdc3c7;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--bg-color);
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background-color: var(--primary-color);
            color: white;
            text-align: center;
            padding: 1em 0;
            margin-bottom: 2em;
        }
        h1 {
            margin: 0;
            font-size: 2.5em;
        }
        h2 {
            color: var(--secondary-color);
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 0.5em;
            margin-top: 1.5em;
        }
        .card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 2em;
            overflow: hidden;
        }
        .card-header {
            background-color: var(--secondary-color);
            color: white;
            padding: 1em;
            font-size: 1.2em;
            font-weight: bold;
        }
        .card-body {
            padding: 1em;
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1em;
        }
        th, td {
            border: 1px solid var(--border-color);
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: var(--primary-color);
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 1em auto;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .small-font-table {
            font-size: 0.85em;
        }
        .small-font-table th,
        .small-font-table td {
            padding: 8px;
        }
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            h1 {
                font-size: 2em;
            }
            table {
                font-size: 0.9em;
            }
            .small-font-table {
                font-size: 0.75em;
            }
            .card-body {
                padding: 0.5em;
            }
            th, td {
                padding: 8px;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>Qtok Analysis Report</h1>
        <p>Data analysis for {{ label }}</p>
    </header>
    <div class="container">
        <div class="card">
            <div class="card-header">Basic Statistics</div>
            <div class="card-body">
                <img src="data:image/png;base64,{{ basic_stats_img }}" alt="Basic Statistics Chart">
                <div class="table-wrapper">
                    <table class="small-font-table">
                        <tr>
                            {% for header in stats_table_p[0] %}
                            <th>{{ header.replace("_", " ")|title }}</th>
                            {% endfor %}
                        </tr>
                        {% for row in stats_table_p[1:] %}
                        <tr>
                            {% for cell in row %}
                            <td>{{ cell }}</td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </table>
                </div>
                <div class="table-wrapper">
                    <table class="small-font-table">
                        <tr>
                            {% for header in stats_table[0] %}
                            <th>{{ header.replace("_", " ")|title }}</th>
                            {% endfor %}
                        </tr>
                        {% for row in stats_table[1:] %}
                        <tr>
                            {% for cell in row %}
                            <td>{{ cell }}</td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">Unicode Statistics</div>
            <div class="card-body">
                <img src="data:image/png;base64,{{ unicode_stats_img }}" alt="Unicode Statistics Chart">
                <div class="table-wrapper">
                    <table class="small-font-table">
                        <tr>
                            {% for header in unicode_table_p[0] %}
                            <th>{{ header.replace("_", " ")|title }}</th>
                            {% endfor %}
                        </tr>
                        {% for row in unicode_table_p[1:] %}
                        <tr>
                            {% for cell in row %}
                            <td>{{ cell }}</td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">Latin Language Statistics</div>
            <div class="card-body">
                <img src="data:image/png;base64,{{ latin_stats_img }}" alt="Latin Language Statistics Chart">
                <div class="table-wrapper">
                    <table>
                        <tr>
                            {% for header in final_table_lat[0] %}
                            <th>{{ header }}</th>
                            {% endfor %}
                        </tr>
                        {% for row in final_table_lat[1:] %}
                        <tr>
                            {% for cell in row %}
                            <td>{{ cell }}</td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">Cyrillic Language Statistics</div>
            <div class="card-body">
                <img src="data:image/png;base64,{{ cyrillic_stats_img }}" alt="Cyrillic Language Statistics Chart">
                <div class="table-wrapper">
                    <table>
                        <tr>
                            {% for header in final_table_cyr[0] %}
                            <th>{{ header }}</th>
                            {% endfor %}
                        </tr>
                        {% for row in final_table_cyr[1:] %}
                        <tr>
                            {% for cell in row %}
                            <td>{{ cell }}</td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """

    rendered_html = Template(template).render(
        label=", ".join(labels),
        stats_table_p=stats_table_p,
        unicode_table_p=unicode_table_p,
        final_table_lat=final_table_lat,
        final_table_cyr=final_table_cyr,
        stats_table=stats_table,
        basic_stats_img=basic_stats_img,
        unicode_stats_img=unicode_stats_img,
        latin_stats_img=latin_stats_img,
        cyrillic_stats_img=cyrillic_stats_img
    )

    with open(os.path.join(output_folder, 'report.html'), 'w', encoding='utf-8') as f:
        f.write(rendered_html)

def generate_latex_report(output_folder, labels, stats_table, stats_table_p, unicode_table_p,
                          final_table_lat, final_table_cyr, unseen_tokens_lat, unseen_tokens_cyr):
    latex_template = r"""
    \documentclass{article}
    \usepackage[utf8]{inputenc}
    \usepackage{graphicx}
    \usepackage{booktabs}
    \usepackage{longtable}
    \usepackage{array}
    \usepackage{pdflscape}
    \usepackage{geometry}
    \usepackage{caption}
    \usepackage{makecell}

    \geometry{margin=2cm}

    \title{Qtok Analysis Report for {{ labels|join(', ') }}}
    \author{Qtok}
    \date{\today}

    \begin{document}

    \maketitle

\section{Basic Statistics}

\begin{landscape}
\begin{figure}[p]
    \centering
    \includegraphics[width=\linewidth]{basic_stats.png}
    \caption{Basic Statistics Chart}
\end{figure}
\end{landscape}

\begin{landscape}
\begin{longtable}{@{}l*{ {{- stats_table_p[0]|length - 1 -}} }{r}@{}}
\caption{Basic Statistics (Percentage)} \\
\toprule
{% for header in stats_table_p[0] -%}
    \makecell{ {{ header }} }
    {% if not loop.last %} & {% endif %}
{%- endfor %} \\
\midrule
\endfirsthead
\multicolumn{ {{- stats_table_p[0]|length -}} }{c}%
{\tablename\ \thetable\ -- \textit{Continued from previous page}} \\
\toprule
{% for header in stats_table_p[0] -%}
    \makecell{ {{ header }} }
    {% if not loop.last %} & {% endif %}
{%- endfor %} \\
\midrule
\endhead
\midrule \multicolumn{ {{- stats_table_p[0]|length -}} }{r}{\textit{Continued on next page}} \\
\endfoot
\endlastfoot
{% for row in stats_table_p[1:] -%}
    {% for cell in row -%}
        {{ cell }} {% if not loop.last %} & {% endif %}
    {%- endfor %} \\
{% endfor %}
\bottomrule
\end{longtable}
\end{landscape}

\begin{landscape}
\begin{longtable}{@{}l*{ {{- stats_table[0]|length - 1 -}} }{r}@{}}
\caption{Basic Statistics (Absolute Values)} \\
\toprule
{% for header in stats_table[0] -%}
    \makecell{ {{ header }} }
    {% if not loop.last %} & {% endif %}
{%- endfor %} \\
\midrule
\endfirsthead
\multicolumn{ {{- stats_table[0]|length -}} }{c}%
{\tablename\ \thetable\ -- \textit{Continued from previous page}} \\
\toprule
{% for header in stats_table[0] -%}
    \makecell{ {{ header }} }
    {% if not loop.last %} & {% endif %}
{%- endfor %} \\
\midrule
\endhead
\midrule \multicolumn{ {{- stats_table[0]|length -}} }{r}{\textit{Continued on next page}} \\
\endfoot
\endlastfoot
{% for row in stats_table[1:] -%}
    {% for cell in row -%}
        {{ cell }} {% if not loop.last %} & {% endif %}
    {%- endfor %} \\
{% endfor %}
\bottomrule
\end{longtable}
\end{landscape}

\section{Unicode Statistics}

\begin{landscape}
\begin{figure}[p]
    \centering
    \includegraphics[width=\linewidth]{unicode_stats.png}
    \caption{Unicode Statistics Chart}
\end{figure}
\end{landscape}


\begin{landscape}
\begin{longtable}{@{}l*{ {{- unicode_table_p1[0]|length - 1 -}} }{r}@{}}
\caption{Unicode Statistics} \\
\toprule
{% for header in unicode_table_p1[0] -%}
    \makecell{ {{ header }} }
    {% if not loop.last %} & {% endif %}
{%- endfor %} \\
\midrule
\endfirsthead
\multicolumn{ {{- unicode_table_p1[0]|length -}} }{c}%
{\tablename\ \thetable\ -- \textit{Continued from previous page}} \\
\toprule
{% for header in unicode_table_p1[0] -%}
    \makecell{ {{ header }} }
    {% if not loop.last %} & {% endif %}
{%- endfor %} \\
\midrule
\endhead
\midrule \multicolumn{ {{- unicode_table_p1[0]|length -}} }{r}{\textit{Continued on next page}} \\
\endfoot
\endlastfoot
{% for row in unicode_table_p1[1:] -%}
    {% for cell in row -%}
        {{ cell }} {% if not loop.last %} & {% endif %}
    {%- endfor %} \\
{% endfor %}
\bottomrule
\end{longtable}
\end{landscape}

\begin{landscape}
\begin{longtable}{@{}l*{ {{- unicode_table_p2[0]|length - 1 -}} }{r}@{}}
\caption{Unicode Statistics} \\
\toprule
{% for header in unicode_table_p2[0] -%}
    \makecell{ {{ header }} }
    {% if not loop.last %} & {% endif %}
{%- endfor %} \\
\midrule
\endfirsthead
\multicolumn{ {{- unicode_table_p2[0]|length -}} }{c}%
{\tablename\ \thetable\ -- \textit{Continued from previous page}} \\
\toprule
{% for header in unicode_table_p2[0] -%}
    \makecell{ {{ header }} }
    {% if not loop.last %} & {% endif %}
{%- endfor %} \\
\midrule
\endhead
\midrule \multicolumn{ {{- unicode_table_p2[0]|length -}} }{r}{\textit{Continued on next page}} \\
\endfoot
\endlastfoot
{% for row in unicode_table_p2[1:] -%}
    {% for cell in row -%}
        {{ cell }} {% if not loop.last %} & {% endif %}
    {%- endfor %} \\
{% endfor %}
\bottomrule
\end{longtable}
\end{landscape}


\section{Latin Language Statistics}

\begin{landscape}
\begin{figure}[p]
    \centering
    \includegraphics[width=\linewidth]{latin_stats.png}
    \caption{Latin Language Statistics Chart}
\end{figure}
\end{landscape}

\begin{landscape}
\begin{longtable}{@{}l*{ {{- final_table_lat[0]|length - 1 -}} }{r}@{}}
\caption{Latin Language Statistics} \\
\toprule
{% for header in final_table_lat[0] -%}
    \makecell{ {{ header }} }
    {% if not loop.last %} & {% endif %}
{%- endfor %} \\
\midrule
\endfirsthead
\multicolumn{ {{- final_table_lat[0]|length -}} }{c}%
{\tablename\ \thetable\ -- \textit{Continued from previous page}} \\
\toprule
{% for header in final_table_lat[0] -%}
    \makecell{ {{ header }} }
    {% if not loop.last %} & {% endif %}
{%- endfor %} \\
\midrule
\endhead
\midrule \multicolumn{ {{- final_table_lat[0]|length -}} }{r}{\textit{Continued on next page}} \\
\endfoot
\endlastfoot
{% for row in final_table_lat[1:] -%}
    {% for cell in row -%}
        {{ cell }} {% if not loop.last %} & {% endif %}
    {%- endfor %} \\
{% endfor %}
\bottomrule
\end{longtable}
\end{landscape}

\section{Cyrillic Language Statistics}

\begin{landscape}
\begin{figure}[p]
    \centering
    \includegraphics[width=\linewidth]{cyrillic_stats.png}
    \caption{Cyrillic Language Statistics Chart}
\end{figure}
\end{landscape}

\begin{landscape}
\begin{longtable}{@{}l*{ {{- final_table_cyr[0]|length - 1 -}} }{r}@{}}
\caption{Cyrillic Language Statistics} \\
\toprule
{% for header in final_table_cyr[0] -%}
    \makecell{ {{ header }} }
    {% if not loop.last %} & {% endif %}
{%- endfor %} \\
\midrule
\endfirsthead
\multicolumn{ {{- final_table_cyr[0]|length -}} }{c}%
{\tablename\ \thetable\ -- \textit{Continued from previous page}} \\
\toprule
{% for header in final_table_cyr[0] -%}
    \makecell{ {{ header }} }
    {% if not loop.last %} & {% endif %}
{%- endfor %} \\
\midrule
\endhead
\midrule \multicolumn{ {{- final_table_cyr[0]|length -}} }{r}{\textit{Continued on next page}} \\
\endfoot
\endlastfoot
{% for row in final_table_cyr[1:] -%}
    {% for cell in row -%}
        {{ cell }} {% if not loop.last %} & {% endif %}
    {%- endfor %} \\
{% endfor %}
\bottomrule
\end{longtable}
\end{landscape}

    \end{document}
    """

    # Process table headers
    stats_table_p[0] = [r" \\ ".join(x.split("_")) for x in stats_table_p[0]]
    unicode_table_p[0] = [r" \\ ".join(x.split(" ")) for x in unicode_table_p[0]]
    final_table_lat[0] = [r" \\ ".join(x.split("_")) for x in final_table_lat[0]]
    final_table_cyr[0] = [r" \\ ".join(x.split("_")) for x in final_table_cyr[0]]
    stats_table[0] = [r" \\ ".join(x.split("_")) for x in stats_table[0]]

    # Split unicode table
    n = len(unicode_table_p[0])//2
    unicode_table_p1 = [unicode_table_p[0][:n]]
    unicode_table_p2 = [[unicode_table_p[0][0]] + list(unicode_table_p[0][n:])]
    for i in range(1, len(unicode_table_p)):
        unicode_table_p1.append(unicode_table_p[i][:n])
        unicode_table_p2.append([unicode_table_p[i][0]] + list(unicode_table_p[i][n:]))

    rendered_latex = Template(latex_template).render(
        labels=labels,
        stats_table_p=stats_table_p,
        unicode_table_p1=unicode_table_p1,
        unicode_table_p2=unicode_table_p2,
        final_table_lat=final_table_lat,
        final_table_cyr=final_table_cyr,
        stats_table=stats_table
    )

    with open(os.path.join(output_folder, 'report.tex'), 'w', encoding='utf-8') as f:
        f.write(rendered_latex)


    # Compile LaTeX to PDF
    # if subprocess.run(["pdflatex", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0: # ERROR HERE, DONT GO INSIDE IF PDFLATEX IS NOT INSTALLED
    #     print("pdflatex is not installed. Please install it and try again to generate the pdf report.")
    # else:
    #     subprocess.run(["pdflatex", "-output-directory", output_folder, os.path.join(output_folder, 'report.tex')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #     subprocess.run(["pdflatex", "-output-directory", output_folder, os.path.join(output_folder, 'report.tex')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Offer to change for this one:
    try:
        subprocess.run(["pdflatex", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pdflatex_success = True
    except Exception as e:
        pdflatex_success = False
        print(f"Error: {e}")
        print("pdflatex is not installed. Please install it and try again to generate the pdf report.")

    if pdflatex_success:
        subprocess.run(["pdflatex", "-output-directory", output_folder, os.path.join(output_folder, 'report.tex')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["pdflatex", "-output-directory", output_folder, os.path.join(output_folder, 'report.tex')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return pdflatex_success
