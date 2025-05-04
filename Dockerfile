FROM archlinux:latest

RUN pacman -Syu --noconfirm arm-none-eabi-gcc arm-none-eabi-binutils arm-none-eabi-newlib python python-pip python-flask
COPY . /app
WORKDIR /app

EXPOSE 5000
CMD ["python", "server.py"]
