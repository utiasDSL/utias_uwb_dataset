'''
Visualize the sensor measurements in rosbag.
Visualize all the UWB tdoa2 measurements
'''
import os, sys
import argparse
import numpy as np
from numpy import linalg
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import matplotlib.style as style
import rosbag
# select the matplotlib plotting style
style.use('ggplot')
# set window background to white
plt.rcParams['figure.facecolor'] = 'w'


if __name__ == "__main__":
    # ---------------- access anchor survey and rosbag ---------------- #
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', nargs=2)
    args = parser.parse_args()
    
    # access the survey results
    anchor_npz = args.i[0]
    anchor_survey = np.load(anchor_npz)
    anchor_pos = anchor_survey['an_pos']
    anchor_qaut = anchor_survey['an_quat']
    
    # print out
    anchor_file = os.path.split(sys.argv[-2])[1]
    print("loading anchor survey results: " + str(anchor_file) + "\n")

    # access rosbag
    ros_bag = args.i[1]
    bag = rosbag.Bag(ros_bag)
    bag_file = os.path.split(sys.argv[-1])[1]

    # print out
    bag_name = os.path.splitext(bag_file)[0]
    print("visualizing rosbag: " + str(bag_file) + "\n")

    # -------------------- extract the rosbag ----------------------------- #
    acc = [];   gyro = [];  flow = [];  tdoa = [];  tof = [];  baro = [] 
    imu = []  # combined IMU data
    gt_pose = [] 

    for topic, msg, t in bag.read_messages(['/accel_data', '/gyro_data', '/flow_data', '/tdoa_data', '/tof_data', '/baro_data', '/pose_data', "/imu_data"]):
        if topic == '/accel_data':
            acc.append([msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9,
                        msg.x, msg.y, msg.z])
        if topic == '/gyro_data':
            gyro.append([msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9,
                        msg.x, msg.y, msg.z])
        if topic == '/flow_data':
            flow.append([msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9,
                        msg.deltaX, msg.deltaY])
        if topic == '/tdoa_data':
            tdoa.append([msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9,
                        msg.idA, msg.idB, msg.data])
        if topic == "/tof_data":
            tof.append([msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9,
                        msg.zrange])
        if topic == "/baro_data":
            baro.append([msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9,
                        msg.asl])
        if topic == "/pose_data":
            gt_pose.append([msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9,
                            msg.pose.pose.position.x,    msg.pose.pose.position.y,    msg.pose.pose.position.z, msg.pose.pose.orientation.x, msg.pose.pose.orientation.y,
                            msg.pose.pose.orientation.z, msg.pose.pose.orientation.w ])
        if topic == "/imu_data":
            imu.append([msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9,
                        msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z,
                        msg.angular_velocity.x,    msg.angular_velocity.y,    msg.angular_velocity.z])
            
            
    # convert to numpy array
    acc = np.array(acc);     gyro = np.array(gyro)
    flow = np.array(flow);   tdoa = np.array(tdoa)
    tof = np.array(tof);     baro = np.array(baro)
    imu = np.array(imu)

    gt_pose = np.array(gt_pose)

    # select the anchor pair for visualization
    # possible anchor ID = [0,1,2,3,4,5,6,7] 

    # get the id for tdoa_ij measurements
    tdoa_70 = np.where((tdoa[:,1]==[7])&(tdoa[:,2]==[0]))
    tdoa_meas_70 = np.squeeze(tdoa[tdoa_70, :])

    tdoa_01 = np.where((tdoa[:,1]==[0])&(tdoa[:,2]==[1]))
    tdoa_meas_01 = np.squeeze(tdoa[tdoa_01, :])

    tdoa_12 = np.where((tdoa[:,1]==[1])&(tdoa[:,2]==[2]))
    tdoa_meas_12 = np.squeeze(tdoa[tdoa_12, :])

    tdoa_23 = np.where((tdoa[:,1]==[2])&(tdoa[:,2]==[3]))
    tdoa_meas_23 = np.squeeze(tdoa[tdoa_23, :])

    tdoa_34 = np.where((tdoa[:,1]==[3])&(tdoa[:,2]==[4]))
    tdoa_meas_34 = np.squeeze(tdoa[tdoa_34, :])

    tdoa_45 = np.where((tdoa[:,1]==[4])&(tdoa[:,2]==[5]))
    tdoa_meas_45 = np.squeeze(tdoa[tdoa_45, :])

    tdoa_56 = np.where((tdoa[:,1]==[5])&(tdoa[:,2]==[6]))
    tdoa_meas_56 = np.squeeze(tdoa[tdoa_56, :])

    tdoa_67 = np.where((tdoa[:,1]==[6])&(tdoa[:,2]==[7]))
    tdoa_meas_67 = np.squeeze(tdoa[tdoa_67, :])

    # visual r_nrr
    # note: in tdoa2, there are a few meas. doesn't follow the round-robbin mechanism
    t_nrr_id = np.where((tdoa[:,2]-tdoa[:,1]!=1) & (tdoa[:,2]-tdoa[:,1]!=-7))
    r_nrr = np.squeeze(tdoa[t_nrr_id, :])
    # compute the gt for r_nrr
    gt_nrr = []
    for idx in range(len(r_nrr)):
        anchor_i = anchor_pos[int(r_nrr[idx,1]),:].reshape(1,-1)
        anchor_j = anchor_pos[int(r_nrr[idx,2]),:].reshape(1,-1)
        cf_x = np.interp(r_nrr[idx,0], gt_pose[:,0], gt_pose[:,1])
        cf_y = np.interp(r_nrr[idx,0], gt_pose[:,0], gt_pose[:,2])
        cf_z = np.interp(r_nrr[idx,0], gt_pose[:,0], gt_pose[:,3])
        cf = np.array([cf_x, cf_y, cf_z]).reshape(1,-1)
        dis_i = np.asarray(linalg.norm(anchor_i - cf, axis = 1))
        dis_j = np.asarray(linalg.norm(anchor_j - cf, axis = 1))
        dis_ij = dis_j - dis_i
        gt_nrr.append(dis_ij)

    gt_nrr = np.array(gt_nrr)

    # compute the ground truth for tdoa_ij
    an_pos_0 = anchor_pos[0,:].reshape(1,-1)
    an_pos_1 = anchor_pos[1,:].reshape(1,-1)
    an_pos_2 = anchor_pos[2,:].reshape(1,-1)
    an_pos_3 = anchor_pos[3,:].reshape(1,-1)
    an_pos_4 = anchor_pos[4,:].reshape(1,-1)
    an_pos_5 = anchor_pos[5,:].reshape(1,-1)
    an_pos_6 = anchor_pos[6,:].reshape(1,-1)
    an_pos_7 = anchor_pos[7,:].reshape(1,-1)
    # cf position from vicon measurement
    cf_pos = gt_pose[:,1:4]      # [x, y, z]
    d_0 = np.asarray(linalg.norm(an_pos_0 - cf_pos, axis = 1))
    d_1 = np.asarray(linalg.norm(an_pos_1 - cf_pos, axis = 1))
    d_2 = np.asarray(linalg.norm(an_pos_2 - cf_pos, axis = 1))
    d_3 = np.asarray(linalg.norm(an_pos_3 - cf_pos, axis = 1))
    d_4 = np.asarray(linalg.norm(an_pos_4 - cf_pos, axis = 1))
    d_5 = np.asarray(linalg.norm(an_pos_5 - cf_pos, axis = 1))
    d_6 = np.asarray(linalg.norm(an_pos_6 - cf_pos, axis = 1))
    d_7 = np.asarray(linalg.norm(an_pos_7 - cf_pos, axis = 1))
    # measurement model
    d_70 = d_0 - d_7
    d_01 = d_1 - d_0
    d_12 = d_2 - d_1
    d_23 = d_3 - d_2

    d_34 = d_4 - d_3
    d_45 = d_5 - d_4
    d_56 = d_6 - d_5
    d_67 = d_7 - d_6
    # visualization 
    # UWB TDOA
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(221)
    ax1.scatter(tdoa_meas_70[:,0], tdoa_meas_70[:,3], color = "steelblue", s = 2.5, alpha = 0.9, label = "tdoa measurements")
    ax1.plot(gt_pose[:,0], d_70, color='red',linewidth=1.5, label = "Vicon ground truth")
    ax1.legend(loc='best')
    ax1.set_xlabel(r'Time [s]')
    ax1.set_ylabel(r'TDoA measurement [m]') 
    plt.title(r"UWB tdoa measurements, (An7, An0)", fontsize=13, fontweight=0, color='black')

    bx1 = fig1.add_subplot(222)
    bx1.scatter(tdoa_meas_01[:,0], tdoa_meas_01[:,3], color = "steelblue", s = 2.5, alpha = 0.9, label = "tdoa measurements")
    bx1.plot(gt_pose[:,0], d_01, color='red',linewidth=1.5, label = "Vicon ground truth")
    bx1.legend(loc='best')
    bx1.set_xlabel(r'Time [s]')
    bx1.set_ylabel(r'TDoA measurement [m]') 
    plt.title(r"UWB tdoa measurements, (An0, An1)", fontsize=13, fontweight=0, color='black')


    cx1 = fig1.add_subplot(223)
    cx1.scatter(tdoa_meas_12[:,0], tdoa_meas_12[:,3], color = "steelblue", s = 2.5, alpha = 0.9, label = "tdoa measurements")
    cx1.plot(gt_pose[:,0], d_12, color='red',linewidth=1.5, label = "Vicon ground truth")
    cx1.legend(loc='best')
    cx1.set_xlabel(r'Time [s]')
    cx1.set_ylabel(r'TDoA measurement [m]') 
    plt.title(r"UWB tdoa measurements, (An1, An2)", fontsize=13, fontweight=0, color='black')

    dx1 = fig1.add_subplot(224)
    dx1.scatter(tdoa_meas_23[:,0], tdoa_meas_23[:,3], color = "steelblue", s = 2.5, alpha = 0.9, label = "tdoa measurements")
    dx1.plot(gt_pose[:,0], d_23, color='red',linewidth=1.5, label = "Vicon ground truth")
    dx1.legend(loc='best')
    dx1.set_xlabel(r'Time [s]')
    dx1.set_ylabel(r'TDoA measurement [m]') 
    plt.title(r"UWB tdoa measurements, (An2, An3)", fontsize=13, fontweight=0, color='black')


    fig2 = plt.figure()
    ax2 = fig2.add_subplot(221)
    ax2.scatter(tdoa_meas_34[:,0], tdoa_meas_34[:,3], color = "steelblue", s = 2.5, alpha = 0.9, label = "tdoa measurements")
    ax2.plot(gt_pose[:,0], d_34, color='red',linewidth=1.5, label = "Vicon ground truth")
    ax2.legend(loc='best')
    ax2.set_xlabel(r'Time [s]')
    ax2.set_ylabel(r'TDoA measurement [m]') 
    plt.title(r"UWB tdoa measurements, (An3, An4)", fontsize=13, fontweight=0, color='black')

    bx2 = fig2.add_subplot(222)
    bx2.scatter(tdoa_meas_45[:,0], tdoa_meas_45[:,3], color = "steelblue", s = 2.5, alpha = 0.9, label = "tdoa measurements")
    bx2.plot(gt_pose[:,0], d_45, color='red',linewidth=1.5, label = "Vicon ground truth")
    bx2.legend(loc='best')
    bx2.set_xlabel(r'Time [s]')
    bx2.set_ylabel(r'TDoA measurement [m]') 
    plt.title(r"UWB tdoa measurements, (An4, An5)", fontsize=13, fontweight=0, color='black')

    cx2 = fig2.add_subplot(223)
    cx2.scatter(tdoa_meas_56[:,0], tdoa_meas_56[:,3], color = "steelblue", s = 2.5, alpha = 0.9, label = "tdoa measurements")
    cx2.plot(gt_pose[:,0], d_56, color='red',linewidth=1.5, label = "Vicon ground truth")
    cx2.legend(loc='best')
    cx2.set_xlabel(r'Time [s]')
    cx2.set_ylabel(r'TDoA measurement [m]') 
    plt.title(r"UWB tdoa measurements, (An5, An6)", fontsize=13, fontweight=0, color='black')

    dx2 = fig2.add_subplot(224)
    dx2.scatter(tdoa_meas_67[:,0], tdoa_meas_67[:,3], color = "steelblue", s = 2.5, alpha = 0.9, label = "tdoa measurements")
    dx2.plot(gt_pose[:,0], d_67, color='red',linewidth=1.5, label = "Vicon ground truth")
    dx2.legend(loc='best')
    dx2.set_xlabel(r'Time [s]')
    dx2.set_ylabel(r'TDoA measurement [m]') 
    plt.title(r"UWB tdoa measurements, (An6, An7)", fontsize=13, fontweight=0, color='black')

    # TDOA2 r_nrr
    # note: In tdoa2, there are a few measurements that are not in round robbin, yet the measurement error is closed to zero mean.
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(r_nrr[:,0], np.squeeze(gt_nrr) - r_nrr[:,3], color='red', s = 2.5, alpha = 0.9, label = "r_nrr error")
    ax.legend(loc='best')
    ax.set_xlabel(r'Time [s]')
    ax.set_ylabel(r'TDoA measurement error [m]') 
    plt.title(r"UWB tdoa2 measurements error (not in round robbin),", fontsize=13, fontweight=0, color='black')

    # Z-range ToF
    fig3 = plt.figure()
    ax3 = fig3.add_subplot(111)
    ax3.scatter(tof[:,0], tof[:,1], color = "steelblue", s = 2.5, alpha = 0.9, label = "tof measurements")
    ax3.plot(gt_pose[:,0], gt_pose[:,3], color='red',linewidth=1.5, label = "Vicon ground truth")
    ax3.legend(loc='best')
    ax3.set_xlabel(r'Time [s]')
    ax3.set_ylabel(r'ToF measurement [m]') 
    plt.title(r"Z-range measurements", fontsize=13, fontweight=0, color='black')

    # flow pixel
    fig4 = plt.figure()
    ax4 = fig4.add_subplot(211)
    plt.title(r"Optical flow measurements", fontsize=13, fontweight=0, color='black')
    ax4.scatter(flow[:,0], flow[:,1], color = "steelblue", s = 2.5, alpha = 0.9, label = "flow dpixel x")
    ax4.set_ylabel(r'number of accelerated pixel in x') 
    bx4 = fig4.add_subplot(212)
    bx4.scatter(flow[:,0], flow[:,2], color = "steelblue", s = 2.5, alpha = 0.9, label = "flow dpixel y")
    bx4.set_ylabel(r'number of accelerated pixel in y') 
    bx4.set_xlabel(r'Time [s]')
    plt.legend(loc='best')

    # baremeter
    fig4 = plt.figure()
    ax4 = fig4.add_subplot(111)
    plt.title(r"Baro measurements", fontsize=13, fontweight=0, color='black')
    ax4.scatter(baro[:,0], baro[:,1], color = "steelblue", s = 2.5, alpha = 0.9, label = "baro asl")
    ax4.set_ylabel(r'asl') 
    plt.legend(loc='best')

    # trajectory
    fig5 = plt.figure()
    ax_t = fig5.add_subplot(111, projection = '3d')
    ax_t.plot(gt_pose[:,1],gt_pose[:,2],gt_pose[:,3],color='steelblue',linewidth=1.9, alpha=0.9)
    ax_t.scatter(anchor_pos[:,0], anchor_pos[:,1], anchor_pos[:,2], marker='o',color='red')
    ax_t.set_xlim3d(np.amin(anchor_pos[:,0])-0.5, np.amax(anchor_pos[:,0])+0.5)  
    ax_t.set_ylim3d(np.amin(anchor_pos[:,1])-0.5, np.amax(anchor_pos[:,1])+0.5)  
    ax_t.set_zlim3d(np.amin(anchor_pos[:,2])-0.1, np.amax(anchor_pos[:,2])+0.3)  
    ax_t.set_xlabel(r'X [m]')
    ax_t.set_ylabel(r'Y [m]')
    ax_t.set_zlabel(r'Z [m]')
    plt.legend(['Trajectory','Anchor position'])
    plt.title(r"Trajectory of the experiment", fontsize=13, fontweight=0, color='black', style='italic', y=1.02 )

    # plot separate x,y,z
    fig6 = plt.figure()
    a_x = fig6.add_subplot(311)
    a_x.plot(gt_pose[:,0],gt_pose[:,1],color='steelblue',linewidth=1.9, alpha=0.9, label = "Vicon gt x")
    a_x.legend(loc='best')
    a_y = fig6.add_subplot(312)
    a_y.plot(gt_pose[:,0],gt_pose[:,2],color='steelblue',linewidth=1.9, alpha=0.9, label = "Vicon gt y")
    a_y.legend(loc='best')
    a_z = fig6.add_subplot(313)
    a_z.plot(gt_pose[:,0],gt_pose[:,3],color='steelblue',linewidth=1.9, alpha=0.9, label = "Vicon gt z")
    a_z.legend(loc='best')
    a_z.set_xlabel(r'Time [s]')

    plt.title(r"Ground truth of the experiment", fontsize=13, fontweight=0, color='black', style='italic', y=1.02 )

    plt.show()