import ProcessPool as PP

resources = dict()
available = dict()


class Source:
    source_name = None
    number_of_source = 0
    source_id = 0

    def __init__(self, source_name, number_of_source):
        self.source_name = source_name
        self.number_of_source = number_of_source


def get_total_resource(resource_name):
    return resources[resource_name]


def define_new_resource(resource_name, number_of_resource):
    resources[resource_name] = number_of_resource
    available[resource_name] = number_of_resource


def assign_resources_to_process(request: dict, process: PP.Process):
    global available
    available_temp = available
    allocated_temp = process.allocated
    # define entry in dictionary
    for resource in request.keys():
        allocated = 0
        try:
            allocated = process.allocated[resource]
        except Exception:
            process.allocated[resource] = 0

        if process.claim[resource] - allocated < request[resource]:
            available = available_temp
            process.allocated = allocated_temp
            raise Exception(f"{process.process_name} requested more than what has already been claimed!")
        elif available[resource] < request[resource]:
            available = available_temp
            process.allocated = allocated_temp
            raise Exception(
                f"there is not {request[resource]} {resource}, to be assigned to {process.process_name}")
        else:
            available[resource] -= request[resource]
            process.allocated[resource] += request[resource]


def release_all_resources_from_process(process: PP.Process):
    for resource in process.claim.keys():
        available[resource] += process.allocated[resource]
        process.allocated[resource] = 0


# claim
def define_process_state(claim: dict, allocation: dict, process: PP.Process):
    for resource in claim.keys():
        if resources[resource] < claim[resource]:
            raise Exception(
                f"there is not {claim[resource]} {resource}, to be claimed from {process.process_name}")

        process.claim[resource] = claim[resource]

        if resources[resource] < allocation[resource]:
            raise Exception("there is not enough resource!")
        if process.claim[resource] < allocation[resource]:
            raise Exception("you are allocating more than you claim!")

        available[resource] -= allocation[resource]
        process.allocated[resource] = allocation[resource]

        process.resource_demand_rank += claim[resource] - allocation[resource]
