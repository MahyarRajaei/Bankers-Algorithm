import ProcessPool
import ResourceManager


def is_safe_state(process) -> bool:
    process.sort(key=lambda p: p.resource_demand_rank)
    p: ProcessPool.Process
    any_process_released = True

    while any_process_released:
        any_process_released = False
        for p in process:
            request = dict()
            for resource in p.claim.keys():
                request[resource] = p.claim[resource] - p.allocated[resource]

            try:
                ResourceManager.assign_resources_to_process(request, p)
                ResourceManager.release_all_resources_from_process(p)
                any_process_released = True
                print(p.process_name, "resources released!")
                process.remove(p)
            except Exception:
                pass

    return len(process) == 0


# taking input
process_list = []

print("Bankers Algorithm. this Algorithm is used to avoid deadlock.")
number_of_resources = int(input("enter number of resources:"))
for _ in range(number_of_resources):
    resource_name = input("enter resource name:")
    amount = int(input(f"enter amount of {resource_name}: "))
    ResourceManager.define_new_resource(resource_name, amount)

number_of_process = int(input("enter number of process:"))
for _ in range(number_of_process):
    process_name = input("enter process name:")
    process = ProcessPool.add_process(process_name)
    claim = dict()
    for resource in ResourceManager.resources.keys():
        claim_for_resource = int(input(f"enter claim for resource {resource}:"))
        claim[resource] = claim_for_resource

    allocated = dict()
    for resource in ResourceManager.resources.keys():
        allocated_of_resource = int(input(f"enter allocated for {resource}:"))
        allocated[resource] = allocated_of_resource

    ResourceManager.define_process_state(claim, allocated, process)
    process_list.append(process)

print("==========================================================================")


if __name__ == "__main__":
    is_safe = is_safe_state(process_list)
    if not is_safe:
        print("Deadlock!")
