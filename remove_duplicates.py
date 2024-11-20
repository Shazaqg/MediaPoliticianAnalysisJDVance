import csv
from collections import OrderedDict

def remove_duplicates(input_file, output_file):
    # Read the CSV file and store unique rows
    unique_rows = OrderedDict()
    print("unique_rows: ", len(unique_rows))
    
    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile)
        headers = next(reader)  # Read the header row
        
        for row in reader:
            # Convert the row to a tuple so it can be used as a dictionary key
            row_tuple = tuple(row)
            unique_rows[row_tuple] = None  # Using None as a placeholder value
    
    # Write the unique rows to the output file
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)  # Write the header row
        writer.writerows(unique_rows.keys())  # Write the unique rows

    print(f"Duplicates removed. Result saved to {output_file}")

# Example usage
input_file = 'articles.csv'  # Replace with your input file name
output_file = 'no_dupes_test.csv'  # Replace with your desired output file name

remove_duplicates(input_file, output_file)