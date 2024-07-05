from roslibpy import Message

class Pose(Message):
    class __Position(Message):
        def __init__(self, x=0.0, y=0.0, z=0.0):
            self.x = x
            self.y = y
            self.z = z
        @property
        def data(self):
            return {'x': self.x, 'y': self.y, 'z': self.z}

    class __Orientation(Message):
        def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
            self.x = x
            self.y = y
            self.z = z
            self.w = w
        @property
        def data(self):
            return {'x': self.x, 'y': self.y, 'z': self.z, 'w': self.w}
        
    
    def __init__(self, position=None, orientation=None):
        self.position = position if position is not None else Pose.__Position()
        self.orientation = orientation if orientation is not None else Pose.__Orientation()

    @property
    def data(self):
        return {'position': self.position.data, 'orientation': self.orientation.data }
    

class PoseStamped(Message):
    class Stamp(Message):
        def __init__(self, secs=0, nsecs=0):
            self.secs = secs
            self.nsecs = nsecs

        @property
        def data(self):
            return {'secs': self.secs, 'nsecs': self.nsecs}
        

    class Header(Message):
        def __init__(self, stamp=None, frame_id='map'):
            self.stamp = stamp if stamp is not None else PoseStamped.Stamp()
            self.frame_id = frame_id

        @property
        def data(self):
            return {'stamp': self.stamp.data, 'frame_id': self.frame_id}

        

    def __init__(self, header=None, pose=None):
        self.header = header if header is not None else PoseStamped.Header()
        self.pose = pose if pose is not None else Pose()

    @property
    def data(self):
        return {'header': self.header.data, 'pose': self.pose.data}
    

if __name__ == '__main__':
    data = PoseStamped()
    print(data)