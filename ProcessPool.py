_process = dict()


def add_process(process_name):
    global _process
    process_id = len(_process) + 1
    process = Process(process_name, process_id)
    _process[process_name] = process
    return process


def get_process(process_name):
    return _process[process_name]


class Process:
    process_name = None
    process_id = 0
    resource_demand_rank = 0
    claim = None
    allocated = None

    def __init__(self, process_name, process_id):
        self.process_name = process_name
        self.process_id = process_id
        self.claim = dict()
        self.allocated = dict()

    def __str__(self):
        process = f"(id:{self.process_id}) {self.process_name}:\n"
        for resource in self.claim.keys():
            process += f"\t{resource} -> {self.claim[resource]}\n"
        return process

    def __cmp__(self, other):
        return self.resource_demand_rank - other.resource_demand_rank

    def __eq__(self, other):
        return self.process_name == other.process_name

