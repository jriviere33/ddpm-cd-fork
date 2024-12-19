import matplotlib.pyplot as plt
import sys
import numpy as np

def plot_from_logs(logs_path, outputdir):
    with open(logs_path, 'r') as f:
        logs = f.read()

    logs = logs.splitlines()
    
    train_loss = []
    val_loss = []
    last = 0
    for i in range(len(logs)):
        if logs[i][:4] == 'l_cd':
            loss = logs[i].split(' ')[19]
            if last % 2 == 0:
                train_loss.append(float(loss))
            else:
                val_loss.append(float(loss))
            last += 1
    print(len(train_loss), len(val_loss))
    x = list(np.arange(len(train_loss)))
    # Plot the curves
    plt.plot(x, train_loss, label='train F1')
    plt.plot(x, val_loss, label='val F1')

    # Add labels and legend
    plt.xlabel('Epoch')
    plt.ylabel('F1')
    plt.title('Train and val F1')
    plt.legend()

    # Show the plot
    plt.savefig(outputdir+'/train_and_val_f1_plot.png')
    plt.show()
    



if __name__ == '__main__':
    log_path = sys.argv[1]
    output = sys.argv[2]

    plot_from_logs(log_path, output)
