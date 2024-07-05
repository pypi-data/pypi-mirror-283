from roslibpy import Message
from .geometry_msgs import PoseStamped, Pose
from .nav_msgs import  Path


class String(Message):
    def __init__(self, data=''):
        self._data = {
            'data': str(data)
        }

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data['data'] = str(value)



if __name__ == '__main__':
    data = Twist()
    print(data)
