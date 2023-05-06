"""Provide plots function for data analyze."""

import matplotlib.pyplot as plt
from wordcloud import WordCloud


def generate_cloud(data):
    """This function generates word clouds for different groups of data.

    Args:
        data: A pandas DataFrame containing the data to be plotted.

    Returns:
        None.
    """
    text = ' '.join(data)

    wordcloud = WordCloud(width=800, height=800, background_color='white').generate(text)

    # Display the word cloud
    plt.figure(figsize=(8, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


def plot_clouds(data=None):
    """This function groups the data by different columns and generates word clouds for each group.

    Args:
        data: A pandas DataFrame containing the data to be plotted.

    Returns:
        None.
    """
    # Group the data by different columns
    data.groupby(['test_codes', 'base_tf', 'base_ea'], axis=0)

    code_group = data.groupby(['test_codes'], as_index=False).size().sort_values(by='size', ascending=False)
    code_group['test_codes'] = code_group['test_codes'].str.replace('000', '')

    tf_group = data.groupby(['base_tf'], as_index=False).size().sort_values(by='size', ascending=False)
    tf_group['base_tf'] = (tf_group['base_tf'] / 60).astype(int).astype(str) + 'm'

    base_group = data.groupby(['base_ea'], as_index=False).size().sort_values(by='size', ascending=False)

    # Generate word clouds for each group
    generate_cloud(code_group['test_codes'])
    generate_cloud(tf_group['base_tf'])
    generate_cloud(base_group['base_ea'])
