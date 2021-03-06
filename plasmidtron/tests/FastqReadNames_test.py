import unittest
import os
from plasmidtron.FastqReadNames import FastqReadNames

test_modules_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(test_modules_dir, 'data','fastqreadnames')

class TestSpreadsheetParser(unittest.TestCase):
	
	def test_invalid_input_file(self):
		i = FastqReadNames(os.path.join(data_dir, 'file_which_doesnt_exist'), 'output')
		with self.assertRaises(Exception):
			i.extract_readnames_from_fastq()
		
	def test_valid_input_file(self):
		f = FastqReadNames(os.path.join(data_dir, 'valid.fastq'), os.path.join(data_dir, 'output_file'))
		f.extract_readnames_from_fastq()
		
		with open(f.output_readnames_file, 'r') as actual_file:
			actual_config_content = actual_file.read()
			self.assertEqual(actual_config_content, """\
IL9_4021:8:1:8:1892#7/1
IL9_4021:8:1:8:1892#7/2
IL9_4021:8:1:9:1658#7/1
IL9_4021:8:1:9:1658#7/2
IL9_4021:8:1:9:1626#7/1
IL9_4021:8:1:9:1626#7/2
""")
		os.remove(os.path.join(data_dir, 'output_file'))
		