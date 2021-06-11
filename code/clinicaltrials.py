#author: Marzia Catherine Azam

import pandas as pd
import json


class ClinicalTrials:
    """Takes 3 files: usan_stems.csv, drugs.csv and clinical_trials2015.jsonl
     and performs various aggregations and calculation as well as returns selected json output.
     Choose method named after task to get the desired output.
     """
    def __init__(self, drugs_file="drugs.csv", 
                trials_file="clinical_trials_2015.jsonl", 
                usan_file="usan_stems.csv"):
        self.drugs = drugs_file
        self.trials = trials_file
        self.usan = usan_file

    def prepare_drugs_file(self):
        df = pd.read_csv(self.drugs)
        df['alternatives'] = df['itemLabel'] + "|" + df['altLabel_list'] 
        df['alternatives'] = df['alternatives'].str.lower().str.split('|')
        #print(df.head())
        return df

    def prepare_trials_file(self):
        df = pd.read_json(self.trials, lines=True)
        print("reading in trials json file")
        return df

    def select_only_drug_trials(self):
        """I filtered by intervention type drug here I was not 
        expecting to find matches in the other categories. 
        This can easily be changed with the following olumn if required."""
        df = self.prepare_trials_file()
        df_drug_trials = df[df['intervention_type'] == "Drug"]
        print("selecting drug trials only")
        return df_drug_trials

    def clean_df_trials(self):
        df_drug_trials = self.select_only_drug_trials()
        df_drug_trials['intervention_name'] = df_drug_trials['intervention_name'].str.lower()
        df_drug_trials['matches'] = df_drug_trials['intervention_name']
        words_to_remove = ["and", "intravenous", "or", "+", "-", "/", r"\(.*\)"]
        for item in words_to_remove:
            df_drug_trials['matches'] = df_drug_trials['matches'].str.replace(item,"", regex=False)

        df_drug_trials['matches'] = df_drug_trials['matches'].str.lower().str.split(',')
        return df_drug_trials

    def _match_drugs(self, matches, df):
        """iterates over the full list of drugs available in drugs.csv, and
        cleaned using regex and string replace methods. Will return the first
        value of the list, as this is the value from 'itemLabel' in drugs.csv """
        print("matching drugs")
        drugs_list = list(df['alternatives'])
        match = ""
        for item in matches:
            for sublist in drugs_list:
                if item not in sublist:
                    continue
                else:
                    match += sublist[0]
                    continue
        return match

    def match_trials_with_drugs(self,):
        df = self.clean_df_trials()
        df_drugs = self.prepare_drugs_file()
        df['drugs'] = df['matches'].apply(self._match_drugs, df=df_drugs)
        df = df[df['drugs'] != ""]
        df_output = df[['nct_id', 'drugs']]
        output_dict_nct = dict(zip(df_output.nct_id, df_output.drugs))
        with open("task1.json", "w") as outfile: 
            json.dump(output_dict_nct, outfile)
        return output_dict_nct


if __name__ == "__main__":
    print("running")
    test = ClinicalTrials()
    test.match_trials_with_drugs()