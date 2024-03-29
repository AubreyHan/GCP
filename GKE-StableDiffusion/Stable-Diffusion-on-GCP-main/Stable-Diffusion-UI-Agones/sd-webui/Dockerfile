FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

RUN set -ex && \
    apt update && \
    apt install -y wget git python3 python3-venv python3-pip libglib2.0-0 pkg-config libcairo2-dev && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117
RUN python3 -m pip install git+https://github.com/TencentARC/GFPGAN.git@8d2447a2d918f8eba5a4a01463fd48e45126a379 --prefer-binary
RUN python3 -m pip install git+https://github.com/openai/CLIP.git@d50d76daa670286dd6cacf3bcd80b5e4823fc8e1 --prefer-binary
RUN python3 -m pip install git+https://github.com/mlfoundations/open_clip.git@bb6e834e9c70d9c27d0dc3ecedeebeaeb1ffad6b --prefer-binary
RUN python3 -m pip install xformers==0.0.16rc425 --prefer-binary
RUN python3 -m pip install pyngrok --prefer-binary
RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
RUN git clone https://github.com/Stability-AI/stablediffusion.git /stable-diffusion-webui/repositories/stable-diffusion-stability-ai
RUN git -C /stable-diffusion-webui/repositories/stable-diffusion-stability-ai checkout cf1d67a6fd5ea1aa600c4df58e5b47da45f6bdbf
RUN git clone https://github.com/CompVis/taming-transformers.git /stable-diffusion-webui/repositories/taming-transformers
RUN git -C /stable-diffusion-webui/repositories/taming-transformers checkout 24268930bf1dce879235a7fddd0b2355b84d7ea6
RUN git clone https://github.com/crowsonkb/k-diffusion.git /stable-diffusion-webui/repositories/k-diffusion
RUN git -C /stable-diffusion-webui/repositories/k-diffusion checkout 5b3af030dd83e0297272d861c19477735d0317ec
RUN git clone https://github.com/sczhou/CodeFormer.git /stable-diffusion-webui/repositories/CodeFormer
RUN git -C /stable-diffusion-webui/repositories/CodeFormer checkout c5b4593074ba6214284d6acd5f1719b6c5d739af
RUN git clone https://github.com/salesforce/BLIP.git /stable-diffusion-webui/repositories/BLIP
RUN git -C /stable-diffusion-webui/repositories/BLIP checkout 48211a1594f1321b00f14c9f7a5b4813144b2fb9
RUN python3 -m pip install -r /stable-diffusion-webui/repositories/CodeFormer/requirements.txt --prefer-binary
RUN python3 -m pip install -r /stable-diffusion-webui/requirements_versions.txt --prefer-binary

RUN set -ex && cd stable-diffusion-webui \
    && git clone https://gitcode.net/ranting8323/sd-webui-additional-networks.git extensions/sd-webui-additional-networks \
    && git clone https://gitcode.net/ranting8323/sd-webui-cutoff extensions/sd-webui-cutoff \
    && git clone https://ghproxy.com/https://github.com/toshiaki1729/stable-diffusion-webui-dataset-tag-editor.git extensions/stable-diffusion-webui-dataset-tag-editor \
    && git clone https://ghproxy.com/https://github.com/yfszzx/stable-diffusion-webui-images-browser extensions/stable-diffusion-webui-images-browser \
    && git clone https://gitcode.net/ranting8323/stable-diffusion-webui-wd14-tagger.git extensions/stable-diffusion-webui-wd14-tagger \
    && git clone https://gitcode.net/overbill1683/stable-diffusion-webui-localization-zh_Hans.git extensions/stable-diffusion-webui-localization-zh_Hans \
    && git clone https://gitcode.net/ranting8323/a1111-sd-webui-tagcomplete.git extensions/a1111-sd-webui-tagcomplete \
    && git clone https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet

RUN python3 -m pip install -r /stable-diffusion-webui/extensions/sd-webui-controlnet/requirements.txt --prefer-binary

EXPOSE 7860

COPY user-watch.py /stable-diffusion-webui/user-watch.py
COPY start.sh /stable-diffusion-webui/start.sh

WORKDIR /stable-diffusion-webui/
CMD ["python3", "launch.py", "--listen", "--xformers", "--medvram", "--enable-insecure-extension-access"]
