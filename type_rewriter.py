#!/usr/bin/env python

import os

package_directory = os.path.dirname(os.path.abspath(__file__))

function_type_extractor_binary_path = os.path.join(package_directory, 'function_type_extractor')
extra_include_path = os.path.join(package_directory, 'include')
extra_include_arg = '{}{}'.format('-I', extra_include_path)


# Debug
test_file_path = os.path.join(package_directory, 'test.h')
print(function_type_extractor_binary_path)
# /Debug

if __name__ == '__main__':
  import argparse
  import subprocess

  parser = argparse.ArgumentParser()
  parser.add_argument('--input-header', help = 'input header path for the type extractor tool', required = True)
  parser.add_argument('--output-header', help = 'output header path for the type extractor tool', required = True)

  args = parser.parse_args()

  input_header_path = os.path.abspath(args.input_header)
  output_header_path = os.path.abspath(args.output_header)

  # Debug
  print('input header path: {}'.format(input_header_path))
  print('output header path: {}'.format(output_header_path))
  # /Debug

  #resolved_types = subprocess.check_output([function_type_extractor_binary_path, '-extra-arg', '-Iinclude', 'tmp.h', '--']).decode('utf-8')
  #resolved_types = subprocess.check_output([function_type_extractor_binary_path, '-extra-arg', extra_include_arg, test_file_path, '--']).decode('utf-8')
  resolved_types = subprocess.check_output([function_type_extractor_binary_path, '-extra-arg', extra_include_arg, input_header_path, '--']).decode('utf-8')

  with open(output_header_path, 'w') as tmp_file:
    tmp_file.write(resolved_types)
