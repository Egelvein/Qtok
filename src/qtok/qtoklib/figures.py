import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

colors = [
    '#5da3ce', '#ffa347', '#6fbf58', '#e77f80', '#b28ac9',
    '#aa7c70', '#ec9ad3', '#a6a6a6', '#cece58', '#5ad0dc',
    '#6b6da1', '#82996a', '#b69b5d', '#ab5e5c', '#5da3ce',
    '#ffa347', '#6fbf58', '#e77f80', '#b28ac9', '#aa7c70',
    '#ec9ad3', '#a6a6a6', '#cece58', '#5ad0dc', '#6b6da1',
    '#82996a', '#b69b5d', '#ab5e5c'
]

markers = ['o', 's', '^', 'D', 'v', 'P', '*', 'X', '<', '>', 'h', 'd', '8', 'H']
markers += reversed(markers)

def plot_with_distinct_markers_and_colors(labels, file_path, output_image_file):
    data_normalized = pd.read_csv(file_path, sep="\t")

    parameters = [param.replace('_', ' ') for param in data_normalized.columns[1:]]
    x = np.arange(len(parameters))
    fig, ax = plt.subplots(figsize=(15, 10))

    tokenizers = data_normalized['Tokenizer'].unique()
    num_tokenizers = len(tokenizers)

    if num_tokenizers > len(colors):
        raise ValueError(f"The number of tokenizers ({num_tokenizers}) exceeds the available number of colors ({len(colors)}). Please add more colors.")
    if num_tokenizers > len(markers):
        raise ValueError(f"The number of tokenizers ({num_tokenizers}) exceeds the available number of markers ({len(markers)}). Please add more markers.")

    tokenizer_styles = {}
    for i, tokenizer in enumerate(tokenizers):
        tokenizer_styles[tokenizer] = {
            'color': colors[i],
            'marker': markers[i],
            'label': tokenizer
        }

    for tokenizer in tokenizers:
        values = data_normalized[data_normalized['Tokenizer'] == tokenizer].values[0][1:]
        std_dev = np.std(values) / np.sqrt(len(values))
        style = tokenizer_styles[tokenizer]

        ax.errorbar(
            x,
            values,
            fmt=style['marker'],
            color=style['color'],
            capsize=5,
            label=style['label'],
            markersize=8
        )

    ax.set_xticks(x)
    ax.set_xticklabels(parameters, rotation=45, ha="right")

    ax.set_ylabel("Normalized Value (%)")

    if 'Qtok' in tokenizers:
        joined_data = data_normalized[data_normalized['Tokenizer'] == 'Qtok'].values[0][1:]
        tokenizer_styles['Qtok'] = {
            'color': '#a6cee3',
            'marker': 'o',
            'label': 'Qtok'
        }
        for i, (xi, yi) in enumerate(zip(x, joined_data)):
            ax.plot(xi, yi, marker='o', markersize=12, markeredgecolor='black',
                    markerfacecolor='#a6cee3', linestyle='None', zorder=8)

    for label in labels:
        if label in tokenizers and label != 'Qtok':
            joined_data = data_normalized[data_normalized['Tokenizer'] == label].values[0][1:]
            tokenizer_styles[label] = {
                'color': '#e77f80',
                'marker': 'o',
                'label': label
            }
            for i, (xi, yi) in enumerate(zip(x, joined_data)):
                ax.plot(xi, yi, marker='o', markersize=12, markeredgecolor='black',
                        markerfacecolor='#e77f80', linestyle='None', zorder=12)

    handles, labels_legend = ax.get_legend_handles_labels()

    if 'Qtok' in tokenizer_styles:
        joined_style = tokenizer_styles['Qtok']
        joined_marker = plt.Line2D([0], [0], marker='o', color='w',
                                   markerfacecolor=joined_style['color'],
                                   markeredgecolor='black', markersize=8, label=joined_style['label'])
        handles.append(joined_marker)
        labels_legend.append('Qtok')

    for label in labels:
        if label in tokenizer_styles and label != 'Qtok':
            joined_style = tokenizer_styles[label]
            joined_marker = plt.Line2D([0], [0], marker='o', color='w',
                                       markerfacecolor=joined_style['color'],
                                       markeredgecolor='black', markersize=12, label=joined_style['label'])
            handles.append(joined_marker)
            labels_legend.append(label)

    handles = handles[1:]
    labels_legend = labels_legend[1:]

    ax.legend(handles=handles, labels=labels_legend, title='Tokenizer', bbox_to_anchor=(1.05, 1), loc='upper left')

    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.2f}'))

    plt.tight_layout()
    plt.savefig(output_image_file, format='png', bbox_inches='tight')
