

import pandas as pd
from optparse import OptionParser 

INPUT_TO_CONV = "data/competition_data/interactions.csv"
INPUT_CONVERTED = "data/ml100k/ratings.csv"
OUTPUT_TO_CONVERT = "output/predictions.csv"
OUTPUT_CONVERTED = "output/submissionTOPPOP.csv"

EXPER = "data/competition_data/item_profile.csv"


def main():
    # Command-line parsing
    parser = OptionParser()
    parser.add_option("--in", 
                      action="store_true", dest="input_convert",
                      help="convert the input interactions file. No checks.")
    parser.add_option("--out",
                      action="store_true", dest="output_convert",
                      help="convert the output recommendations file. No checks.")
    parser.add_option("--exp",
                      action="store_true", dest="experiment",
                      help="Do NOT use")
    (options, args) = parser.parse_args()
    
    if options.input_convert:
        input_conv(INPUT_TO_CONV, INPUT_CONVERTED)
    elif options.output_convert:
        output_conv(OUTPUT_TO_CONVERT, OUTPUT_CONVERTED)
    elif options.experiment:
        exp_input_conv(EXPER, INPUT_CONVERTED)
    


def input_conv(in_file_path, out_file_path):
    """
    Convert a tsv file with header
        user_id	    item_id	    interaction_type	created_at
    into a csv file with header 
        user_id,item_id,rating,ts
    """
    tsv_table =  pd.read_csv(in_file_path, sep="\t")
    tsv_table.columns = ['user_id','item_id','rating','ts']
    tsv_table.to_csv(out_file_path, index=False,)
    
    
def exp_input_conv(in_file_path, out_file_path):
    """
    Convert a tsv file into a csv
    """
    tsv_table =  pd.read_csv(in_file_path, sep="\t")
    #tsv_table.columns = ['user_id','item_id','rating','ts']
    tsv_table.to_csv(out_file_path, index=False,)

    
    
def output_conv(in_file_path, out_file_path):
    """
    Convert a tsv file with header
        user_id,rec_item1,rec_item2,rec_item3,rec_item4,rec_item5,\
        rec_item6,rec_item7,rec_item8,rec_item9,rec_item10
    into a csv file with header 
        user_id,recommended_items
    compressing the rec_itemX rows into the usual recommendations format.
    """
    csv_table =  pd.read_csv(in_file_path, sep=",")
    csv_copy = csv_table.copy()
    tsv_values = csv_copy.drop('user_id', axis=1)
    tsv_values = tsv_values.apply(lambda x: " ".join([str(y) for y in x.values]),axis=1)
    tsv_table = pd.concat( [csv_table.user_id, tsv_values], axis=1)
    tsv_table.columns = ['user_id','recommended_items'] 
    tsv_table.to_csv(out_file_path, index=False,)


if __name__ == "__main__":
    main()
