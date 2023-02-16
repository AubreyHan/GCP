#Env
ProjectID="hy-20230214-001"
VMName="vmdemo"
Disk="vmdemo"
Image="vmdemo-image"
Region="us-central1"
Zone="us-central1-a"
InstanceTemplate="vm-instance-template"
MachineType="n2-standard-2"

#Stop Template VM
gcloud compute instances stop --project=$ProjectID --zone=$Zone $VMName-v2

#Capture Disk Image
gcloud compute images create $Image-v2 --project=$ProjectID --source-disk=$Disk-v2  --source-disk-zone=$Zone --storage-location=$Region

#Create Instance Template
gcloud compute instance-templates create $InstanceTemplate-v2 --project=$ProjectID --machine-type=$MachineType --network-interface=network=default,network-tier=PREMIUM --tags=http-server,https-server --create-disk=auto-delete=yes,boot=yes,image=projects/$ProjectID/global/images/$Image-v2,size=10,type=pd-balanced

