#Enable API
gcloud services enable compute.googleapis.com artifactregistry.googleapis.com container.googleapis.com file.googleapis.com vpcaccess.googleapis.com redis.googleapis.com cloudscheduler.googleapis.com

#Enviroment Viriable
PROJECT_ID='hy-sd-001'
GKE_CLUSTER_NAME='hy-sd-gke'
REGION='us-central1'
VPC_NETWORK='default'
VPC_SUBNETWORK='default'

#GKE Create and Config
gcloud beta container --project ${PROJECT_ID} clusters create ${GKE_CLUSTER_NAME} --region ${REGION} \
    --no-enable-basic-auth --release-channel "None" \
    --machine-type "e2-standard-2" \
    --image-type "COS_CONTAINERD" --disk-type "pd-balanced" --disk-size "100" \
    --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/cloud-platform" \
    --num-nodes "1" --logging=SYSTEM,WORKLOAD --monitoring=SYSTEM --enable-ip-alias \
    --network "projects/${PROJECT_ID}/global/networks/${VPC_NETWORK}" \
    --subnetwork "projects/${PROJECT_ID}/regions/${REGION}/subnetworks/${VPC_SUBNETWORK}" \
    --no-enable-intra-node-visibility --default-max-pods-per-node "110" --no-enable-master-authorized-networks \
    --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver,GcpFilestoreCsiDriver \
    --autoscaling-profile optimize-utilization
gcloud beta container --project ${PROJECT_ID} node-pools create "gpu-pool" --cluster ${GKE_CLUSTER_NAME} --region ${REGION} --machine-type "custom-4-49152-ext" --accelerator "type=nvidia-tesla-t4,count=1" --image-type "COS_CONTAINERD" --disk-type "pd-balanced" --disk-size "100" --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/cloud-platform" --enable-autoscaling --total-min-nodes "0" --total-max-nodes "6" --location-policy "ANY" --enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 --max-pods-per-node "110" --num-nodes "0"
