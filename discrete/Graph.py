from ForwardKinematics import Px,Py,Pz
from Node import Node
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
from mpl_toolkits.mplot3d import Axes3D
from math import sqrt


def heuristic(config,goal_state):
    hq = np.square(np.array(goal_state)-np.array(config))
    hq = np.sum(hq)
    hq = np.sqrt(hq)
    return hq


class Graph:
    def __init__(self):
        self.nodelist = []
        self.obstaclelist = []
        self.connection_idx = []

    def put_node(self,Node):
        (q1,q2,q3,q4,q5) = Node.config[0],Node.config[1],Node.config[2],Node.config[3],Node.config[4]
        x = Px(q1,q2,q3,q4,q5)
        y = Py(q1,q2,q3,q4,q5)
        z = Pz(q1,q2,q3,q4,q5)
        intersect = 0
        if z<0:
            intersect = 1
        if intersect == 0:
            for i in self.obstaclelist:
                if i.twopoint[0][0] < x and i.twopoint[1][0] > x and i.twopoint[0][1] < y and i.twopoint[1][1] > y and i.twopoint[0][2] < z and i.twopoint[1][2] > z:
                    intersect = 1
                    break
        if intersect == 0:
            self.nodelist.append(Node)

    def put_obstacle(self,obstacle):
        self.obstaclelist.append(obstacle)

    def visualize15z(self):
        pointlist = []
        for i in self.nodelist:
            (q1, q2, q3, q4, q5) = i.config[0], i.config[1], i.config[2], i.config[3], i.config[4]
            z = Pz(q1, q2, q3, q4, q5)
            pointlist.append([q1,q5,z])
        np_pointlist = np.array(pointlist)
        q1list = np_pointlist[:,0]
        q5list = np_pointlist[:,1]
        zlist = np_pointlist[:, 2]
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.scatter(q1list,q5list,zlist)
        for i in self.connection_idx:
            config_a = self.nodelist[i[0]].config
            config_b = self.nodelist[i[1]].config
            z_1 = Pz(config_a[0],config_a[1],config_a[2],config_a[3],config_a[4])
            z_2 = Pz(config_b[0],config_b[1],config_b[2],config_b[3],config_b[4])
            q1 = [config_a[0],config_b[0]]
            q5 = [config_a[4],config_b[4]]
            z = [z_1,z_2]
            ax.plot(q1,q5,z, color='red')
        plt.show(ax)

    def visualizexyz(self):
        xlist = []
        ylist = []
        zlist = []
        for i in self.nodelist:
            (q1, q2, q3, q4, q5) = i.config[0], i.config[1], i.config[2], i.config[3], i.config[4]
            x = Px(q1, q2, q3, q4, q5)
            y = Py(q1, q2, q3, q4, q5)
            z = Pz(q1, q2, q3, q4, q5)
            xlist.append(x)
            ylist.append(y)
            zlist.append(z)
        x_np = np.array(xlist)
        y_np = np.array(ylist)
        z_np = np.array(zlist)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.scatter(x_np, y_np, z_np)

        for i in self.obstaclelist:
            xmin,ymin,zmin = i.twopoint[0]
            xmax,ymax,zmax = i.twopoint[1]
            sq1 = np.array([[xmin,ymin,zmin],[xmin,ymin,zmax],[xmax,ymin,zmax],[xmax,ymin,zmin]])
            sq2 = np.array([[xmin,ymin,zmin],[xmin,ymax,zmin],[xmax,ymax,zmin],[xmax,ymin,zmin]])
            sq3 = np.array([[xmin,ymin,zmin],[xmin,ymin,zmax],[xmin,ymax,zmax],[xmin,ymax,zmin]])
            sq4 = np.array([[xmin,ymin,zmax],[xmin,ymax,zmax],[xmax,ymax,zmax],[xmax,ymin,zmax]])
            sq5 = np.array([[xmax,ymin,zmin],[xmax,ymax,zmin],[xmax,ymax,zmax],[xmax,ymin,zmax]])
            sq6 = np.array([[xmin,ymax,zmin],[xmax,ymax,zmin],[xmax,ymax,zmax],[xmin,ymax,zmax]])
            squarelist = [sq1,sq2,sq3,sq4,sq5,sq6]
            for i in squarelist:
                x = i[:,0]
                y = i[:,1]
                z = i[:,2]
                verts = [list(zip(x,y,z))]
                pc = Poly3DCollection(verts,facecolors='g')
                line = Line3DCollection(verts, colors='k', linewidths=0.5)
                ax.add_collection3d(pc)
                ax.add_collection(line)
        for i in self.connection_idx:
            config_a = self.nodelist[i[0]].config
            config_b = self.nodelist[i[1]].config
            x_1 = Px(config_a[0],config_a[1],config_a[2],config_a[3],config_a[4])
            y_1 = Py(config_a[0],config_a[1],config_a[2],config_a[3],config_a[4])
            z_1 = Pz(config_a[0],config_a[1],config_a[2],config_a[3],config_a[4])
            x_2 = Px(config_b[0],config_b[1],config_b[2],config_b[3],config_b[4])
            y_2 = Py(config_b[0],config_b[1],config_b[2],config_b[3],config_b[4])
            z_2 = Pz(config_b[0],config_b[1],config_b[2],config_b[3],config_b[4])
            x = [x_1,x_2]
            y = [y_1,y_2]
            z = [z_1,z_2]
            ax.plot(x,y,z,color='red')
        plt.show(ax)

    def connect_graph(self):
        for a in range(len(self.nodelist)):
            for b in range(len(self.nodelist)):
                if self.nodelist[a] == self.nodelist[b] or (b,a) in self.connection_idx or (a,b) in self.connection_idx:
                    continue
                no_colission = True
                q1 = np.array(self.nodelist[a].config)
                q2 = np.array(self.nodelist[b].config)
                diff = q1-q2
                dis_s = np.square(diff)
                sum = np.sum(dis_s)
                dis = np.sqrt(sum)
                if dis > 1.5:
                    # print('check1')
                    continue
                percentile = [0.2,0.4,0.6,0.8]
                for c in percentile:
                    config = q1 + c*(q2-q1)
                    q1_i,q2_i,q3_i,q4_i,q5_i = config.tolist()
                    # print(q1_i,q2_i,q3_i,q4_i,q5_i)
                    x = Px(q1_i,q2_i,q3_i,q4_i,q5_i)
                    y = Py(q1_i,q2_i,q3_i,q4_i,q5_i)
                    z = Pz(q1_i,q2_i,q3_i,q4_i,q5_i)
                    # print(x,y,z)
                    for d in self.obstaclelist:
                        # print(d.twopoint)
                        if d.twopoint[0][0] <= x and d.twopoint[1][0] >= x and d.twopoint[0][1] <= y and d.twopoint[1][1] >= y and d.twopoint[0][2] <= z and d.twopoint[1][2] >= z:
                            no_colission = False
                            break
                    if no_colission == False:
                        break
                # print(no_colission)
                if no_colission:
                    # print('check1')
                    self.connection_idx.append((a,b))
                    self.nodelist[a].connectedNode.append(b)
                    self.nodelist[b].connectedNode.append(a)

    def astar(self,q_init,q_goal):
        Node_init = Node(q_init)
        Node_goal = Node(q_goal)
        self.put_node(Node_init)
        self.put_node(Node_goal)
        self.connect_graph()
        current_Node = self.nodelist[len(self.nodelist)-2]
        Node_goal = self.nodelist[len(self.nodelist)-1]
        path = [current_Node.config]
        cost = 0
        scorelist = []
        nodelist = []
        layer = 1
        layerlist = []
        costlist = []
        while current_Node != Node_goal:
            for i in range(len(current_Node.connectedNode)):
                Node_i = self.nodelist[current_Node.connectedNode[i]]
                cost_i = cost + heuristic(current_Node.config,Node_i.config)
                h = heuristic(Node_i.config,Node_goal.config)
                scorelist.append(h+cost_i)
                nodelist.append((layer,Node_i))
                costlist.append(cost_i)
            if layer != 1:
                idx_previous = scorelist.index(previous_score)
                scorelist.remove(scorelist[idx_previous])
                nodelist.remove(nodelist[idx_previous])
                costlist.remove(costlist[idx_previous])
            idx = scorelist.index(min(scorelist))
            if nodelist[idx][0] < layer:
                diff = layer -nodelist[idx][0]
                for j in range(diff):
                    path.remove(path[len(path)-1])
                layer = nodelist[idx][0]
            print(layer)
            cost = costlist[idx]
            layerlist.append(layer)
            current_Node = nodelist[idx][1]
            layer+=1
            path.append(current_Node.config)
            previous_score = min(scorelist)
        return path

