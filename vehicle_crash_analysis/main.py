# main.py

import pandas as pd
from src.config_reader import read_config
from src.data_cleaning import clean_data
from src.crash_analysis import (
    analyze_males_killed,
    analyze_two_wheelers,
    analyze_top_vehicle_makes,
    analyze_valid_licences_hit_and_run,
    analyze_females_not_involved,
    analyze_top_veh_makes_for_injuries,
    analyze_top_ethnic_group_per_body_style,
    analyze_top_zip_codes_for_alcohol,
    analyze_no_damages_high_damage_level,
    analyze_top_vehicle_makes_speeding
)

def load_data(config):
    """Load all data from CSV files."""
    dataframes = {}
    for key, file_name in config['files'].items():
        dataframes[key] = pd.read_csv(config['data_path'] + file_name, low_memory=False)
    return dataframes

def main():
    input_config = read_config('config/input_config.yaml')
    output_config = read_config('config/output_config.yaml')
    
    # Load data
    dataframes = load_data(input_config)
    
    # Clean data
    cleaned_data = clean_data(dataframes)

    # Perform analyses
    results = {}
    results['males_killed'] = analyze_males_killed(cleaned_data['primary_persons'])
    results['two_wheelers'] = analyze_two_wheelers(cleaned_data['units'])
    results['top_vehicle_makes'] = analyze_top_vehicle_makes(cleaned_data['primary_persons'], cleaned_data['units'])
    results['valid_licences_hit_and_run'] = analyze_valid_licences_hit_and_run(cleaned_data['units'], cleaned_data['primary_persons'])
    results['females_not_involved'] = analyze_females_not_involved(cleaned_data['primary_persons'])
    results['top_veh_makes_for_injuries'] = analyze_top_veh_makes_for_injuries(cleaned_data['units'])
    results['top_ethnic_group_per_body_style'] = analyze_top_ethnic_group_per_body_style(cleaned_data['primary_persons'], cleaned_data['units'])
    results['top_zip_codes_for_alcohol'] = analyze_top_zip_codes_for_alcohol(cleaned_data['primary_persons'], cleaned_data['units'])
    results['no_damages_high_damage_level'] = analyze_no_damages_high_damage_level(cleaned_data['damages'], cleaned_data['units'])
    results['top_vehicle_makes_speeding'] = analyze_top_vehicle_makes_speeding(cleaned_data['charges'], cleaned_data['primary_persons'], cleaned_data['units'])

    # Save results to CSV in corresponding analysis folders
    results_files = [
        ("males_killed", "Analysis_1"),
        ("two_wheelers", "Analysis_2"),
        ("top_vehicle_makes", "Analysis_3"),
        ("valid_licences_hit_and_run", "Analysis_4"),
        ("females_not_involved", "Analysis_5"),
        ("top_veh_makes_for_injuries", "Analysis_6"),
        ("top_ethnic_group_per_body_style", "Analysis_7"),
        ("top_zip_codes_for_alcohol", "Analysis_8"),
        ("no_damages_high_damage_level", "Analysis_9"),
        ("top_vehicle_makes_speeding", "Analysis_10"),
    ]

    for key, folder_name in results_files:
        value = results[key]  # Get the result value
        output_folder = output_config['output_paths'][folder_name.lower()]  # Get the corresponding output path

        if isinstance(value, pd.Series):  # If value is a Series
            value.to_csv(f"{output_folder}{key}_results.csv", header=True)
        else:
            with open(f"{output_folder}{key}_results.csv", 'w') as f:
                f.write(str(value))

if __name__ == "__main__":
    main()
