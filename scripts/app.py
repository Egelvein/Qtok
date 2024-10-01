import streamlit as st
import shutil
import os
import json
import plotly.express as px
import pandas as pd
from token_analysis import tokens_analyzer, tokens_analyzer_gguf, plot_stats
from model_downloader import download_model, load_tokenizer, TOKENIZER_TYPE


def gguf_tokenization(tokenizer_url, token):
    models = [
        {"name": "Model", "tokt": TOKENIZER_TYPE.SPM, "repo": tokenizer_url, },
        {"name": "Model", "tokt": TOKENIZER_TYPE.BPE, "repo": tokenizer_url, },
        {"name": "Model", "tokt": TOKENIZER_TYPE.WPM, "repo": tokenizer_url, }
    ]
    if os.path.exists("models/tokenizers/Model"):
        shutil.rmtree("models/tokenizers/Model")

    for model in models:
        try:
            download_model(model, token)
        except Exception as e:
            continue

    tokenizer = None
    for model in models:
        name = model["name"]
        tokt = model["tokt"]

        if tokt == TOKENIZER_TYPE.SPM:
            continue

        if not os.path.exists(f"models/tokenizers/{name}"):
            continue

        try:
            tokenizer = load_tokenizer(name)
            # tokenizer = AutoTokenizer.from_pretrained(f"models/tokenizers/{name}")
        except OSError as e:
            print(f"Failed to load tokenizer. Error: {e}")
            continue
    result = tokens_analyzer_gguf(tokenizer)
    return result


def main():
    st.title("Token Distribution Map")

    token = st.text_input("Enter token:")
    tokenizer_url = st.text_input("Enter tokenizer URL:")

    # @st.cache_data
    def load_geojson():
        with open('countries.geo.json') as f:
            return json.load(f)

    geojson_data = load_geojson()

    if st.button("Analyze Tokens"):
        if token and tokenizer_url:
            with st.spinner("Analyzing tokens, please wait..."):
                try:
                    result, length_one_distribution, vocab_stats, tokenizer_metrics = tokens_analyzer(tokenizer_url, token)
                    df_result = pd.DataFrame(result)
                    # print(df_result)
                    # print("OK1")
                    # print(length_one_distribution)
                    length_one_distribution_result = pd.DataFrame(length_one_distribution)
                    # print(df_result)
                    # print("OK2")
                    tokenizer_metrics_df = pd.DataFrame(tokenizer_metrics, index=["Tokenizer"])
                except:
                    result, length_one_distribution, vocab_stats, tokenizer_metrics = gguf_tokenization(tokenizer_url, token)
                    df_result = pd.DataFrame(result)
                    # print(length_one_distribution)
                    length_one_distribution_result = pd.DataFrame(length_one_distribution)
                    # print(df_result)
                    # print("OK2")
                    tokenizer_metrics_df = pd.DataFrame(tokenizer_metrics, index=["Tokenizer"])
                all_countries = pd.DataFrame([feature['properties']['name'] for feature in geojson_data['features']],
                                             columns=['Country'])
                df_result = pd.merge(all_countries, df_result, on='Country', how='left').fillna(0)
                df_result['highlight'] = df_result['Number of tokens'] > 0

                fig = px.choropleth(
                    df_result,
                    geojson=geojson_data,
                    locations="Country",
                    featureidkey="properties.name",
                    color="Number of tokens",
                    hover_name="Country",
                    # color_continuous_scale=px.colors.sequential.Blues,
                    color_continuous_scale=[
                        [0, "lightgrey"],
                        [0.00001, "blue"],
                        [1.0, "red"]
                    ],
                )
                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(
                    geo=dict(
                        showframe=False,
                        showcoastlines=False,
                        projection_type='equirectangular'
                    ),
                    margin={"r":0,"t":0,"l":0,"b":0}
                )
                st.plotly_chart(fig, use_container_width=True, width=1200, height=1200)

                length_one_distribution_result = pd.merge(all_countries, length_one_distribution_result, on='Country', how='left').fillna(0)
                length_one_distribution_result['highlight'] = length_one_distribution_result['Number of tokens'] > 0

                fig_2 = px.choropleth(
                    length_one_distribution_result,
                    geojson=geojson_data,
                    locations="Country",
                    featureidkey="properties.name",
                    color="Number of tokens",
                    hover_name="Country",
                    # color_continuous_scale=px.colors.sequential.Blues,
                    color_continuous_scale=[
                        [0, "lightgrey"],
                        [0.00001, "blue"],
                        [1.0, "red"]
                    ],
                )
                fig_2.update_geos(fitbounds="locations", visible=False)
                fig_2.update_layout(
                    geo=dict(
                        showframe=False,
                        showcoastlines=False,
                        projection_type='equirectangular'
                    ),
                    margin={"r": 0, "t": 0, "l": 0, "b": 0}
                )
                st.plotly_chart(fig_2, use_container_width=True, width=1200, height=1200)

                plot_stats(vocab_stats)

                st.dataframe(tokenizer_metrics_df)


if __name__ == "__main__":
    main()
