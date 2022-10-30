import csv
import time

shut_down_data = {}
monitor_data = {}
res = []  # 0: event id, 1: shut_down_event_id, 2: sensor_id, 3: time1, 4: time2, 5: sub1, 6: sub2, 7: delta


def main():
    # read csv
    with open('shut_down_data_line_9.csv', 'r') as filein:
        lines = csv.reader(filein)
        for t in lines:  # index: event id, 0: ring id, 1: time restored, 3: elapsed
            shut_down_data[int(t[0])] = [int(t[1]), int(time.mktime(time.strptime(t[3], '%Y/%m/%d'))), float(t[4])]

    with open('sub_monitor_data_line_9.csv', 'r') as filein:
        lines = csv.reader(filein)
        cnt = 0
        tmp = []
        for t in lines:
            tmp.append(t)
            cnt += 1
        current_ring = int(tmp[0][1])
        monitor_data[current_ring] = []  # index: sensor (ring) id, inner index: time, 0: date, 1: data
        for t in tmp:
            if (int(t[1]) != current_ring):
                current_ring = int(t[1])
                monitor_data[current_ring] = []
            tmp = [int(time.mktime(time.strptime(t[4], '%Y/%m/%d'))), t[0], float(t[3])]
            monitor_data[current_ring].append(tmp)

    # process
    cnt_event = 0
    for shut_event_id, shut_content in shut_down_data.items():  # current shut event id
        for k in range(2 if ((shut_content[0] - 10) < 2) else shut_content[0] - 10,
                       shut_content[0] + 12 + 1):  # current ring
            if k in monitor_data:  # ring & sensor matched; below: to match the nearest time
                for pnt in range(0, len(monitor_data[k]) - 1):
                    if monitor_data[k][pnt][0] <= shut_content[1] <= monitor_data[k][pnt + 1][0]:
                        res.append([cnt_event, shut_event_id, k, monitor_data[k][pnt][1], monitor_data[k][pnt + 1][1],
                                    monitor_data[k][pnt][2], monitor_data[k][pnt + 1][2],
                                    monitor_data[k][pnt + 1][2] - monitor_data[k][pnt][2]])
                        cnt_event += 1

    # output
    with open('res1.csv', 'w', newline='') as fileout:
        writer = csv.writer(fileout)
        for t in res:
            writer.writerow(t)


if __name__ == '__main__':
    main()
