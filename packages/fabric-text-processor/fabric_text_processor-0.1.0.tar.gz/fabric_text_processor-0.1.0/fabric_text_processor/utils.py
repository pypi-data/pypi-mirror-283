import os

def save_results(results: List[str], output_file: str):
    output_dir = os.path.dirname(output_file)
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write('\n\n'.join(results))
    print(f"\nProcessing completed. Output file: {output_file}")
