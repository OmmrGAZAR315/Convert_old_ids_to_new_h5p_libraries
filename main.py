import pandas as pd

last_id = input("Enter the last id: ")
# Load CSV data into a pandas DataFrame
file_path = 'C:\\Users\\omara\\Downloads\\mfisg.csv'  # Replace with the actual path to your CSV file
data = pd.read_csv(file_path)

# Start constructing the SQL query
query = "UPDATE h5p_contents_libraries\nSET id = CASE \n"

# Iterate over each row in the data to construct the CASE statements
for _, row in data.iterrows():
    query += f"    WHEN id = {row['old_id']} THEN {row['new_id']}\n"

# Close the CASE statement and add the WHERE clause to filter based on old IDs
old_ids = ', '.join(map(str, data['old_id'].unique()))
query += f"END\nWHERE id IN ({old_ids})"

query+= f",\n and content_id <= {last_id}; \n"

# Output the generated SQL query
with open(file_path+".txt", 'w') as file:
    file.write(query)
print(f"Extracted text saved to: {file_path}.txt")
