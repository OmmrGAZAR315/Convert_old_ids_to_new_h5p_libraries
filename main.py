import pandas as pd

last_id = input("Enter the last id: ")
isItTable_h5p_content = input("Is it table h5p_content? (y/n): ")
file_path = input("Enter the file path: ").strip('"')

data = pd.read_csv(file_path)

if isItTable_h5p_content == "y":
    query = "UPDATE h5p_contents \nSET library_id = CASE\n"
else:
    query = """
ALTER TABLE h5p_contents_libraries 
ADD version VARCHAR(3)
DEFAULT 'old';
"""
    query += """
ALTER TABLE `h5p_contents_libraries`
DROP PRIMARY KEY,
ADD PRIMARY KEY(
    `content_id`,
    `library_id`,
    `dependency_type`,
    `version`
);
"""
    query += """
UPDATE h5p_contents_libraries 
SET library_id = CASE
"""

# Iterate over each row in the data to construct the CASE statements
for _, row in data.iterrows():
    query += f"    WHEN library_id = {row['old_id']} THEN {row['new_id']}\n"

# Close the CASE statement and add the WHERE clause to filter based on old IDs
old_ids = ', '.join(map(str, data['old_id'].unique()))

query += f"END\n" + (",version = 'new'\n" if isItTable_h5p_content != "y" else "")

query += f"WHERE library_id IN ({old_ids})\n"

query += "AND " + ("id" if isItTable_h5p_content == "y" else f"content_id") + f" <= {last_id};\n"

if isItTable_h5p_content != "y":
    query += f"""
DELETE FROM h5p_contents_libraries
WHERE version = 'old'
AND content_id <= {last_id};\n
"""
    query += "ALTER TABLE `h5p_contents_libraries` DROP `version`;"

# Output the generated SQL query
output_file = f"{file_path}{'h5p_contents' if isItTable_h5p_content == 'y' else 'h5p_contents_libraries'}.txt"
with open(output_file, 'w') as file:
    file.write(query)

print(f"Extracted text saved to: {output_file}")
