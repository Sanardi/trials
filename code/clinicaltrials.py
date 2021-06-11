#author: Marzia Catherine Azam
import numpy as np
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
        words_to_remove = ["and", "intravenous", "+", "- ", "/", r"\(.*\)", "®", " or"]
        for item in words_to_remove:
            df_drug_trials['matches'] = df_drug_trials['matches'].str.replace(item,",")

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

    def match_trials_with_drugs(self):
        df = self.clean_df_trials()
        df_drugs = self.prepare_drugs_file()
        df['drugs'] = df['matches'].apply(self._match_drugs, df=df_drugs)
        df = df[df['drugs'] != ""]
        return df

    def output_task1(self):
        #outputs the requested json
        df = self.match_trials_with_drugs()
        df_output = df[['nct_id', 'drugs']]
        json_output = df_output.to_json(orient="records")
        parsed = json.loads(json_output)
        with open("task1.json", "w") as outfile: 
            json.dump(parsed, outfile)
        return parsed

    def match_drugs_to_usan_descriptions(self):
        df_usan_all = pd.read_csv(self.usan, header=None, sep='\n')
        df_usan_all = df_usan_all[0].str.split(',', expand=True)
        headers = list(df_usan_all.iloc[0].fillna("rename")) 
        headers = [i.replace('\"', "") for i in headers]
        print(headers)
        #temporarily renaming empty the empty columns
        df_usan_all.columns = ['name', 'stem', 'definition', 'example', '1', '2', '3', '4', '5', '6']
        df_usan_all.drop(index=0, inplace=True)
        df_usan = df_usan_all.loc[~df_usan_all['name'].str.contains("subgroup:",regex=False)]
        df_usan = df_usan.loc[~df_usan['name'].str.contains("subgroups:",regex=False)]
        df_usan['name'] = df_usan['name'].replace("", np.NaN )
        df_usan['name'] = df_usan['name'].fillna(method='ffill')
        df_usan['definition'] = df_usan['definition'].str.strip(' " " ')
        df_usan = df_usan.fillna("")
        df_usan['example_all'] = df_usan['definition'] + "," + df_usan['example'] + ","  + df_usan['1'] + "," + df_usan['2'] + "," + df_usan['3'] + "," + df_usan['4'] + "," + df_usan['5'] + "," + df_usan['6'] 
        df_usan['example_all'] = df_usan['example_all'].replace('\"', '')
        df_usan.drop(columns=['example', '1', '2', '3', '4', '5', '6'], inplace=True)
        print(df_usan.head())
        return df_usan

    def make_task2_ouput(self):
        df_usan = self.match_drugs_to_usan_descriptions()
        print(df_usan.head())
        usan_dict = dict(zip(df_usan.name, df_usan.definition))
        #print(usan_dict)
        output_list_usan = []
        df_trials = self.match_trials_with_drugs()
        print(df_trials.head())
        for drug in list(df_trials['drugs']):
            drug_usan = {}
            usan_codes = []
            drug_usan['drug'] = drug
            for k, v in usan_dict.items():
                usandict = {}
                if drug.endswith(k):            
                    #print("k ", k)
                    usandict['description'] = v
                    usan_codes.append(usandict)
                    #print(usan_codes)
            if len(usan_codes) > 0:
                drug_usan['usan_codes'] = usan_codes
                output_list_usan.append(drug_usan)
        with open('task2.json', 'w') as t:
            json.dump(output_list_usan, t)
        return output_list_usan



if __name__ == "__main__":
    print("running")
    test = ClinicalTrials()
    test.match_trials_with_drugs()
    test.make_task2_ouput()
