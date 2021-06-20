import pandas as pd
import re


def parse_spec_txt_file(file_path):
    import pandas as pd

    with open(file_path, 'r') as f:
        inds = []
        times = []
        marks = []
        for line in f:
            m = re.match('(\d+), ([se]), (\d+)', line)
            if m:
                inds.append(int(m.group(1)))
                times.append(int(m.group(3)))
                marks.append(m.group(2))

    df = pd.DataFrame(zip(inds, marks, times))
    return df


def mark_submission(spec_txt_file_path, submission_csv_path):
    spec_df = parse_spec_txt_file(spec_txt_file_path)
    df = pd.read_csv(submission_csv_path)

    df['y'] = [0] * len(df)

    df.columns = ['id', 'time', 'x', 'y']
    s, e = 0, 0
    for i, row in spec_df.iterrows():
        if 's' in row[1]:
            s = row[2]
        if 'e' in row[1]:
            e = row[2]
            df.iloc[(df['id'] == row[0]) & (df['time'] <= e) & (df['time'] >= s), 3] = 1

    return df


if __name__ == "__main__":
    df = mark_submission('in.csv', 'train.csv')
    df.to_csv('sb.csv', index=False)
