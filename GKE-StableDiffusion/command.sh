#Enable API
gcloud services enable compute.googleapis.com artifactregistry.googleapis.com container.googleapis.com file.googleapis.com vpcaccess.googleapis.com redis.googleapis.com cloudscheduler.googleapis.com

#Enviroment Viriable
PROJECT_ID='hy-sd-001'
GKE_CLUSTER_NAME='hy-sd-gke'
REGION='us-central1'
VPC_NETWORK='default'
VPC_SUBNETWORK='default'
BUILD_REGIST='hy-repo-001'
FILESTORE_NAME='hy-fstore-001'
FILESTORE_ZONE='us-central1-a'
FILESHARE_NAME='hy_fshare_001'

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
gcloud container clusters get-credentials ${GKE_CLUSTER_NAME} --region ${REGION}
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml

#Create Docker Repo
gcloud artifacts repositories create ${BUILD_REGIST} --repository-format=docker \
--location=${REGION}
gcloud auth configure-docker ${REGION}-docker.pkg.dev

# Build Stable Diffusion Image
cd Stable-Diffusion-on-GCP/Stable-Diffusion-UI-Agones/sd-webui
docker build . -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/${BUILD_REGIST}/sd-webui:0.1
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${BUILD_REGIST}/sd-webui:0.1

#Create FileStor and mount
gcloud filestore instances create ${FILESTORE_NAME} --zone=${FILESTORE_ZONE} --tier=BASIC_HDD --file-share=name=${FILESHARE_NAME},capacity=1TB --network=name=${VPC_NETWORK}
gcloud filestore instances create nfs-store --zone=us-central1-b --tier=BASIC_HDD --file-share=name="vol1",capacity=1TB --network=name=${VPC_NETWORK}
kubectl apply -f ./Stable-Diffusion-UI-Agones/agones/nfs_pv.yaml
kubectl apply -f ./Stable-Diffusion-UI-Agones/agones/nfs_pvc.yaml

# Install Argones
helm repo add agones https://agones.dev/chart/stable
helm repo update
kubectl create namespace agones-system
cd Stable-Diffusion-on-GCP/Stable-Diffusion-UI-Agones
helm install sd-agones-release --namespace agones-system -f ./agones/values.yaml agones/agones

# Create Redis
gcloud redis instances create --project=${PROJECT_ID}  sd-agones-cache --tier=standard --size=1 --region=${REGION} --redis-version=redis_6_x --network=projects/${PROJECT_ID}/global/networks/${VPC_NETWORK} --connect-mode=DIRECT_PEERING
gcloud redis instances describe sd-agones-cache --region ${REGION} --format=json | jq .host
