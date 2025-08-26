FROM ros:jazzy-ros-base

ARG USERNAME=norden
ARG USER_UID=1000
ARG USER_GID=$USER_UID

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN if id -u $USER_UID ; then userdel `id -un $USER_UID` ; fi

RUN groupadd -g ${USER_GID} ${USERNAME} \
 && useradd -m -s /bin/bash -u ${USER_UID} -g ${USER_GID} ${USERNAME} \
 && apt-get update \
 && apt-get install -y --no-install-recommends sudo \
 && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
 && chmod 0440 /etc/sudoers.d/${USERNAME}


RUN apt-get update && apt-get install -y --no-install-recommends \
      python3-colcon-common-extensions python3-rosdep \
      ros-jazzy-ros2bag ros-jazzy-rosbag2-storage-sqlite3 ros-jazzy-rosbag2-storage-mcap \
      git build-essential cmake \
      python3-pip \
      python3-venv

# RUN python3 -m venv .venv
# RUN source .venv/bin/activate && pip3 install --no-cache-dir rosbags rosbags-image tqdm

RUN rm -rf /var/lib/apt/lists/*

RUN rosdep init || true

USER ${USERNAME}
WORKDIR /home/ws
CMD ["bash"]
