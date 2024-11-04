import streamlit as st
import csv
from io import StringIO


# Function to generate the numbered file
def generate_numbered_file(name: str, column_count: int, num_range: range, aligned=False):
    # Adjust the range to include the stop value
    num_range = range(num_range.start, num_range.stop + 1)

    # Determine the maximum length based on the largest number in the range
    max_length = len(str(num_range[-1]))

    # Use StringIO to capture file output in memory
    output = StringIO()
    writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    # Write the column headers dynamically based on column_count
    headers = [f'No.{i + 1}' for i in range(column_count)]
    writer.writerow(headers)

    # Prepare and write each row
    row = []
    for i in num_range:
        # Pad the number with leading zeros if aligned is True
        number = str(i).zfill(max_length) if aligned else str(i)
        row.append(number)

        # Once row reaches column_count, write it and reset row
        if len(row) == column_count:
            writer.writerow(row)
            row = []

    # Write any remaining numbers in the last row if row is not empty
    if row:
        writer.writerow(row)

    # Move to start of the StringIO object to read contents
    output.seek(0)
    return output.getvalue()


# Streamlit interface
st.markdown('### Print Merge Generator for Corel Draw\n'
            '_Copyright (©) Keller Hydle_')

# Input fields
name = st.text_input('Enter the file name (with extension)', 'output.txt')
column_count = st.number_input('Number of columns', min_value=1, value=1)
range_start = st.number_input('Range start', min_value=1, value=1)
range_stop = st.number_input('Range stop', min_value=1, value=100)
aligned = st.checkbox('Align numbers with leading zeros')

# Generate file when the button is clicked
if st.button('Generate File'):
    # Generate file content
    file_content = generate_numbered_file(name, int(column_count), range(int(range_start), int(range_stop) + 1),
                                          aligned)

    # Provide download button for the generated file
    st.download_button(
        label='Download File',
        data=file_content,
        file_name=name,
        mime='text/csv'
    )
