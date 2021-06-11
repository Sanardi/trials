import unittest
from clinicaltrials import ClinicalTrials

class ClinicalTrialsTest(unittest.TestCase):
    """Test Class for testing Clinical Trials, 
    currently assumes you take the files that are in the directory by checking first entry.
    This could be extended to test different files if desired"""
       
    def setUp(self) -> None:
        self.clinicaltrials = ClinicalTrials()

    def tearDown(self) -> None:
        pass

    def test_prepare_drugs_file(self):
        """checking file is being loaded an return 1st line"""

        data_expected = 'propylthiouracil'
        df = self.clinicaltrials.prepare_drugs_file()
        data_received = df.iloc[0].itemLabel
        self.assertEqual(data_expected, data_received)

    #@unittest.skip("WIP")
    def test_prepare_trials_file(self):
        """checking file is being loaded and returns 1st line"""
        data_expected = 'NCT00293735'
        df = self.clinicaltrials.prepare_trials_file()
        data_received = df.iloc[0].nct_id
        self.assertEqual(data_expected, data_received)

    def test_clean_df_trials(self):
        data_expected = 'Drug'
        df = self.clinicaltrials.clean_df_trials()
        data_sample = df.intervention_type.sample(n=1).reset_index()
        data_received = data_sample['intervention_type']
        print(data_received)
        self.assertEqual(data_expected, data_received.any())

    @unittest.skip("WIP")    
    def test_is_consistent(self):
        self.phonebook.add("Bob", "12345")
        self.phonebook.add("Anna", "012345")
        self.assertTrue(self.phonebook.is_consistent())
    @unittest.skip("WIP")
    def test_inconsistent_with_duplicate_entries(self):
        self.phonebook.add("Bob", "12345")
        self.phonebook.add("Sue", "12345")
        self.assertFalse(self.phonebook.is_consistent())
    @unittest.skip("WIP")
    def test_inconsistent_with_different_prefixes(self):
        self.phonebook.add("Bob", "12345")
        self.phonebook.add("Sue", "123")
        self.assertFalse(self.phonebook.is_consistent())
    @unittest.skip("WIP")
    def test_phonebook_adds_names_and_numbers(self):
        self.phonebook.add("Richard", "09158")
        self.assertIn("Richard", self.phonebook.get_names())
        self.assertIn("09158", self.phonebook.get_numbers())


