import os, time
import vlc
from time import sleep
from onvif import ONVIFCamera
import zeep

class Player:
    '''
        args:设置 options
    '''
    def __init__(self, *args):
        if args:
            instance = vlc.Instance(*args)
            self.media = instance.media_player_new()
        else:
            self.media = vlc.MediaPlayer()

    # 设置待播放的url地址或本地文件路径，每次调用都会重新加载资源
    def set_uri(self, uri):
        self.media.set_mrl(uri)

    # 播放 成功返回0，失败返回-1
    def play(self, path=None):
        if path:
            self.set_uri(path)
            return self.media.play()
        else:
            return self.media.play()

    # 暂停
    def pause(self):
        self.media.pause()

    # 恢复
    def resume(self):
        self.media.set_pause(0)

    # 停止
    def stop(self):
        self.media.stop()

    # 释放资源
    def release(self):
        return self.media.release()

    # 是否正在播放
    def is_playing(self):
        return self.media.is_playing()

    # 已播放时间，返回毫秒值
    def get_time(self):
        return self.media.get_time()

    # 拖动指定的毫秒值处播放。成功返回0，失败返回-1 (需要注意，只有当前多媒体格式或流媒体协议支持才会生效)
    def set_time(self, ms):
        return self.media.get_time()

    # 音视频总长度，返回毫秒值
    def get_length(self):
        return self.media.get_length()

    # 获取当前音量（0~100）
    def get_volume(self):
        return self.media.audio_get_volume()

    # 设置音量（0~100）
    def set_volume(self, volume):
        return self.media.audio_set_volume(volume)

    # 返回当前状态：正在播放；暂停中；其他
    def get_state(self):
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1

    # 当前播放进度情况。返回0.0~1.0之间的浮点数
    def get_position(self):
        return self.media.get_position()

    # 拖动当前进度，传入0.0~1.0之间的浮点数(需要注意，只有当前多媒体格式或流媒体协议支持才会生效)
    def set_position(self, float_val):
        return self.media.set_position(float_val)

    # 获取当前文件播放速率
    def get_rate(self):
        return self.media.get_rate()

    # 设置播放速率（如：1.2，表示加速1.2倍播放）
    def set_rate(self, rate):
        return self.media.set_rate(rate)

    # 设置宽高比率（如"16:9","4:3"）
    def set_ratio(self, ratio):
        self.media.video_set_scale(0)  # 必须设置为0，否则无法修改屏幕宽高
        self.media.video_set_aspect_ratio(ratio)

    # 注册监听器
    def add_callback(self, event_type, callback):
        self.media.event_manager().event_attach(event_type, callback)

    # 移除监听器
    def remove_callback(self, event_type, callback):
        self.media.event_manager().event_detach(event_type, callback)

    def my_call_back(event):
        print("call:", player.get_time())
class onvif():
    XMAX = 0.1
    XMIN = -0.1
    YMAX = 0.1
    YMIN = -0.1
    def zeep_pythonvalue(self, xmlvalue):
        return xmlvalue


    def perform_move(ptz, request, timeout):
        # Start continuous move
        ptz.ContinuousMove(request)
        # Wait a certain time
        sleep(timeout)
        # Stop continuous move
        ptz.Stop({'ProfileToken': request.ProfileToken})


    def move_up(ptz, request, timeout=0.5):
        print('move up...')
        request.Velocity.PanTilt.x = 0
        request.Velocity.PanTilt.y = YMAX
        onvif.perform_move(ptz, request, timeout)


    def move_down(ptz, request, timeout=0.5):
        print('move down...')
        request.Velocity.PanTilt.x = 0
        request.Velocity.PanTilt.y = YMIN
        onvif.perform_move(ptz, request, timeout)


    def move_right(ptz, request, timeout=0.5):
        print('move right...')
        request.Velocity.PanTilt.x = XMAX
        request.Velocity.PanTilt.y = 0
        onvif.perform_move(ptz, request, timeout)


    def move_left(ptz, request, timeout=0.5):
        print('move left...')
        request.Velocity.PanTilt.x = XMIN
        request.Velocity.PanTilt.y = 0
        onvif.perform_move(ptz, request, timeout)


    def continuous_move():
        mycam = ONVIFCamera('192.168.1.99', 80, 'admin', 'admin111')
        # Create media service object
        media = mycam.create_media_service()
        # Create ptz service object
        ptz = mycam.create_ptz_service()

        # Get target profile
        zeep.xsd.simple.AnySimpleType.pythonvalue = onvif.zeep_pythonvalue
        media_profile = media.GetProfiles()[0]

        # Get PTZ configuration options for getting continuous move range
        request = ptz.create_type('GetConfigurationOptions')
        request.ConfigurationToken = media_profile.PTZConfiguration.token
        ptz_configuration_options = ptz.GetConfigurationOptions(request)

        request = ptz.create_type('ContinuousMove')
        request.ProfileToken = media_profile.token
        ptz.Stop({'ProfileToken': media_profile.token})

        if request.Velocity is None:
            request.Velocity = ptz.GetStatus({'ProfileToken': media_profile.token}).Position
            request.Velocity = ptz.GetStatus({'ProfileToken': media_profile.token}).Position
            request.Velocity.PanTilt.space = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].URI
            request.Velocity.Zoom.space = ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].URI

        # Get range of pan and tilt
        # NOTE: X and Y are velocity vector
        global XMAX, XMIN, YMAX, YMIN
        XMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
        XMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min
        YMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max
        YMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min

        while True :
            control = input('请输入云台控制指令，上下左右：w s a d ')

            if control == 'a':
                    # move right
                    onvif.move_right(ptz, request)
            if control == 'd':
                    # move left
                    onvif.move_left(ptz, request)
            if control == 'w':
                    # Move up
                    onvif.move_up(ptz, request)
            if control == 's':
                    # move down
                    onvif.move_down(ptz, request)

if "__main__" == __name__:
    player = Player()
    #player.add_callback(vlc.EventType.MediaPlayerTimeChanged, Player.my_call_back)
    # 在线播放流媒体视频
    player.play("rtsp://admin:admin111@192.168.1.99/Streaming/Channels/1")

    # 播放本地mp3
    # player.play("D:/abc.mp3")

    # 防止当前进程退出
    while True:
        pass
        onvif.continuous_move()




