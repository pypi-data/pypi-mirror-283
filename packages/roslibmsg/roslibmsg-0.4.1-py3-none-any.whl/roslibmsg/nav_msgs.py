from roslibpy import Message
from roslibmsg.geometry_msgs import PoseStamped,Pose

class Vector3(Message):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
        self._data = {'x': self.x, 'y': self.y, 'z': self.z}

    @property
    def data(self):
        self._data = {'x': self.x, 'y': self.y, 'z': self.z}
        return self._data
    
class Twist(Message):
    def __init__(self, linear=Vector3(), angular=Vector3()):
        self.linear = linear
        self.angular = angular

    @property
    def data(self):
        self._data = {
            'linear': self.linear.data,
            'angular': self.angular.data
        }
        return self._data

class Path(Message):
    def __init__(self, header=None, poses=None):
        self.header = header if header is not None else PoseStamped.Header()
        self.poses = poses if poses is not None else []

    @property
    def data(self):
        return {'header':self.header.data, 'poses': [pose.data for pose in self.poses]}

class Odometry(Message):
    def __init__(self, header=None, child_frame_id=None, pose=None, twist=None):
        self.header = header if header is not None else PoseStamped.Header()
        self.child_frame_id = child_frame_id if child_frame_id is not None else ''
        self.pose = pose if pose is not None else Pose()
        self.twist = twist if twist is not None else Twist()

    @property
    def data(self):
        return {'header':self.header.data, 'child_frame_id':self.child_frame_id, 'pose':self.pose.data, 'twist':self.twist.data}

if __name__ == '__main__':
    data = Odometry()
    print(data.data)