# import csv module
import csv
import sys
sys.path.append(".")

# csv file name
filename = "Track_Resources\\PLC_Folder_Generator\\RedLine.csv"

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


with open(filename, mode = 'r')as file:
    csvFile = csv.reader(file)

    # extract field names
    fields = next(csvFile)

    # extract data
    for row in csvFile:
        rows.append(row[:3])

    # convert from letter
    rows2 = convert_second_element_to_number_list(rows)

    # output file

    # create list for wayside
    wayside_made = []

    # iterate through waysides
    for i in rows2:
        Wayside_Number = i[1]

        # create a new wayside output file based on color
        if 'Red' in [i[0]]:
            LINCO = 0
            output = f"Track_Resources\\PLC_Folder_Generator\\PLC_RD_WS" + str(i[1])+ ".txt"
        elif 'Green' in [i[0]]:
            LINCO = 1
            output = f"Track_Resources\\PLC_Folder_Generator\\PLC_GR_WS" + str(i[1]) + ".txt"
        else:
            exit(-1)

        # check if Wayside made already, and if so append
        if Wayside_Number in wayside_made:
            with open(output, mode = 'a', newline="")as old:
                Ap = csv.writer(old, delimiter='"')
                # Write Block Info
                Ap.writerow(["BLK_START"])

                Block_Number = i[2]
                binary_block = format(int(Block_Number), '08b')[-8:]

                # Write
                Ap.writerow([f"BK001 {binary_block[7]}"])
                Ap.writerow([f"BK002 {binary_block[6]}"])
                Ap.writerow([f"BK004 {binary_block[5]}"])
                Ap.writerow([f"BK008 {binary_block[4]}"])
                Ap.writerow([f"BK0016 {binary_block[3]}"])
                Ap.writerow([f"BK0032 {binary_block[2]}"])
                Ap.writerow([f"BK0064 {binary_block[1]}"])
                Ap.writerow([f"BK0128 {binary_block[0]}"])

                # Write block info
                Ap.writerow(["SWITC 0"])
                Ap.writerow(["TRAFF 0"])
                Ap.writerow(["CROSS 0"])

                # end block
                Ap.writerow(["BLK_END"])
                continue
            
    
        # unique wayside - add to dictionary
        wayside_made.append(i[1])

        # open file
        with open(output, mode = 'w', newline="")as outfile:
            Out = csv.writer(outfile, delimiter='"')
            # WRITE LINE 1
            Out.writerow(["LN_START"])

            # WRITE LINE color
            Out.writerow([f"LINCO {LINCO}"])

            # write line 3
            Out.writerow(["LN_END"])

            # Write line 4
            Out.writerow(["WS_START"])

            # find Wayside info
            binary_wayside = format(Wayside_Number, '05b')[-5:]

            # Write Wayside info
            Out.writerow([f"WS001 {binary_wayside[4]}"])
            Out.writerow([f"WS002 {binary_wayside[3]}"])
            Out.writerow([f"WS004 {binary_wayside[2]}"])
            Out.writerow([f"WS008 {binary_wayside[1]}"])
            Out.writerow([f"WS0016 {binary_wayside[0]}"])

            Out.writerow(["WS_END"])

            # Write Block Info
            Out.writerow(["BLK_START"])

            Block_Number = i[2]
            binary_block = format(int(Block_Number), '08b')[-8:]

            # Write
            Out.writerow([f"BK001 {binary_block[7]}"])
            Out.writerow([f"BK002 {binary_block[6]}"])
            Out.writerow([f"BK004 {binary_block[5]}"])
            Out.writerow([f"BK008 {binary_block[4]}"])
            Out.writerow([f"BK0016 {binary_block[3]}"])
            Out.writerow([f"BK0032 {binary_block[2]}"])
            Out.writerow([f"BK0064 {binary_block[1]}"])
            Out.writerow([f"BK0128 {binary_block[0]}"])

            # Write block info
            Out.writerow(["SWITC 0"])
            Out.writerow(["TRAFF 0"])
            Out.writerow(["CROSS 0"])

            # end block
            Out.writerow(["BLK_END"])

            





    
    
