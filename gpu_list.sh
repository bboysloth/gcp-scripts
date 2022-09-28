# simple gcloud commands for extracting all instances with a GPU attached
# outputs to the console as a table
# Jeremy Hannan June 2022

#!/bin/bash

for proj in $(gcloud alpha projects list --folder=189084715210 --format='value(PROJECT_ID)'); do for gpu_zone in $(gcloud compute instances list --project=$proj --format='value(ZONE)'); do for gpu_attached in $(gcloud compute instances list --project=$proj --zones=$gpu_zone --format='value(NAME)'); do gcloud compute instances describe $gpu_attached --project=$proj --zone=$gpu_zone --format="table(name,zone.basename(),guestAccelerators[].acceleratorCount,guestAccelerators[].acceleratorType.basename())"; done; done; done
