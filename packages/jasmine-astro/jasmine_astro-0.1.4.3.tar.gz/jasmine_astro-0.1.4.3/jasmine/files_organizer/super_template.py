def process_file(input_file, output_file, *,
                 new_mass_ratio=None,
                 new_separation=None,
                 new_rho=None):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            stripped_line = line.strip()
            if stripped_line:
                values = stripped_line.split()
                # Write the original line
                outfile.write('\t'.join(values) + '\n')
                if new_mass_ratio is not None:
                    if len(values) > 1:
                        values[1] = new_mass_ratio
                        outfile.write('\t'.join(values) + '\n')
                if new_separation is not None:
                    if len(values) > 1:
                        values[0] = new_separation
                        outfile.write('\t'.join(values) + '\n')
                if new_rho is not None:
                    if len(values) > 1:
                        values[4] = new_separation
                        outfile.write('\t'.join(values) + '\n')



root_path = '/Users/stela/Documents/Scripts/RTModel_project/RTModel/RTModel/data/'
input_file_path = root_path + 'TemplateLibrary.txt'
output_file_path = root_path + 'TemplateLibrary_SIS.txt'
# Run the function
process_file(input_file_path, output_file_path, new_mass_ratio='0.0001')