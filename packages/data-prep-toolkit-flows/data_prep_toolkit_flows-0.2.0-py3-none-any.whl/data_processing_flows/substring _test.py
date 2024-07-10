path = '/Users/home/foo/input_guf/path/to/f.parquet'

input_folder = '/test-data/input/wdu_pdf2md/1_file'
output_folder = '/tmp/wdu_pdf2md'

indx = path.find(input_folder)
print(indx)
suffix = path[indx+len(input_folder):]
print(output_folder + suffix)