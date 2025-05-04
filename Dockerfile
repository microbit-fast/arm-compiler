FROM archlinux:latest

RUN pacman -Syu --noconfirm arm-none-eabi-gcc arm-none-eabi-binutils arm-none-eabi-newlib python python-pip
COPY . /app
WORKDIR /app
RUN pip install flask

EXPOSE 5000
CMD ["python", "server.py"]
