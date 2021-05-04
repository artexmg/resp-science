import os
import pandas as pd
from convert_to_excel import *
import matplotlib.pyplot as plt
import matplotlib.patches as mp


# df = pd.read_excel(file, engine='') #, columns=['Time (sec)','Airway Pressure (cmH2O)'])
def plot_waveforms(df, title, subtitle):
    fig = plt.figure()
    plt.plot(df['Time (sec)'], df['Airway Pressure (cmH2O)'])
    fig.suptitle("Waveform {}".format(title))
    plt.title(subtitle)

    # Axis titles
    plt.xlabel('Time (sec)')
    plt.ylabel('Airway Pressure (cmH2O)')

    # # Set handlers for labels
    lb1 = mp.Patch(label=title, facecolor='royalblue')
    plt.legend(handles=[lb1], loc="upper center", fontsize="small", title="")

    # Y axis range
    plt.ylim(-10, 50)
    # Set Title
    plt.plot(df['Time (sec)'], df['Airway Pressure (cmH2O)'], color='royalblue')
    plt.show()
    # return  plt


def plot_summary(df):
    my_df = df.loc[3:][['Breath Num.', 'Ppeak (cmH2O)', 'I/E', 'PEEP (cmH2O)', 'Vol 1 Peak (mL)']]
    my_df.plot(x='Breath Num.', y=['Ppeak (cmH2O)', 'PEEP (cmH2O)'])
    plt.show()


def compare_waveforms(df1, vent1, df2, vent2, subtitle):
    # frames
    fig = plt.figure()
    # Titles
    fig.suptitle("Pressure {vent1} vs {vent2}".format(vent1=vent1, vent2=vent2))
    plt.xlabel('Time (sec)')
    plt.ylabel('Airway Pressure (cmH2O)')
    plt.title(subtitle)

    # # Set handlers for labels
    lb1 = mp.Patch(label=vent1, facecolor='royalblue')
    lb2 = mp.Patch(label=vent2, facecolor='coral')
    plt.legend(handles=[lb1, lb2], loc="upper center", fontsize="small", title="")

    # Y axis range
    plt.ylim(-10, 50)
    # Set Title
    plt.plot(df1['Time (sec)'], df1['Airway Pressure (cmH2O)'], color='royalblue')
    plt.plot(df2['Time (sec)'], df2['Airway Pressure (cmH2O)'], color='coral')
    return plt


def get_df(file, input_path):
    file = os.path.join(input_path, file)
    content = read_source_file(file)
    df = create_dataframe(content)
    return cleanse_dataframe(df)


