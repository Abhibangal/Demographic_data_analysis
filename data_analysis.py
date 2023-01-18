import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult_data.csv', header=0)

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.groupby(['race'])['race'].count()

    # What is the average age of men?
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(axis=0), 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(df.loc[df['education'] == 'Bachelors']['education'].count() / df['education'].count() * 100,1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = round(df.loc[((df['education'] == 'Bachelors') | (df['education'] == 'Masters') |
                                     (df['education'] == 'Doctorate'))],1)
    lower_education = round(df.loc[~((df['education'] == 'Bachelors') | (df['education'] == 'Masters') |
                                     (df['education'] == 'Doctorate'))], 1)

    # percentage with salary >50K
    higher_education_rich = higher_education[higher_education['salary'] == '>50K']['salary'].count() / higher_education['education'].count() * 100
    lower_education_rich = lower_education[lower_education['salary'] == '>50K']['salary'].count() / lower_education['education'].count() * 100

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df.loc[df['hours-per-week'] == df['hours-per-week'].min()]

    rich_percentage = num_min_workers[num_min_workers['salary'] == '>50K']['hours-per-week'].count()/ num_min_workers['hours-per-week'].count() * 100

    # What country has the highest percentage of people that earn >50K?
    df1 = df.groupby(['native-country'], as_index=False)['salary'].count()
    df1.columns = ['Country', 'Total_cnt']

    df2 = df[df['salary'] == '>50K']
    df3 = df2.groupby(['native-country'], as_index=False)['salary'].count()
    df3.columns = ['Country', 'Total_>50_cnt']
    df4 = pd.merge(df1, df3, on='Country', how='inner')
    df4['_%_'] = round(df4['Total_>50_cnt'] / df4['Total_cnt'] * 100, 1)
    highest_earning_country = df4[df4['_%_'] == df4['_%_'].max()]['Country'].squeeze()
    highest_earning_country_percentage = df4[df4['_%_'] == df4['_%_'].max()]['_%_'].squeeze()

    # Identify the most popular occupation for those who earn >50K in India.
    rich_india = df2[df2['native-country'] == 'India']

    grp_india = rich_india.groupby(['occupation'], as_index=False)['salary'].count()
    top_IN_occupation = grp_india[grp_india['salary'] == grp_india['salary'].max()]['occupation'].squeeze()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }


print(calculate_demographic_data())