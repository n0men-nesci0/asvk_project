class InputInformation:
    def __init__(self, flag):
        self.is_file_correct = flag

    def set(self, number_of_cpu_, cpu_load_limits_,
            number_of_programs_, programs_load_, links_):
        self.number_of_cpu = number_of_cpu_  # int
        self.cpu_load_limits = cpu_load_limits_  # list
        self.number_of_programs = number_of_programs_  # int
        self.programs_load = programs_load_  # list
        self.links = links_  # dict (int,int)->int
        return self