if __name__ == "__main__":
    def vent_vs_vent(df, vent1, vent2, ini_v1, ini_v2, region, color, delta1=10000, delta2=10000):
        df1 = df[vent1].loc[ini_v1:ini_v1 + delta1][[x, y]]
        df2 = df[vent2].loc[ini_v2:ini_v2 + delta2][[x, y]]
        plot = compare_waveforms(df1=df1, vent1=vent1, df2=df2, vent2=vent2, subtitle=f"{color} {mft} {region}")
        plot.savefig(os.path.join(output_path, f"waveform-{vent1}-vs-{vent2}-{color}-{mft}-{region}.png"),
                     transparent=False)


    def process_mf3(color):
        # Build a registry of Dataframes
        color = color.title()
        mf3_df = {}
        mf3_df['vortran'] = get_df(f"M3_{color}_Vortran.rwa", input_path)
        mf3_df['servo'] = get_df(f"M3_{color}_Servo.rwa", input_path)
        mf3_df['invent'] = get_df(f"M3_Jung_{color}_20_Click.rwa", input_path)

        # Extravents for green
        if color == "green":
            mf3_df['click'] = get_df(f"M3_{color}_20_Click.rwa", input_path)
            mf3_df['thorpe'] = get_df(f"M3_{color}_20_Thorpe.rwa", input_path)

        # Vortran vs Click
        vent1 = "vortran"
        vent2 = "invent"

        vent_vs_vent(df=mf3_df, vent1=vent1, vent2=vent2, ini_v1=60000, ini_v2=60000, region="region 1", color=color)
        vent_vs_vent(df=mf3_df, vent1=vent1, vent2=vent2, ini_v1=150000, ini_v2=150000, region="region 2", color=color)
        vent_vs_vent(df=mf3_df, vent1=vent1, vent2=vent2, ini_v1=200000, ini_v2=200000, region="region 3", color=color)

        # servo vs invent
        vent1 = "servo"
        vent2 = "invent"

        vent_vs_vent(df=mf3_df, vent1=vent1, vent2=vent2, ini_v1=60000, ini_v2=60000, region="region 1", color=color)
        vent_vs_vent(df=mf3_df, vent1=vent1, vent2=vent2, ini_v1=150000, ini_v2=150000, region="region 2", color=color)
        vent_vs_vent(df=mf3_df, vent1=vent1, vent2=vent2, ini_v1=200000, ini_v2=200000, region="region 3", color=color)

        # only for green (so far)
        # thorpe vs click
        if color == "green":
            vent1 = "thorpe"
            vent2 = "click"

            vent_vs_vent(df=mf3_df, vent1=vent1, vent2=vent2, ini_v1=60000, ini_v2=70000, region="region 1",
                         color=color)
            vent_vs_vent(df=mf3_df, vent1=vent1, vent2=vent2, ini_v1=150000, ini_v2=160000, region="region 2",
                         color=color)
            vent_vs_vent(df=mf3_df, vent1=vent1, vent2=vent2, ini_v1=200000, ini_v2=210000, region="region 3",
                         color=color)


    def process_mf2(color):
        # Build a registry of Dataframes
        color = color.title()
        mf2_df = {}
        mf2_df['click'] = get_df(f"M2_{color}_25_Click.rwa", input_path)
        mf2_df['rescue'] = get_df(f"M2_{color}_25_Rescue.rwa", input_path)
        if color in ["Green", "Yellow"]:
            mf2_df['thorpe'] = get_df(f"M2_{color}_25_Thorpe.rwa", input_path)

        # Rescue vs Click
        vent1 = "rescue"
        vent2 = "click"

        # plot_waveforms(mf2_df[vent1].loc[160000:200000],vent1,color)
        # plot_waveforms(mf2_df[vent2].loc[150000:190000], vent2, color)

        vent_vs_vent(df=mf2_df, vent1=vent1, vent2=vent2, ini_v1=60000, ini_v2=60000, region="region 1", color=color)
        vent_vs_vent(df=mf2_df, vent1=vent1, vent2=vent2, ini_v1=160000, ini_v2=160000, region="region 2", color=color)
        vent_vs_vent(df=mf2_df, vent1=vent1, vent2=vent2, ini_v1=200000, ini_v2=200000, region="region 3", color=color)

        if color in ["Green", "Yellow"]:
            # Thorpe vs Click
            vent1 = "thorpe"
            vent2 = "click"

            vent_vs_vent(df=mf2_df, vent1=vent1, vent2=vent2, ini_v1=60000, ini_v2=60000, region="region 1",
                         color=color)
            vent_vs_vent(df=mf2_df, vent1=vent1, vent2=vent2, ini_v1=160000, ini_v2=160000, region="region 2",
                         color=color)
            vent_vs_vent(df=mf2_df, vent1=vent1, vent2=vent2, ini_v1=200000, ini_v2=200000, region="region 3",
                         color=color)


    # ---------------------------------------------------------------
    #  MAIN PROCESS - Plotter -
    # ---------------------------------------------------------------

    # source_file_name = "./data/15MAR21/raw_data/input/M2_Red_25_Rescue.rwa"
    # source_file_name = "./data/15MAR21/breath_data/input/M3_Red_Servo.bra"

    input_path = "./data/15MAR21/raw_data/input/"
    output_path = "./data/15MAR21/raw_data/output/"
    _RED = "red"
    _GREEN = "green"
    _YELLOW = "yellow"
    # Axis
    x = "Time (sec)"
    y = "Airway Pressure (cmH2O)"

    mft = "MF3@20LPM"
    # process_mf3(_GREEN)
    # process_mf3(_RED)
    # process_mf3(_YELLOW)

    mft = "MF2@25LPM"
    # process_mf2(_GREEN)
    # process_mf2(_RED)
    # process_mf2(_YELLOW)

    # Simple Workflow for a file
    # file_content = read_source_file(source_file_name)
    # # creates csv file out of content (cleansing not needed rows)
    # df = create_dataframe(file_content)
    # df = cleanse_dataframe(df)
    #
    # plot_summary(df)

    print('x')