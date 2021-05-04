import sys
import os
import convert_to_excel

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        input_path = "."
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        output_path = os.path.join(input_path,"output")

    print(f"input: {input_path}")
    print(f"output: {output_path}")
    with os.scandir(input_path) as entries:
        for entry in entries:
            if entry.is_file():
                print(f"processing {entry.name}")
                filename = os.path.join(input_path,entry.name)
                convert_to_excel.process_file(filename,output_path)

