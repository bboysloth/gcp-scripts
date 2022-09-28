# For listing out all compute instances which have a GPU attached to them
# python
# Jeremy Hannan - June 2022

import subprocess
import json
import csv

def exec(command):
    output = subprocess.run(
                command, 
                shell=True,
                capture_output=True
            ).stdout

    if len(output)>0:
        return json.loads(output)
    else: return []

gpu_list = []
for project in exec("gcloud alpha projects list --format='json'"):
    
    for instance in exec(f"gcloud compute instances list --project={project['projectId']} --format='json' --quiet"):
        # print(instance["name"], instance["zone"])

        gpu_info = exec(f"gcloud compute instances describe --project={project['projectId']} --zone={instance['zone']} --format='json' --quiet {instance['name']}")
        if "guestAccelerators" in gpu_info:
            for accel in gpu_info["guestAccelerators"]:
                gpu_list.append({
                    "project_id": project['projectId'], 
                    "project_name": project['name'], 
                    "instance_name": gpu_info["name"], 
                    "status": gpu_info["status"], 
                    "zone": gpu_info["zone"].split("/")[-1], 
                    "acceleratorType": accel["acceleratorType"].split("/")[-1],
                    "acceleratorCount": accel["acceleratorCount"]
                })
        else:
            gpu_list.append({
                "project_id": project['projectId'], 
                "project_name": project['name'], 
                "instance_name": gpu_info["name"], 
                "status": gpu_info["status"], 
                "zone": gpu_info["zone"].split("/")[-1], 
                "acceleratorType": None,
                "acceleratorCount": 0
            })

    print(project["projectId"], project["name"], " - tot. gpu_list length: ", len(gpu_list))

# write gpu_list to gpu_list.csv
header = [
    "project_id",
    "project_name",
    "instance_name",
    "status",
    "zone",
    "acceleratorType",
    "acceleratorCount"
]
with open('gpu_list.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    for instance in gpu_list:
        writer.writerow(instance.values())
