import re
import matplotlib.pyplot as plt

def parse_id_values(filename="3.txt", target_id=19):
    """
    Parse a log file and extract raw Val values for a specific ID.
    """
    values = []
    line_regex = re.compile(r"ID=(\d+)\s+Val=(-?\d+)")

    with open(filename, 'r') as f:
        for line in f:
            match = line_regex.search(line)
            if match:
                id_val, raw_val = map(int, match.groups())
                if id_val == target_id:
                    values.append(raw_val)

    return values


def main():
    try:
        # change target_id here (19, 20, 21, 47, etc.)
        target_id = 61
        data = parse_id_values("3.txt", target_id)

        if not data:
            print(f"No data found for ID={target_id}")
            return

        time_axis = range(len(data))

        plt.style.use('seaborn-v0_8-whitegrid')
        plt.figure(figsize=(14, 6))
        plt.plot(time_axis, data, label=f"ID={target_id} Raw Values")
        plt.title(f"Raw Data Visualization for ID={target_id}")
        plt.xlabel("Sample Number")
        plt.ylabel("Raw Value")
        plt.legend()
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("Error: data file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
