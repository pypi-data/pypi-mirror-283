import re

import langid


def split_text_with_overlap(text, segment_length, overlap_length):
    """
    Splits English text into segments with a specified overlap length.

    Parameters:
    text (str): The input text to be split.
    segment_length (int): The length of each segment.
    overlap_length (int): The number of words that overlap between segments.

    Returns:
    list: A list of text segments.

    Raises:
    ValueError: If the input text is not in English.
    ValueError: If segment_length or overlap_length are not positive integers.
    """

    # Check if segment_length and overlap_length are positive integers
    if not isinstance(segment_length, int) or segment_length <= 0:
        raise ValueError("segment_length must be a positive integer.")
    if not isinstance(overlap_length, int) or overlap_length < 0:
        raise ValueError("overlap_length must be a non-negative integer.")

    # Detect the language of the text
    lang, confidence = langid.classify(text)
    if lang != 'en':
        raise ValueError("The text is not in English.")

    # Clean the text, keeping only letters and spaces
    text = re.sub(r'[^A-Za-z\s]', '', text)

    # Split the text into words
    words = text.split()

    # Handle cases where text is too short
    if len(words) == 0:
        return []
    if segment_length > len(words):
        return [' '.join(words)]

    # Split the text into segments with overlap
    segments = []
    start = 0
    while start < len(words):
        end = start + segment_length
        segments.append(' '.join(words[start:end]))
        start = end - overlap_length  # Move start to end - overlap_length

    return segments


if __name__ == '__main__':

    # Example usage
    text = "This is an example text to demonstrate the function. This function will split this text into segments with specified overlap."
    try:
        segments = split_text_with_overlap(text, 5, 2)
        for i, segment in enumerate(segments):
            print(f"Segment {i + 1}: {segment}")
    except ValueError as e:
        print(e)
