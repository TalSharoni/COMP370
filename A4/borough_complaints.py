import argparse
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


def main():
    args = parser_args()

    chunksize = 1000
    combined = pd.DataFrame()

    for chunk in pd.read_csv(args.input, chunksize=chunksize, header=None):
        df = chunk[[5, 1, 2, 16]]
        df.columns = ['type', 'opened', 'closed', 'borough']
    
        df['type'] = df['type'].str.strip().str.lower()
        df['borough'] = df['borough'].apply(find_borough)
        df['opened'] = pd.to_datetime(df['opened'])
        df['closed'] = pd.to_datetime(df['closed'])
        start = pd.to_datetime(args.start)
        end = pd.to_datetime(args.end)

        df = df[(df['opened'] >= start) & (df['closed'] <= end)]

        counts = df.groupby(['type', 'borough']).size().reset_index(name='count')
        combined = pd.concat([combined, counts], ignore_index=True)
        combined = combined.groupby(['type', 'borough'], as_index=False).agg({'count': 'sum'})

    output(combined, args.output)

def parser_args():
    parser = argparse.ArgumentParser(description="complaints by borough for given date range")
    parser.add_argument('-i', '--input', required=True, help='input a CSV file')
    parser.add_argument('-s', '--start', required=True, help='start date (MM-DD-YYYY).')
    parser.add_argument('-e', '--end', required=True, help='end date (MM-DD-YYYY).')
    parser.add_argument('-o', '--output', help='output file [optional]')
    return parser.parse_args()

def find_borough(row):
    boroughs = ["manhattan", "brooklyn", "queens", "bronx", "staten island"]
    for borough in boroughs:
        if borough in str(row).lower():
            return borough
    return None 

def output(df, file):
    if file:
        df.to_csv(file, index=False)
    else:
        print(df.to_csv(index=False)) 

if __name__ == "__main__":
    main()
