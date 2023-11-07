import time
import functools
from collections import Counter
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-interactive mode
import matplotlib.pyplot as plt

# Decorator to measure execution time of a function
def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return execution_time
    return wrapper

# Read Shakespeare's artwork
def read_shakespeare_text(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Count words using a dictionary
@timing_decorator
def count_words_dict(text):
    word_count = {}
    words = text.split()
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return word_count

# Count words using Counter
@timing_decorator
def count_words_counter(text):
    words = text.split()
    return Counter(words)

if __name__ == '__main':
    shakespeare_text = read_shakespeare_text('t8.shakespeare.txt')
    
    # Perform the experiment 100 times
    num_experiments = 100
    execution_times_dict = []
    execution_times_counter = []

    for _ in range(num_experiments):
        execution_times_dict.append(count_words_dict(shakespeare_text))
        execution_times_counter.append(count_words_counter(shakespeare_text))

    # Plot the distribution of execution times
    plt.hist(execution_times_dict, bins=20, label='Using Dictionary', alpha=0.5)
    plt.hist(execution_times_counter, bins=20, label='Using Counter', alpha=0.5)
    plt.xlabel('Execution Time (seconds)')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')

    plt.savefig('C:/Users/admin/downloads')  # Save the graph to a file

    plt.show()

