FROM debian:bullseye-slim

WORKDIR /app

# Instalar dependências mínimas
RUN apt-get update && apt-get install -y \
    python3 \
    zip unzip \
    libfreetype6 libglib2.0-0 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Copiar o JDK e SDKs para dentro do container
#COPY jdk1.8.0_431     /app/jdk1.8.0_431
COPY jdk-24           /app/jdk-24
COPY javafx-sdk-24    /app/javafx-sdk-24
COPY jarlibs          /app/jarlibs
COPY androidFX        /app/androidFX
COPY sdks/android     /app/sdks/android
COPY builder.py       /app/builder.py

# Variáveis de ambiente
ENV JAVA_HOME=/app/jdk-24
ENV ANDROID_SDK=/app/sdks/android
ENV PATH="$JAVA_HOME/bin:$ANDROID_SDK/platform-tools:$ANDROID_SDK/build-tools/34.0.0:$PATH"

ENTRYPOINT ["python3", "/app/builder.py"]
