import csv

start_number = 220001001
end_number = 220001086

# Define the CSV file name
csv_file = "Face_recognition/Attendance/templates/attendance.csv"

# Generate a list of integers
integers = list(range(start_number, end_number + 1))

# Write the integers to the CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows([[str(num)] for num in integers])

print(f"Integers from {start_number} to {end_number} have been written to {csv_file}")
    