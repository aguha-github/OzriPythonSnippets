import sys, os, time, datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import log_mining_cfg as cfg
from ags_admin import AgsAdmin

#Defines the entry point into the script
def main():  

    plotPath = "E:/Path/to/plot/results/"

    milliseconds_to_query = 86400000 # One day 
    
    # create instance of arcgis admin
    ags_admin = AgsAdmin(cfg.SERVER_NAME, cfg.SERVER_PORT, cfg.USER_NAME, cfg.PASSWORD)
    
    # define log parameters
    start_time = int(round(time.time() * 1000))
    end_time = start_time - milliseconds_to_query
    log_filter = "{'services':'*','server':'*','machines':'*'}"

    # query logs
    log_data = ags_admin.query_logs(start_time, end_time, log_filter)

    # collate the log data
    statistics = collate_log_data(log_data)

    # create the plot
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(6,12))

    # add the pie chart of request distribution
    construct_request_distribution_subplot(axes[0], statistics)

    # add the box plots of request performance
    construct_elapsed_times_boxplots(axes[1], statistics)

    # build up date time for file name
    date_time = datetime.datetime.now().isoformat('_')
    date_time = date_time.replace(':', '-')
    date_time = date_time[:date_time.index('.')]

    plot_file = os.path.join(plotPath, date_time + ".png")

    # save the file
    fig.savefig(plot_file, bbox_inches='tight')

    # open the file
    os.system("start " + plot_file)


def collate_log_data(log_data):
       
    statistics = {}

    # Iterate over messages to aggregate the statistics       
    for item in log_data["logMessages"]:
        
        if item["message"] == "End ExportMapImage":

            elapsed = float(item["elapsed"])
            key_check = item["source"]

            if key_check in statistics:
                stats_item = statistics[key_check]

                # Add 1 to tally of hits
                stats_item["count"] += 1
                
                # Add elapsed time to total elapsed time
                stats_item["elapsed"].append(elapsed)

            else:
                # Add key with one hit and total elapsed time
                statistics[key_check] = { "count": 1, "elapsed": [elapsed] }

    return statistics


def construct_request_distribution_subplot(axis, log_data):        

    # get the data and labels for the plot from the log data statistics
    data = [ log_data[key]["count"] for key in log_data ]
    labels = [ key for key in log_data ]

    axis.set_title('Percentage of Requests', fontsize=20)

    # create a list of sizes to explode the shapes in the pie chart.
    # in this case we are only exploding the largest section so each item is 0 except for the largest
    explode = [0] * len(labels)
    explode[data.index(max(data))] = 0.1

    axis.pie(data, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)


def construct_elapsed_times_boxplots(axis, log_data):

    # get the data and labels for the plot from the log data statistics
    elapsed_data = [ log_data[key]["elapsed"] for key in log_data ]
    labels = [ key for key in log_data ]

    palegreen = matplotlib.colors.colorConverter.to_rgb('#8CFF6F')

    axis.set_title('Request Times', fontsize=20)

    # Create the boxplot
    bp = axis.boxplot(elapsed_data)

    plt.setp(bp['boxes'], color='g')
    plt.setp(bp['whiskers'], color='g')
    plt.setp(bp['fliers'], color=palegreen, marker='+')

    num_boxes = len(elapsed_data)

    for index in range(num_boxes):
        box = bp['boxes'][index]
        boxX = []
        boxY = []

        for point in range(5):
            boxX.append(box.get_xdata()[point])
            boxY.append(box.get_ydata()[point])
            box_coords = zip(boxX, boxY)
            box_polygon = Polygon(box_coords, facecolor=palegreen)
            axis.add_patch(box_polygon)

    axis.set_xlim(0.5, num_boxes + 0.5)

    xtick_names = plt.setp(axis, xticklabels=labels)
    plt.setp(xtick_names, rotation=90, fontsize=8)

    axis.set_xlabel('Services')
    axis.set_ylabel('Elapsed Time (seconds)')


# Script start
if __name__ == "__main__":
    sys.exit(main())