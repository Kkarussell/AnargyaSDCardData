import re
import math
import matplotlib.pyplot as plt


def quaternion_to_euler(w, x, y, z):
    """
    Convert quaternion to Euler XYZ angles in degrees.
    """
    # Roll (X)
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    # Pitch (Y)
    t2 = +2.0 * (w * y - z * x)
    t2 = max(min(t2, 1.0), -1.0)
    pitch_y = math.asin(t2)

    # Yaw (Z)
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    return (
        math.degrees(roll_x),
        math.degrees(pitch_y),
        math.degrees(yaw_z)
    )


def parse_quaternion_and_accel(filename="2.txt"):
    """
    Parse quaternion (ID 47–50) and accelerometer (ID 51–53) data.
    """
    w_raws, x_raws, y_raws, z_raws = [], [], [], []
    ax_raws, ay_raws, az_raws = [], [], []

    line_regex = re.compile(r"ID=(\d+)\s+Val=(-?\d+)")

    with open(filename, 'r') as f:
        for line in f:
            match = line_regex.search(line)
            if match:
                id_val, val = map(int, match.groups())

                # Quaternion
                if id_val == 47:
                    w_raws.append(val)
                elif id_val == 48:
                    x_raws.append(val)
                elif id_val == 49:
                    y_raws.append(val)
                elif id_val == 50:
                    z_raws.append(val)

                # Accelerometer
                elif id_val == 51:
                    ax_raws.append(val)
                elif id_val == 52:
                    ay_raws.append(val)
                elif id_val == 53:
                    az_raws.append(val)

    # Ensure equal lengths
    nq = min(len(w_raws), len(x_raws), len(y_raws), len(z_raws))
    na = min(len(ax_raws), len(ay_raws), len(az_raws))

    quats = []
    for i in range(nq):
        quats.append((
            w_raws[i] / 16384,
            x_raws[i] / 16384,
            y_raws[i] / 16384,
            z_raws[i] / 16384
        ))

    accels = []
    for i in range(na):
        accels.append((
            ax_raws[i] / 16384,
            ay_raws[i] / 16384,
            az_raws[i] / 16384
        ))

    return quats, accels


def main():
    try:
        quats, accels = parse_quaternion_and_accel("2.txt")

        if not quats:
            print("No quaternion data found.")
            return

        # --- Euler angles ---
        rolls, pitches, yaws = [], [], []
        for w, x, y, z in quats:
            r, p, yw = quaternion_to_euler(w, x, y, z)
            rolls.append(r)
            pitches.append(p)
            yaws.append(yw)

        t_angle = range(len(rolls))

        plt.style.use('seaborn-v0_8-whitegrid')

        fig1, axs1 = plt.subplots(3, 1, figsize=(15, 12), sharex=True)
        fig1.suptitle('Euler Angles from Quaternion (Degrees)', fontsize=18)

        axs1[0].plot(t_angle, rolls)
        axs1[0].set_ylabel('Roll (°)')

        axs1[1].plot(t_angle, pitches)
        axs1[1].set_ylabel('Pitch (°)')

        axs1[2].plot(t_angle, yaws)
        axs1[2].set_ylabel('Yaw (°)')
        axs1[2].set_xlabel('Sample Number')

        plt.tight_layout(rect=[0, 0, 1, 0.95])

        # --- Accelerometer ---
        if accels:
            ax, ay, az = zip(*accels)
            t_acc = range(len(ax))

            fig2, axs2 = plt.subplots(3, 1, figsize=(15, 12), sharex=True)
            fig2.suptitle('Accelerometer Data (g)', fontsize=18)

            axs2[0].plot(t_acc, ax)
            axs2[0].set_ylabel('Accel X (g)')

            axs2[1].plot(t_acc, ay)
            axs2[1].set_ylabel('Accel Y (g)')

            axs2[2].plot(t_acc, az)
            axs2[2].set_ylabel('Accel Z (g)')
            axs2[2].set_xlabel('Sample Number')

            plt.tight_layout(rect=[0, 0, 1, 0.95])

        plt.show()

    except FileNotFoundError:
        print("Error: data file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
