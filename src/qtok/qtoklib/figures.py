import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

colors = [
    '#5da3ce', '#ffa347', '#6fbf58', '#e77f80', '#b28ac9',
    '#aa7c70', '#ec9ad3', '#a6a6a6', '#cece58', '#5ad0dc',
    '#6b6da1', '#82996a', '#b69b5d', '#ab5c5c', '#5da3ce',
    '#ffa347', '#6fbf58', '#e77f80', '#b28ac9', '#aa7c70',
    '#ec9ad3', '#a6a6a6', '#cece58', '#5ad0dc', '#6b6da1',
    '#82996a', '#b69b5d', '#ab5c5c'
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

    # Добавление меток для Qtok с большой иконкой
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

    # Добавление меток для других токенизаторов
    for label in labels:
        if label in tokenizers and label != 'Qtok':
            joined_data = data_normalized[data_normalized['Tokenizer'] == label].values[0][1:]
            style = tokenizer_styles[label]
            for i, (xi, yi) in enumerate(zip(x, joined_data)):
                ax.plot(xi, yi, marker=style['marker'], markersize=12, markeredgecolor='black',
                        markerfacecolor=style['color'], linestyle='None', zorder=12)

    handles, labels_legend = ax.get_legend_handles_labels()

    # Удаление дублирующихся меток
    unique_labels = []
    unique_handles = []
    for handle, label in zip(handles, labels_legend):
        if label not in unique_labels:
            unique_labels.append(label)
            unique_handles.append(handle)

    ax.legend(handles=unique_handles, labels=unique_labels, title='Tokenizer', bbox_to_anchor=(1.05, 1), loc='upper left')

    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.2f}'))

    plt.tight_layout()
    plt.savefig(output_image_file, format='png', bbox_inches='tight')
