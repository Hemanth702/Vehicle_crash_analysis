# src/crash_analysis.py

import pandas as pd
from src.visualization import save_visualization
from src.visualization import save_visualization_mutli_dim

def analyze_males_killed(primary_persons_df):
    # Analyze crashes with male fatalities
    male_kills = primary_persons_df[primary_persons_df['PRSN_GNDR_ID'] == 'MALE']
    crashes_with_male_kills = male_kills.groupby('CRASH_ID')['DEATH_CNT'].sum()
    count = (crashes_with_male_kills >= 2).sum()
    return count

def analyze_two_wheelers(units_df):
    # Count two-wheeler vehicles (motorcycles)
    two_wheelers = units_df[units_df['VEH_BODY_STYL_ID'].str.upper().str.contains('MOTORCYCLE')]
    two_wheelers_count = two_wheelers.shape[0] 
    return {'two_wheelers_count' : two_wheelers_count}

def analyze_top_vehicle_makes(primary_persons_df, units_df):
    # Analyze top vehicle makes where drivers died and airbags did not deploy
    merged_data = primary_persons_df.merge(units_df, on='CRASH_ID', how='inner')
    merged_data['TOTAL_DEATH_CNT'] = merged_data['DEATH_CNT_x'] + merged_data['DEATH_CNT_y']
    filtered_data = merged_data[
        (merged_data['TOTAL_DEATH_CNT'] > 0) & 
        (merged_data['PRSN_TYPE_ID'] == 'DRIVER') & 
        (merged_data['PRSN_AIRBAG_ID'] == 'NOT DEPLOYED') & 
        (merged_data['VEH_MAKE_ID'].notnull()) & 
        (merged_data['VEH_MAKE_ID'] != 'NA') & 
        (merged_data['VEH_MAKE_ID'] != '')
    ]
    top_vehicle_makes = filtered_data['VEH_MAKE_ID'].value_counts().nlargest(5)
    save_visualization(top_vehicle_makes, 'Top Vehicle Makes Where Driver Died and Airbags Did Not Deploy', 'output/visualizations/analysis_3_visual.png')
    
    return top_vehicle_makes

def analyze_valid_licences_hit_and_run(units_df, primary_person_df):
    # Count hit-and-run incidents involving valid driver licenses
    hit_and_run = units_df[units_df['VEH_HNR_FL'] == 'Y']
    valid_licences = primary_person_df[primary_person_df['DRVR_LIC_TYPE_ID'].isin(['DRIVER LICENSE', 'COMMERCIAL DRIVER LIC.'])]
    count = hit_and_run[hit_and_run['CRASH_ID'].isin(valid_licences['CRASH_ID'])].shape[0]
    
    return {'count' :count}

def analyze_females_not_involved(primary_persons_df):
    # Identify the state with the highest number of crashes involving non-female drivers
    non_female_crashes = primary_persons_df[primary_persons_df['PRSN_GNDR_ID'] != 'FEMALE']
    state_counts = non_female_crashes['DRVR_LIC_STATE_ID'].value_counts()
    highest_state = state_counts.idxmax()
    
    return {'highest_state' :highest_state}

def analyze_top_veh_makes_for_injuries(units_df):
    # Analyze vehicle makes by total injuries and deaths
    total_injuries_and_deaths = units_df.groupby('VEH_MAKE_ID')[['TOT_INJRY_CNT', 'DEATH_CNT']].sum()
    total_injuries_and_deaths['TOTAL_COUNT'] = total_injuries_and_deaths['TOT_INJRY_CNT'] + total_injuries_and_deaths['DEATH_CNT']
    sorted_injuries_and_deaths = total_injuries_and_deaths['TOTAL_COUNT'].sort_values(ascending=False)
    save_visualization(sorted_injuries_and_deaths.iloc[2:5], 'Top 3rd to 5th Vehicle Makes by Injuries and Deaths', 'output/visualizations/analysis_6_visual.png')
    
    return sorted_injuries_and_deaths.iloc[2:5]

def analyze_top_ethnic_group_per_body_style(primary_persons_df, units_df):
    # Identify top ethnic groups by vehicle body style
    merged_data_y = primary_persons_df.merge(units_df, on='CRASH_ID', how='inner')
    merged_data_y = merged_data_y[
        ~merged_data_y['VEH_BODY_STYL_ID'].isin(['UNKNOWN', 'OTHER (EXPLAIN IN NARRATIVE)', 'NOT REPORTED'])
    ]
    merged_data_y = merged_data_y[merged_data_y['VEH_BODY_STYL_ID'].notna() & merged_data_y['VEH_BODY_STYL_ID'].ne('')]
    ethnic_groups = merged_data_y.groupby(['VEH_BODY_STYL_ID', 'PRSN_ETHNICITY_ID']).size().reset_index(name='counts')
    top_ethnic_groups = ethnic_groups.loc[ethnic_groups.groupby('VEH_BODY_STYL_ID')['counts'].idxmax()]
    save_visualization_mutli_dim(top_ethnic_groups[['VEH_BODY_STYL_ID', 'PRSN_ETHNICITY_ID', 'counts']],
                                  'Top Ethnic Groups by Body Style',
                                  'output/visualizations/analysis_7_visual.png')
    
    return top_ethnic_groups

