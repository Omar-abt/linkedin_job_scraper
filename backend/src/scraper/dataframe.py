import pandas as pd

class Columns:
    JOB_TITLE = "Job Title"
    COMPANY_NAME = "Company Name"
    ROLE_LOCATION = "Role Location"
    JOB_TYPE = "Job Type"
    EXPERIENCE_LEVEL = "Experience Level"
    POST_DATE = "Post Date"
    NUM_OF_APPLICANTS = "Number of Applicants"


def create_data_frame(job_titles, company_names, role_locations, job_type, experience_level, post_dates, number_applicants):
    df = pd.DataFrame(list(zip(job_titles, company_names,
                    role_locations, job_type, experience_level,
                    post_dates, number_applicants)),
                    columns = [Columns.JOB_TITLE, Columns.COMPANY_NAME, Columns.ROLE_LOCATION, 
                            Columns.JOB_TYPE, Columns.EXPERIENCE_LEVEL, Columns.POST_DATE,
                            Columns.NUM_OF_APPLICANTS])
    return df
    
def clean_data_frame(df):

    role_locations_options = {'On-site', 'Hybrid', 'Remote'}
    job_type_options = {'Full-time', 'Part-time', 'Contract', 'Temporary', 'Internship', 'Volunteer', 'Other'}
    experience_level_options = {'Internship', 'Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive'}

    # cleaning out incorrect values for role location
    mask = ~df[Columns.ROLE_LOCATION].isin(role_locations_options)
    df.loc[mask, Columns.ROLE_LOCATION] = ''  # Update column values with empty string

    # cleaning out incorrect values for job type
    mask = ~df[Columns.JOB_TYPE].isin(job_type_options)
    df.loc[mask, Columns.JOB_TYPE] = ''  # Update column values with empty string

    # cleaning out incorrect values for experience level
    mask = ~df[Columns.EXPERIENCE_LEVEL].isin(experience_level_options)
    df.loc[mask, Columns.EXPERIENCE_LEVEL] = ''  # Update column values with empty string

    # cleaning number of applicants column
    df[Columns.NUM_OF_APPLICANTS] = df[Columns.NUM_OF_APPLICANTS].astype(str).str.replace(r'\D', '', regex=True)



    # df[Columns.NUM_OF_APPLICANTS] = df[Columns.NUM_OF_APPLICANTS].str.extract(r'(\d+)').astype(str)

    # df.to_csv('backend/output/jobs_cleaned.csv', index=False)
    
    return df



# df = pd.read_csv('backend/output/jobs.csv')
# df = clean_data_frame(df)
# df.to_csv('backend/output/jobs_cleaned.csv', index=False)