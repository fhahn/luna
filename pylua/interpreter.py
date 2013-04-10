class Interpreter(object):
    def __init__(self, flags, frames):
        self.flags = flags
        self.frames = frames
        self.num_frames = len(frames)

    def run(self):
        while True:
            frame_ind = 0
            next_frame = self.frames[frame_ind]
            frame_ind += 1

            returnvalue = next_frame.execute_frame()
            if returnvalue.w_returnvalue == 1 or frame_ind == self.num_frames:
                break

        print("finished interpreting")
