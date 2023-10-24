# import csv module
import csv

# csv file name
filename = "RedLine.csv"
output = "RedLineOutput.txt"

# set up letter converter
def letter_to_number(letter):
    letter = letter.upper()  # Convert the letter to uppercase if it's not already
    if 'A' <= letter <= 'Z':
        return ord(letter) - ord('A') + 1
    else:
        return None  # Return None for non-alphabet characters

def convert_second_element_to_number_list(lst):
    result = []

    for inner_list in lst:
        if len(inner_list) >= 2 and isinstance(inner_list[1], str) and inner_list[1].isalpha():
            inner_list[1] = letter_to_number(inner_list[1])
        result.append(inner_list)

    return result

#initalize title and rows
fields = []
rows = []


with open(filename, mode = 'r')as file, open(output, mode = 'w', newline='') as f:
    csvFile = csv.reader(file)
    output = csv.writer(f)

    # extract field names
    fields = next(csvFile)

    # extract data
    for row in csvFile:
        rows.append(row[:3])

    # convert from letter
    rows2 = convert_second_element_to_number_list(rows)

    # output file
    #output.writerows(rows2)
    print(rows2[0])
    # get color 
    if 'Red' in [l[0] for l in rows2]:
        LINCO = 0
    # elif rows2[0].lower() == "green":
    #    LINCO = 1
    else:
        LINCO = 3
    # WRITE LINE 1 
    output.writerow(["LN_INF_START"])

    # WRITE LINE 2
    output.writerow([f"\tLINCO - {LINCO}"])
    
    # Write Line 3
    output.writerow(["LN_INF_END"])

    #Write line 4
    output.writerow(["WS_INF_START"])

    # write Wayside info


    
