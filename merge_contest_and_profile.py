import pandas as pd
import numpy as np
import re
from tqdm import tqdm


date_start = "2022-02-01"
date_end = "2022-02-28"

date_range = pd.date_range(start = date_start, end = date_end)

for date in tqdm(date_range):
    date = str(date)[:10]
    df_contest = pd.read_csv("contest_data_" + date + ".csv")
    df_user_profile = pd.read_csv("user_profile_" + date + ".csv")

    # get user id
    def get_user_level(row):

        res = []
        entries = row['entries']
        res += re.findall("'participant_id': '\d{5,8}'", entries)
        
        deleted_entries = row['deleted_entries']
        res += re.findall("'participant_id': '\d{5,8}'", deleted_entries)

        res = list(set(res))

        # search participant ids
        ids = list(map(lambda x: re.search("\d{5,8}", x).group(0), res))

        # get user levels
        entry_level = 0
        mid_level = 0
        top_level = 0

        for id in ids:
            try:
                certification = df_user_profile[df_user_profile["user_id"] == int(id)]["certification"].values[0]
                # print(certification)
            except:
                certification = []
            if 'Top Level' in certification:
                top_level += 1
            elif 'Mid Level' in certification:
                mid_level += 1
            else:
                entry_level += 1

        # get top_n participant's contest won and runner up
        contest_won = []
        runner_up = []
        for id in ids:
            try:
                contest_won.append(df_user_profile[df_user_profile["user_id"] == int(id)]["contests_won"].values[0])
                runner_up.append(df_user_profile[df_user_profile["user_id"] == int(id)]["runner_up"].values[0])
                # print(certification)
            except:
                pass

        # sort contest won and runner up in descending order
        contest_won.sort(reverse=True)
        runner_up.sort(reverse=True)

        if len(contest_won) >= 10:
            avg_contest_won = np.mean(contest_won)
            avg_contest_won_top_10 = np.mean(contest_won[:10])
            avg_contest_won_top_5 = np.mean(contest_won[:5])
        elif len(contest_won) >= 5:
            avg_contest_won = np.mean(contest_won)
            avg_contest_won_top_10 = np.mean(contest_won)
            avg_contest_won_top_5 = np.mean(contest_won[:5])
        else:
            avg_contest_won = np.mean(contest_won)
            avg_contest_won_top_10 = np.mean(contest_won)
            avg_contest_won_top_5 = np.mean(contest_won)

        if len(runner_up) >= 10:
            avg_runner_up = np.mean(runner_up)
            avg_runner_up_top_10 = np.mean(runner_up[:10])
            avg_runner_up_top_5 = np.mean(runner_up[:5])
        elif len(contest_won) >= 5:
            avg_runner_up = np.mean(runner_up)
            avg_runner_up_top_10 = np.mean(runner_up)
            avg_runner_up_top_5 = np.mean(runner_up[:5])
        else:
            avg_runner_up = np.mean(runner_up)
            avg_runner_up_top_10 = np.mean(runner_up)
            avg_runner_up_top_5 = np.mean(runner_up)

        return entry_level, mid_level, top_level, avg_contest_won, avg_contest_won_top_5, avg_contest_won_top_10, avg_runner_up, avg_runner_up_top_5, avg_runner_up_top_10


    df_contest[['entry_level', 'mid_level', 'top_level', 'avg_contest_won', 'avg_contest_won_top_5', 'avg_contest_won_top_10', 'avg_runner_up', 'avg_runner_up_top_5', 'avg_runner_up_top_10']] = df_contest.apply(get_user_level, axis=1, result_type="expand")

    df_contest.to_csv("out/contest_data_merged_" + date + ".csv", index=False)






