name="us-west"
zone="southamerica-west1-a	"



gcloud compute backend-services create bk-$name \
      --load-balancing-scheme=EXTERNAL_MANAGED \
      --protocol=HTTP \
      --port-name=http \
      --health-checks=httpck \
      --global


gcloud compute instance-groups set-named-ports vm-$name \
    --named-ports http:80 \
    --zone $zone


gcloud compute backend-services add-backend bk-$name \
      --instance-group=vm-$name \
      --instance-group-zone=$zone \
      --global