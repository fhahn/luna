class Interpreter(object):
    def __init__(self, flags, frames):
        self.flags = flags
        self.frames = frames

    def run(self):
        while True:
            frame_ind = 0
            next_frame = self.frames[frame_ind]
            frame_ind += 1

            exit_status = next_frame.execute_frame()
            if exit_status == 1:
                break

        print("finished interpreting")
