import pandas as pd
import matplotlib.pyplot as plt

def load_and_clean_csv(ots_swarm_log.csv):
    try:
        df = pd.read_csv(ots_swarm_log.csv, skipinitialspace=True)
    except FileNotFoundError:
        print(f"Error: CSV file '{ots_swarm_log.csv}' not found. Check the filename and path.")
        exit(1)
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
        exit(1)

    # Convert boolean columns from strings to actual booleans
    for col in ['Payload Deployed', 'Compound Deployed']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower().map({'true': True, 'false': False})
        else:
            print(f"Warning: Column '{col}' not found in CSV.")

    # Ensure Cycle column is integer
    if 'Cycle' in df.columns:
        df['Cycle'] = df['Cycle'].astype(int)
    else:
        print("Warning: Column 'Cycle' not found in CSV.")

    return df

def plot_ots_data(df):
    units = df['Unit ID'].unique()

    # Plot ozone levels
    plt.figure(figsize=(12, 6))
    for unit in units:
        unit_data = df[df['Unit ID'] == unit]
        plt.plot(unit_data['Cycle'], unit_data['Ozone Level (ppm)'], marker='o', label=unit)
    plt.title("Ozone Levels per Swarm Unit Over Cycles")
    plt.xlabel("Simulation Cycle")
    plt.ylabel("Ozone Level (ppm)")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot payload and compound deployment timeline
    plt.figure(figsize=(12, 6))
    for idx, unit in enumerate(units):
        unit_data = df[df['Unit ID'] == unit]
        payload = unit_data['Payload Deployed']
        compound = unit_data['Compound Deployed']

        # Plot payload deployment (red circles)
        plt.plot(unit_data['Cycle'], payload * (idx * 2 + 1.5), 'ro', label=f"{unit} Payload" if idx == 0 else "")
        # Plot compound deployment (blue squares)
        plt.plot(unit_data['Cycle'], compound * (idx * 2 + 1.0), 'bs', label=f"{unit} Compound" if idx == 0 else "")

    plt.yticks([i * 2 + 1 for i in range(len(units))], units)
    plt.title("Payload (red circles) and Compound (blue squares) Deployment Over Cycles")
    plt.xlabel("Simulation Cycle")
    plt.ylabel("Swarm Units")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()

def main():
    filename = "ots_swarm_log.csv"
    df = load_and_clean_csv(filename)
    plot_ots_data(df)

if __name__ == "__main__":
    main()
