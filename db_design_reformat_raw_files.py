
import os
import sys
import pandas as pd
import numpy as np

df = pd.read_excel('current_learning_objectives_raw_data.xlsx', sheet_name='assigned_raw', skiprows = 2)

standard_cols = ['course_id', 'course_name', 'instructor_name']
fall_df = df.iloc[:,:3]
fall_df.columns = standard_cols
fall_df['term_name'] = 'FALL2021'

sum_df = df.iloc[:,4:7]
sum_df.columns = standard_cols
sum_df['term_name'] = 'SUMMER2021'

spring_df = df.iloc[:,8:11]
spring_df.columns = standard_cols
spring_df['term_name'] = 'SPRING2021'

def drop_null_rows(df1, df2, df3):
    """Takes three dataframes and drops all rows where the 'course_id' column is null."""
    df1_cleaned = df1[~df1['course_id'].isnull()]
    df2_cleaned = df2[~df2['course_id'].isnull()]
    df3_cleaned = df3[~df3['course_id'].isnull()]

    return df1_cleaned, df2_cleaned, df3_cleaned

def clean_dataframes(dfs, column_to_check=None):
    """Iterates through a list of DataFrames and strip, lowercase, remove nulls""""
    cleaned_dfs = []

    for df in dfs:
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip().str.lower()
            df[col] = df[col].str.replace(r'^.*?:', '', regex=True)

        if column_to_check:
            df = df[~df[column_to_check].isnull()]

        cleaned_dfs.append(df.copy()) 

    return cleaned_dfs


def add_prefixed_id(df, id_column_name, prefix):
    """Add an auto-incrementing integer ID column with a prefix to a DataFrame."""
    df[id_column_name] = [f"{prefix}{i:04d}" for i in range(1, len(df) + 1)]
    return df.set_index(id_column_name)

cleaned_fall_df, cleaned_summer_df, cleaned_spring_df = drop_null_rows(fall_df, sum_df, spring_df)

combined_df = pd.concat([cleaned_fall_df, cleaned_summer_df, cleaned_spring_df],ignore_index=True)

for col in combined_df.columns:
    combined_df[col] = combined_df[col].astype(str).str.strip().str.lower()

# remove text before colon in course_name
combined_df['course_name'] = combined_df['course_name'].apply(lambda x: x.split(':', 1)[-1].strip() if ':' in x else x)

#split instructor name

combined_df['instructor_name'] = combined_df['instructor_name'].str.replace('&', ',')

combined_df['instructor_name'] = combined_df['instructor_name'].str.split(',\s*')

df_expanded = combined_df.explode('instructor_name', ignore_index=True)

course_offerings = df_expanded

course_offerings_df = add_prefixed_id(course_offerings, 'offering_id', 'OFFER')

""" Terms"""

term_raw = pd.read_excel(dir+'current_learning_objectives_raw_data.xlsx', sheet_name='other_data_raw', skiprows = 24)

terms = term_raw.iloc[:3,:1]

terms.to_csv(dir + 'terms.csv')

""" Instructors"""

instructors_raw = pd.read_excel(dir+'current_learning_objectives_raw_data.xlsx', sheet_name='other_data_raw', skiprows = 30)

instructors_raw  = instructors_raw.iloc[:22,:1]
instructors_raw = instructors_raw.rename(columns = {'Unnamed: 0': 'instructor_name'})

for col in instructors_raw.columns:
    instructors_raw[col] = instructors_raw[col].astype(str).str.strip().str.lower()

# split instructor name
instructors_raw['instructor_name'] = instructors_raw['instructor_name'].str.replace('&', ',')

instructors_raw['instructor_name'] = instructors_raw['instructor_name'].str.split(',\s*')

df_expanded = instructors_raw.explode('instructor_name', ignore_index=True)

instructors = df_expanded.drop_duplicates()

names_to_set_inactive = ['jeremy bolton','luis felipe rosado murillo']

instructors['active'] = instructors['instructor_name'].apply(lambda x: 'FALSE' if x in names_to_set_inactive else 'TRUE')

teachers_df = add_prefixed_id(instructors, 'teacher_id', 'INST')

teachers_df.to_csv('intructors.csv')

"""Courses"""

courses_raw = pd.read_excel(dir+'current_learning_objectives_raw_data.xlsx', sheet_name='other_data_raw', skiprows = 3)

courses = courses_raw.iloc[:17,:4]

courses['name'] = courses['name'].astype(str).str.strip().str.lower()

courses['description_short'] = courses['description_short'].astype(str).str.strip().str.lower()

courses.to_csv('courses.csv')

"""Learning Outcomes"""

tab_names = ['5001', '5012','5100','5110','6001','6002','6003','6011','6012','6030']

dfs = []

# loop through each course sheet name to import append it to the list
for tab in tab_names:
    df = pd.read_excel(dir+'current_learning_objectives_raw_data.xlsx', sheet_name=tab, skiprows = 2)
    dfs.append(df)

cleaned_dfs = clean_dataframes(dfs, column_to_check=None)

cleaned_dfs = clean_dataframes(dfs, column_to_check=None)

learning_oucomes = pd.concat(cleaned_dfs, ignore_index=True)

learning_oucomes = add_prefixed_id(learning_oucomes, 'outcome_id', 'LO')

learning_oucomes.to_csv(dir+'learning_outcomes.csv')

"""Rework course offerings to include foreign keys"""

for col in course_offerings_df.select_dtypes(include=['object']).columns:
            course_offerings_df[col] = course_offerings_df[col].str.strip().str.lower()
            course_offerings_df[col] = course_offerings_df[col].str.replace(r'^.*?:', '', regex=True)

for col in instructors.select_dtypes(include=['object']).columns:
            instructors[col] = instructors[col].str.strip().str.lower()
            instructors[col] = instructors[col].str.replace(r'^.*?:', '', regex=True)

course_offerings_final = pd.merge(
    course_offerings_df,
    instructors[['instructor_name', 'teacher_id']],
    on='instructor_name',
    how='left'
)


course_offerings_final.drop(columns='instructor_name', inplace = True)
course_offerings_final.drop(columns='course_name', inplace = True)

course_offerings_final = add_prefixed_id(course_offerings_final, 'offering_id', 'CO')

course_offerings_final.to_csv('course_offerings.csv')