def analyze_top_zip_codes_for_alcohol(primary_persons_df, units_df):
    # Analyze top zip codes for crashes involving alcohol
    merged_data = primary_persons_df.merge(units_df, on='CRASH_ID', how='inner')
    alcohol_crashes = merged_data[
        merged_data['CONTRIB_FACTR_1_ID'].str.contains('ALCOHOL', na=False) |
        merged_data['CONTRIB_FACTR_2_ID'].str.contains('ALCOHOL', na=False) |
        merged_data['CONTRIB_FACTR_P1_ID'].str.contains('ALCOHOL', na=False)
    ]
    car_body_styles = ['PASSENGER CAR, 4-DOOR', 'SPORT UTILITY VEHICLE', 'PASSENGER CAR, 2-DOOR']
    car_crashes = alcohol_crashes[alcohol_crashes['VEH_BODY_STYL_ID'].isin(car_body_styles)]
    car_crashes = car_crashes[car_crashes['DRVR_ZIP'].notna() & car_crashes['DRVR_ZIP'].ne('')]
    top_zip_codes = car_crashes['DRVR_ZIP'].value_counts().nlargest(5)
    save_visualization(top_zip_codes, 'Top 5 Zip Codes for Crashes Involving Alcohol', 'output/visualizations/analysis_8_visual.png')
    
    return top_zip_codes

def analyze_no_damages_high_damage_level(damages_df, units_df):
    # Count distinct crash IDs with no damage but high damage level
    no_damage_df = damages_df[damages_df['DAMAGED_PROPERTY'].isin(["NONE", "NONE1"])]
    high_damage_df = units_df[
        ((units_df['VEH_DMAG_SCL_1_ID'] > "DAMAGED 4") & 
         (~units_df['VEH_DMAG_SCL_1_ID'].isin(["NA", "NO DAMAGE", "INVALID VALUE"]))) |
        ((units_df['VEH_DMAG_SCL_2_ID'] > "DAMAGED 4") & 
         (~units_df['VEH_DMAG_SCL_2_ID'].isin(["NA", "NO DAMAGE", "INVALID VALUE"])))
    ]
    merged_df = no_damage_df.merge(high_damage_df, on="CRASH_ID", how='inner')
    insured_vehicles = merged_df[merged_df['FIN_RESP_TYPE_ID'] == "PROOF OF LIABILITY INSURANCE"]
    distinct_crash_ids = insured_vehicles['CRASH_ID'].nunique()
    return {'distinct_crash_ids' : distinct_crash_ids}

def analyze_top_vehicle_makes_speeding(charges_df, primary_persons_df, units_df):
    # Analyze top vehicle makes involved in speeding incidents
    speeding_charges = charges_df[charges_df['CHARGE'].str.contains('SPEED', na=False)]
    merged_units_speeding = speeding_charges.merge(units_df[['CRASH_ID', 'VEH_LIC_STATE_ID']], on='CRASH_ID', how='inner')
    top_25_states = merged_units_speeding['VEH_LIC_STATE_ID'].value_counts().nlargest(25).index.tolist()
    top_10_colors = units_df[units_df['VEH_COLOR_ID'] != "NA"]['VEH_COLOR_ID'].value_counts().nlargest(10).index.tolist()
    merged_data = speeding_charges.merge(primary_persons_df, on='CRASH_ID', how='inner') \
                                  .merge(units_df, on='CRASH_ID', how='inner')
    filtered_data = merged_data[
        (merged_data['CHARGE'].str.contains('SPEED', na=False)) &
        (merged_data['DRVR_LIC_TYPE_ID'].isin(["DRIVER LICENSE", "COMMERCIAL DRIVER LIC."])) &
        (merged_data['VEH_COLOR_ID'].isin(top_10_colors)) &
        (merged_data['VEH_LIC_STATE_ID'].isin(top_25_states))
    ]
    top_vehicle_makes = filtered_data['VEH_MAKE_ID'].value_counts().nlargest(5)
    save_visualization(top_vehicle_makes, 'Top 5 Vehicle Makes', 'output/visualizations/analysis_10_visual.png')
    
    return top_vehicle_makes
